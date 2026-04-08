#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
owon_vds1022.py — Standalone Python API for the OWON VDS1022 / VDS1022I oscilloscope
=======================================================================================

A clean, self-contained rewrite of the VDS1022 Python interface.
No external project files are needed — just install the dependencies below.

Dependencies (install with pip):
    pip install pyusb numpy matplotlib scipy

Optional extras for richer output:
    pip install pandas bokeh

Quick-start
-----------
    from owon_vds1022 import Oscilloscope, CH1, CH2, DC, AC, RISE, FALL, EDGE, ONCE

    with Oscilloscope() as osc:
        osc.set_channel(CH1, volt_range='10v', probe='x10', coupling=DC)
        osc.set_trigger(CH1, mode=EDGE, condition=RISE, level='2v', sweep=ONCE)
        osc.set_timerange('20ms')
        frames = osc.fetch()
        print(frames.ch1.describe())
        frames.plot()
"""

# ──────────────────────────────────────────────────────────────────────────────
# Standard library
# ──────────────────────────────────────────────────────────────────────────────
import bisect
import collections
import csv
import datetime
import gc
import json
import logging
import os
import struct
import sys
import threading
import time
from array import array
from copy import copy, deepcopy
from math import ceil, copysign, floor, log10, pi, sqrt

assert sys.version_info >= (3, 6), "Python 3.6+ required"

# ──────────────────────────────────────────────────────────────────────────────
# Third-party
# ──────────────────────────────────────────────────────────────────────────────
try:
    import usb.backend.libusb1 as _libusb1
    import usb.backend.libusb0 as _libusb0
    from usb.core import USBError
    import numpy as np
except ImportError as _e:
    raise ImportError(
        "Missing required packages. Install with:\n"
        "    pip install pyusb numpy"
    ) from _e

# ──────────────────────────────────────────────────────────────────────────────
# Public API symbols
# ──────────────────────────────────────────────────────────────────────────────
__all__ = (
    "Oscilloscope",
    "Frame", "Frames",
    "CH1", "CH2", "EXT",
    "DC", "AC", "GND",
    "EDGE", "SLOPE", "PULSE",
    "AUTO", "NORMAL", "ONCE",
    "RISE", "FALL",
    "RISE_SUP", "RISE_EQU", "RISE_INF",
    "FALL_SUP", "FALL_EQU", "FALL_INF",
    "VOLT_RANGES", "SAMPLING_RATES",
)

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

# Channels
CH1 = 0
CH2 = 1
EXT = 2

# Coupling
AC  = 0
DC  = 1
GND = 2

# Trigger modes
EDGE  = 0
VIDEO = 1
SLOPE = 2
PULSE = 3

# Trigger conditions
RISE_SUP =  0
RISE_EQU =  1
RISE_INF =  2
FALL_SUP =  3 - 128
FALL_EQU =  4 - 128
FALL_INF =  5 - 128
RISE = RISE_SUP
FALL = FALL_SUP

# Sweep modes
AUTO   = 0
NORMAL = 1
ONCE   = 2

# Multi-port modes
_MULTI_OUT = 0
_MULTI_PF  = 1
_MULTI_IN  = 2

# Available settings
VOLT_RANGES = (50e-3, 100e-3, 200e-3, 500e-3, 1, 2, 5, 10, 20, 50)
SAMPLING_RATES = (
    2.5, 5, 12.5, 25, 50, 125, 250, 500,
    1.25e3, 2.5e3, 5e3, 12.5e3, 25e3, 50e3, 125e3, 250e3, 500e3,
    1.25e6, 2.5e6, 5e6, 12.5e6, 25e6, 50e6, 100e6,
)

# ADC / frame geometry
_FRAME_SIZE = 5211   # 11 header + 100 trigger buffer + 5100 ADC
_ADC_SIZE   = 5100   # 50 pre + 5000 signal + 50 post
_ADC_MAX    = +125
_ADC_MIN    = -125
_ADC_RANGE  = 250
_SAMPLES    = 5000
_HTP_ERR    = 11     # horizontal trigger position correction

# Calibration indices
_GAIN = 0
_AMPL = 1
_COMP = 2

# Attenuation relay engages at or above this volt-range index
_ATTEN_IDX  = 6

# Roll mode threshold (samples/s): below this, roll mode activates automatically
_ROLL_THRESH = 2500

# USB identifiers
_USB_VID     = 0x5345
_USB_PID     = 0x1234
_USB_INTF    = 0
_USB_TIMEOUT = 200     # ms

_FLASH_SIZE  = 2002

log = logging.getLogger("owon_vds1022")


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def _find_ge(arr, x):
    """Index of first value >= x."""
    i = bisect.bisect_left(arr, x)
    return min(i, len(arr) - 1)

def _find_le(arr, x):
    """Index of last value <= x."""
    i = bisect.bisect_right(arr, x) - 1
    return max(i, 0)

def _u8(x):  return x & 0xFF
def _u16(lo, hi): return (lo & 0xFF) | ((hi & 0xFF) << 8)
def _swap16(x): return ((x & 0xFF00) >> 8) | ((x & 0x00FF) << 8)
def _bit_mask(flags): return sum(1 << i for i, f in enumerate(flags) if f)

def _iexp10(value, limit):
    """Split value into mantissa <= limit and base-10 exponent."""
    m, e = value, 0
    while m > limit:
        m, e = m / 10, e + 1
    return round(m), e

def _rms(arr):
    return float(sqrt(np.square(arr, dtype=np.float32).mean()))

def _precision(x, n=5):
    if not x:
        return 0.0
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))

def _rfft(data, window, size):
    size  = 2 ** int(log2(min(size or len(data), 4096)))
    trim  = (len(data) - size) >> 1
    data  = data[trim: -trim or None]
    scale = 2 / size
    if window is not None:
        win   = window(size)
        data  = data * win
        scale /= win.mean()
    return np.fft.rfft(data), scale

def _quad_interp(yy, i):
    """Quadratic spectral peak interpolation."""
    yi = yy[i]
    yp = yy[i - 1] if i > 0 else yy[i + 1]
    yn = yy[i + 1] if i + 1 < len(yy) else yy[i - 1]
    x  = i + 0.5 * (yp - yn) / (yp - 2 * yi + yn)
    y  = yi - 0.25 * (yp - yn) * (x - i)
    return x, y

def log2(x):
    import math
    return math.log2(x)


# ──────────────────────────────────────────────────────────────────────────────
# Argument parsing helpers
# ──────────────────────────────────────────────────────────────────────────────

_SI = {'M': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12}

_CONST_MAP = {
    'CH1': CH1, 'CH2': CH2, 'EXT': EXT,
    'DC': DC, 'AC': AC, 'GND': GND,
    'EDGE': EDGE, 'SLOPE': SLOPE, 'PULSE': PULSE,
    'AUTO': AUTO, 'NORMAL': NORMAL, 'ONCE': ONCE,
    'RISE': RISE, 'FALL': FALL,
    'RISE_SUP': RISE_SUP, 'RISE_EQU': RISE_EQU, 'RISE_INF': RISE_INF,
    'FALL_SUP': FALL_SUP, 'FALL_EQU': FALL_EQU, 'FALL_INF': FALL_INF,
}

def _parse_si(text):
    """Parse SI-suffixed number string, e.g. '10k', '2.5M', '500m'."""
    text = text.strip()
    if text[-1] in _SI:
        return float(text[:-1]) * _SI[text[-1]]
    return float(text)

def _parse_volts(v):
    if isinstance(v, str):
        return _parse_si(v.rstrip('Vv'))
    return float(v)

def _parse_seconds(v):
    if isinstance(v, str):
        return _parse_si(v.rstrip('sS'))
    return float(v)

def _parse_freq(v):
    if isinstance(v, str):
        return _parse_si(v.rstrip('Hz'))
    return float(v)

def _parse_probe(v):
    if isinstance(v, str):
        return float(v.strip('Xx'))
    return float(v)

def _parse_ratio(v):
    if isinstance(v, str):
        return float(v.replace('%', 'e-2'))
    return float(v)

def _parse_const(v):
    if isinstance(v, str):
        key = v.upper()
        if key not in _CONST_MAP:
            raise ValueError(f"Unknown constant: {v!r}")
        return _CONST_MAP[key]
    return int(v)


# ──────────────────────────────────────────────────────────────────────────────
# USB command table
# ──────────────────────────────────────────────────────────────────────────────

class _Cmd:
    """Encapsulates a USB command: address + packing format."""

    _BI   = struct.Struct('<BI')
    _IBB  = struct.Struct('<IBB')
    _IBH  = struct.Struct('<IBH')
    _IBI  = struct.Struct('<IBI')

    def __init__(self, name, address, fmt):
        self.name    = name
        self.address = address
        self._fmt    = fmt
        self.size    = fmt.size - 5

    def pack(self, arg):
        return array('B', self._fmt.pack(self.address, self.size, arg))

    def unpack_response(self, buf):
        _, value = self._BI.unpack_from(buf)
        return value


class _CmdTable:
    """All USB commands."""

    _IBB = struct.Struct('<IBB')
    _IBH = struct.Struct('<IBH')
    _IBI = struct.Struct('<IBI')

    READ_FLASH       = _Cmd('READ_FLASH',       0x01B0, _IBB)
    WRITE_FLASH      = _Cmd('WRITE_FLASH',      0x01A0, _IBB)
    QUERY_FPGA       = _Cmd('QUERY_FPGA',       0x0223, _IBB)
    LOAD_FPGA        = _Cmd('LOAD_FPGA',        0x4000, _IBI)
    GET_MACHINE      = _Cmd('GET_MACHINE',      0x4001, _IBB)
    GET_DATA         = _Cmd('GET_DATA',         0x1000, _IBH)
    GET_TRIGGERED    = _Cmd('GET_TRIGGERED',    0x0001, _IBB)
    SET_MULTI        = _Cmd('SET_MULTI',        0x0006, _IBH)
    SET_PEAKMODE     = _Cmd('SET_PEAKMODE',     0x0009, _IBB)
    SET_ROLLMODE     = _Cmd('SET_ROLLMODE',     0x000A, _IBB)
    SET_CHL_ON       = _Cmd('SET_CHL_ON',       0x000B, _IBB)
    SET_FORCETRG     = _Cmd('SET_FORCETRG',     0x000C, _IBB)
    SET_PHASEFINE    = _Cmd('SET_PHASEFINE',    0x0018, _IBH)
    SET_TRIGGER      = _Cmd('SET_TRIGGER',      0x0024, _IBH)
    SET_TIMEBASE     = _Cmd('SET_TIMEBASE',     0x0052, _IBI)
    SET_SUF_TRG      = _Cmd('SET_SUF_TRG',      0x0056, _IBI)
    SET_PRE_TRG      = _Cmd('SET_PRE_TRG',      0x005A, _IBH)
    SET_DEEPMEMORY   = _Cmd('SET_DEEPMEMORY',   0x005C, _IBH)
    SET_RUNSTOP      = _Cmd('SET_RUNSTOP',      0x0061, _IBB)
    GET_STOPPED      = _Cmd('GET_STOPPED',      0x00B1, _IBB)

    # Per-channel commands: index 0 → CH1, 1 → CH2
    SET_CHANNEL      = (_Cmd('SET_CHANNEL_CH1',    0x0111, _IBB),
                        _Cmd('SET_CHANNEL_CH2',    0x0110, _IBB))
    SET_ZERO_OFF     = (_Cmd('SET_ZERO_OFF_CH1',   0x010A, _IBH),
                        _Cmd('SET_ZERO_OFF_CH2',   0x0108, _IBH))
    SET_VOLT_GAIN    = (_Cmd('SET_VOLT_GAIN_CH1',  0x0116, _IBH),
                        _Cmd('SET_VOLT_GAIN_CH2',  0x0114, _IBH))
    SET_EDGE_LEVEL   = (_Cmd('SET_EDGE_LEVEL_CH1', 0x002E, _IBH),
                        _Cmd('SET_EDGE_LEVEL_CH2', 0x0030, _IBH))
    SET_SLOPE_THRED  = (_Cmd('SET_SLOPE_THRED_CH1',0x0010, _IBH),
                        _Cmd('SET_SLOPE_THRED_CH2',0x0012, _IBH))
    SET_TRG_HOLDOFF  = (_Cmd('SET_TRG_HOLDOFF_CH1',0x0026, _IBH),
                        _Cmd('SET_TRG_HOLDOFF_CH2',0x002A, _IBH))
    SET_TRG_CDT_GL   = (_Cmd('SET_TRG_CDT_GL_CH1', 0x0042, _IBH),
                        _Cmd('SET_TRG_CDT_GL_CH2', 0x0046, _IBH))
    SET_TRG_CDT_HL   = (_Cmd('SET_TRG_CDT_HL_CH1', 0x0044, _IBH),
                        _Cmd('SET_TRG_CDT_HL_CH2', 0x0048, _IBH))
    SET_TRG_CDT_EQU_H= (_Cmd('SET_TRG_CDT_EQU_H_CH1',0x0032, _IBH),
                        _Cmd('SET_TRG_CDT_EQU_H_CH2',0x003A, _IBH))
    SET_TRG_CDT_EQU_L= (_Cmd('SET_TRG_CDT_EQU_L_CH1',0x0036, _IBH),
                        _Cmd('SET_TRG_CDT_EQU_L_CH2',0x003E, _IBH))
    SET_FREQREF      = (_Cmd('SET_FREQREF_CH1',    0x004A, _IBB),
                        _Cmd('SET_FREQREF_CH2',    0x004B, _IBB))

CMD = _CmdTable()


# ──────────────────────────────────────────────────────────────────────────────
# Flash memory I/O
# ──────────────────────────────────────────────────────────────────────────────

class _Flash:
    """Read/write structured data from the device flash image."""

    def __init__(self, data):
        self._buf = bytearray(data)
        self._pos = 0

    def seek(self, pos):
        self._pos = pos

    def read(self, fmt):
        result = struct.unpack_from(fmt, self._buf, self._pos)
        self._pos += struct.calcsize(fmt)
        return result if len(result) > 1 else result[0]

    def write(self, fmt, *values):
        struct.pack_into(fmt, self._buf, self._pos, *values)
        self._pos += struct.calcsize(fmt)

    def read_str(self):
        end = self._buf.index(0, self._pos)
        s = self._buf[self._pos:end].decode('ascii')
        self._pos = end + 1
        return s

    def write_str(self, text):
        b = text.encode('ascii') + b'\x00'
        self._buf[self._pos:self._pos + len(b)] = b
        self._pos += len(b)

    @property
    def buffer(self):
        return bytes(self._buf)


# ──────────────────────────────────────────────────────────────────────────────
# Frame — holds samples from one channel
# ──────────────────────────────────────────────────────────────────────────────

class Frame:
    """
    One acquisition frame for a single channel.

    Attributes
    ----------
    channel   : int   — CH1 (0) or CH2 (1)
    name      : str   — 'CH1' or 'CH2'
    sx        : float — seconds per ADC sample (time scale)
    tx        : float — time at sample[0] relative to trigger (seconds)
    sy        : float — volts per ADC unit (voltage scale)
    ty        : float — voltage at ADC=0 (offset in volts)
    size      : int   — number of samples (5000)
    ylim      : tuple — (lower_v, upper_v) display range
    frequency : float — measured frequency in Hz (None if unavailable)
    """

    def __init__(self, channel, volt_range, probe, volt_offset,
                 sampling_rate, trigger_position, raw_buffer, frequency=None):
        """
        Parameters
        ----------
        channel         : int   — CH1 or CH2
        volt_range      : float — V/div * 10 (full-scale range at probe tip)
        probe           : float — probe attenuation ratio (e.g. 10)
        volt_offset     : float — offset as fraction of full range (−0.5..+0.5)
        sampling_rate   : float — samples per second
        trigger_position: float — 0..1 fraction of frame where trigger sits
        raw_buffer      : bytes/array — raw ADC bytes (int8), at least _SAMPLES long
        frequency       : float — optional pre-measured frequency
        """
        self.channel   = channel
        self.name      = ('CH1', 'CH2')[channel]
        self.frequency = frequency

        vr = volt_range * probe          # full-scale probe range
        self.sy = vr / _ADC_RANGE        # volts per ADC unit
        self.ty = -vr * volt_offset      # voltage at ADC == 0

        self.sx = 1.0 / sampling_rate
        self.tx = -_SAMPLES * self.sx * trigger_position  # leftmost time

        self.size = _SAMPLES
        self.ylim = (self.ty - vr / 2, self.ty + vr / 2)

        # Keep raw int8 points
        self._pts = np.frombuffer(raw_buffer, dtype=np.int8,
                                   count=_SAMPLES).copy()

    # ── Waveform arrays ────────────────────────────────────────────────────────

    def x(self):
        """numpy array of time values in seconds (relative to trigger)."""
        return np.linspace(self.tx, self.tx + _SAMPLES * self.sx,
                           _SAMPLES, endpoint=False, dtype=np.float32)

    def y(self):
        """numpy array of voltage values in volts."""
        return self._pts * np.float32(self.sy) + np.float32(self.ty)

    # ── Scalar measurements ────────────────────────────────────────────────────

    def avg(self):
        """Mean voltage (V)."""
        return round(float(self._pts.mean()) * self.sy + self.ty, 4)

    def rms(self):
        """True RMS voltage (V)."""
        pts = self._pts + np.float32(self.ty / self.sy)
        return round(_rms(pts) * self.sy, 4)

    def std(self):
        """Standard deviation (V)."""
        pts = self._pts + np.float32(self.ty / self.sy)
        return round(float(pts.std()) * self.sy, 4)

    def median(self):
        """Median voltage (V)."""
        return round(float(np.median(self._pts)) * self.sy + self.ty, 4)

    def min(self):
        """Minimum voltage (V)."""
        return round(float(self._pts.min()) * self.sy + self.ty, 4)

    def max(self):
        """Maximum voltage (V)."""
        return round(float(self._pts.max()) * self.sy + self.ty, 4)

    def vpp(self):
        """Peak-to-peak voltage (V)."""
        return round(self.max() - self.min(), 4)

    def amp(self):
        """Amplitude Vtop − Vbase (V), based on histogram levels."""
        lo, hi = self.levels()
        return round(hi - lo, 4)

    def crest_factor(self):
        """Crest factor = Vmax / Vrms."""
        r = self.rms()
        return round(self.max() / r, 4) if r else None

    def levels(self):
        """
        Most-prevalent low and high voltage levels (Vbase, Vtop).
        Uses histogram to find the two dominant levels in a digital/periodic signal.
        """
        pts = self._pts + 128           # shift to 0..255
        counts = np.bincount(pts, minlength=256)
        mid = int(np.dot(counts, np.arange(256)) // len(pts))
        lo  = int(np.argmax(counts[:mid + 1])) - 128
        hi  = int(np.argmax(counts[mid:])) + mid - 128
        return lo * self.sy + self.ty, hi * self.sy + self.ty

    # ── Frequency / phase ──────────────────────────────────────────────────────

    def freq(self, period=360, start=-0.5):
        """
        Estimate fundamental frequency and phase.

        Parameters
        ----------
        period : float  — wrap range for phase (360 for degrees, 2π for radians)
        start  : float  — phase start ratio (default −0.5 → range is [−period/2, +period/2])

        Returns
        -------
        (frequency_Hz, phase) or (None, None) if no periodic signal detected.
        """
        ys = self._pts - np.float32(self._pts.mean())
        if ys.max() <= 15:
            return None, None

        crossings = np.nonzero((ys[1:] >= 0) & (ys[:-1] < 0))[0]
        if crossings.size < 2:
            return None, None

        gaps    = np.diff(crossings)
        thresh  = gaps.max() * 0.8
        mask    = np.diff(crossings, prepend=-thresh) > thresh
        crossings = crossings[mask]
        if crossings.size < 2:
            return None, None

        period_pts = float(np.mean(np.diff(crossings)))
        frequency  = 1.0 / (period_pts * self.sx)
        phase_frac = float(np.mean((1 + len(ys) / 2 + crossings) % period_pts)) / period_pts
        phase      = ((phase_frac - start + 1) % 1.0 + start) * period
        return round(frequency, 4), round(-phase, 4)

    # ── Spectrum / FFT ─────────────────────────────────────────────────────────

    def spectrum(self, window=None, size=None):
        """
        Compute magnitude and phase spectrum via FFT.

        Parameters
        ----------
        window : callable — windowing function (e.g. np.blackman). None = rectangular.
        size   : int      — FFT size (power of 2). None = auto.

        Returns
        -------
        (frequencies_Hz, magnitudes_V, phases_normalised)
        """
        if window is None:
            window = np.blackman
        ft, scale = _rfft(self.y(), window, size)
        freqs  = np.linspace(0, 0.5 / self.sx, len(ft))
        mags   = np.abs(ft) * scale
        phases = (np.angle(ft) / pi + 2.5) % 2 - 1
        return freqs, mags, phases

    def dominant_components(self, threshold=0.01, window=None, size=None):
        """
        Return dominant spectral components above a relative threshold.

        Parameters
        ----------
        threshold : float — fraction of peak magnitude to include (default 1%)

        Returns
        -------
        list of (frequency_Hz, magnitude_V, phase) sorted by magnitude descending
        """
        if window is None:
            window = np.blackman
        pts = self._pts + np.float32(self.ty / self.sy)
        ft, scale = _rfft(pts, window, size)
        mag_adc   = np.abs(ft) * scale
        dy        = _parse_ratio(threshold) * _ADC_MAX

        avg_mag = np.convolve(mag_adc, np.ones(10)).flatten()
        ii = np.nonzero(np.diff(avg_mag, prepend=0) > dy)[0]
        ii = ii[np.nonzero(np.diff(ii, prepend=0) > 1)[0]]
        ii = [max(0, i - 2) + int(np.argmax(mag_adc[i - 2: i + 5])) for i in ii]

        if not ii:
            return []

        results = []
        for i in ii:
            xi, mi = _quad_interp(mag_adc, i)
            freq  = round(xi / len(ft) / 2 / self.sx)
            mag   = self.sy * mi
            phase = (np.angle(ft[i]) / pi + 2.5) % 2 - 1
            results.append((freq, mag, float(phase)))

        results.sort(key=lambda r: r[1], reverse=True)
        return results

    # ── Signal conditioning ────────────────────────────────────────────────────

    def to_ttl(self, ratio_low=0.2, ratio_high=0.4):
        """
        Convert to TTL logic levels (0 or 1) using hysteresis.

        Returns
        -------
        numpy int8 array of 0s and 1s
        """
        lo_pts = round((self.levels()[0] - self.ty) / self.sy)
        hi_pts = round((self.levels()[1] - self.ty) / self.sy)

        if (hi_pts - lo_pts) < 16:
            lo_pts = min(lo_pts, round(-self.ty / self.sy))
            if (hi_pts - lo_pts) < 16:
                return np.zeros(_SAMPLES, np.int8)

        thresh_hi = lo_pts + int((hi_pts - lo_pts) * ratio_high)
        thresh_lo = lo_pts + int((hi_pts - lo_pts) * ratio_low)

        pts = self._pts
        out = (pts > thresh_hi).astype(np.int8)
        mid = (pts > thresh_lo).astype(np.int8)
        for i in range(1, len(out)):
            out[i] = out[i] or (mid[i] and out[i - 1])
        return out

    def lowpass_filter(self, cutoff_ratio=0.1):
        """
        Apply a Butterworth low-pass filter in-place.

        Parameters
        ----------
        cutoff_ratio : float — cutoff as fraction of Nyquist (0 < ratio < 1)

        Returns
        -------
        self (for chaining)
        """
        try:
            from scipy import signal
        except ImportError:
            raise ImportError("scipy is required for filtering: pip install scipy")
        wn = cutoff_ratio
        b, a = signal.butter(3, wn, btype='low')
        filtered = signal.filtfilt(b, a, self._pts.astype(np.float64), padlen=200)
        self._pts = filtered.astype(np.float32)
        return self

    def slice(self, t_start, t_stop):
        """
        Extract a time slice, returning a new Frame with adjusted tx.

        Parameters
        ----------
        t_start, t_stop : float — start and stop times in seconds

        Returns
        -------
        Frame
        """
        i0 = max(0, round((t_start - self.tx) / self.sx))
        i1 = min(_SAMPLES, round((t_stop  - self.tx) / self.sx))
        if i0 >= i1:
            raise ValueError(f"Empty slice [{t_start}, {t_stop}]")
        f = copy(self)
        f._pts = self._pts[i0:i1].copy()
        f.tx   = self.tx + i0 * self.sx
        f.size = i1 - i0
        return f

    # ── Statistics summary ─────────────────────────────────────────────────────

    def describe(self):
        """
        Return a dict of key measurements for this channel.
        """
        frequency, phase = self.freq()
        vbase, vtop = self.levels()
        return {
            'Channel'  : self.name,
            'Samples'  : self.size,
            'Sampling' : f'{self.sx and 1/self.sx:.3g} S/s',
            'Vmin'     : self.min(),
            'Vmax'     : self.max(),
            'Vpp'      : self.vpp(),
            'Vavg'     : self.avg(),
            'Vrms'     : self.rms(),
            'Vstd'     : self.std(),
            'Vbase'    : round(vbase, 4),
            'Vtop'     : round(vtop,  4),
            'Vamp'     : self.amp(),
            'Frequency': frequency,
            'Period'   : round(1 / frequency, 6) if frequency else None,
            'Phase_deg': phase,
            'Crest'    : self.crest_factor(),
        }

    def __repr__(self):
        d = self.describe()
        lines = [f"Frame({self.name})"]
        for k, v in d.items():
            if k != 'Channel':
                lines.append(f"  {k:10s}: {v}")
        return '\n'.join(lines)

    # ── Protocol decoders ──────────────────────────────────────────────────────

    def decode_uart(self, baud=None, bits=8, parity=None, msb=False):
        """Decode UART from this channel. Returns list of UARTMsg namedtuples."""
        return _decode_uart([self], baud=baud, bits=bits, parity=parity, msb=msb)

    def decode_1wire(self):
        """Decode 1-Wire protocol from this channel. Returns list of WireMsg namedtuples."""
        return _decode_1wire(self)

    # ── Plotting ───────────────────────────────────────────────────────────────

    def plot(self, title=None, show=True, figsize=(12, 4)):
        """
        Plot this channel using matplotlib.

        Parameters
        ----------
        title   : str  — optional plot title
        show    : bool — call plt.show() immediately (default True)
        figsize : tuple

        Returns
        -------
        (fig, ax) tuple
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.ticker as mticker
        except ImportError:
            raise ImportError("matplotlib is required: pip install matplotlib")

        xs = self.x()
        ys = self.y()

        fig, ax = plt.subplots(figsize=figsize)
        color = '#2196F3' if self.channel == 0 else '#FF9800'
        ax.plot(xs, ys, color=color, linewidth=0.8, label=self.name)

        # Format x-axis as time with SI prefix
        def _fmt_time(x, _):
            for unit, factor in [('ms', 1e3), ('µs', 1e6), ('ns', 1e9)]:
                if abs(self.sx) < 1 / factor * 10:
                    return f'{x * factor:.3g} {unit}'
            return f'{x:.4g} s'

        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_time))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.3g} V'))

        ax.set_xlabel('Time')
        ax.set_ylabel('Voltage (V)')
        ax.set_title(title or f'{self.name} — {1/self.sx:.4g} S/s')
        ax.grid(True, alpha=0.4)
        ax.legend(loc='upper right')
        ax.set_xlim(xs[0], xs[-1])
        ax.set_ylim(*self.ylim)
        fig.tight_layout()

        if show:
            plt.show()
        return fig, ax

    # ── Export ─────────────────────────────────────────────────────────────────

    def to_csv(self, filepath):
        """
        Save time and voltage samples to a CSV file.

        Parameters
        ----------
        filepath : str — output path (e.g. 'ch1_capture.csv')
        """
        xs = self.x()
        ys = self.y()
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time_s', 'voltage_v'])
            writer.writerows(zip(xs.tolist(), ys.tolist()))
        log.info("Saved %d samples to %s", len(xs), filepath)

    def to_numpy(self):
        """Return (time_array, voltage_array) as numpy float32 arrays."""
        return self.x(), self.y()


# ──────────────────────────────────────────────────────────────────────────────
# Frames — holds one or two simultaneous channel frames
# ──────────────────────────────────────────────────────────────────────────────

class Frames:
    """
    Container for a simultaneous acquisition across one or both channels.

    Attributes
    ----------
    ch1, ch2  : Frame or None
    timestamp : float — Unix timestamp of acquisition
    """

    def __init__(self, ch1: 'Frame | None' = None, ch2: 'Frame | None' = None):
        self._frames  = (ch1, ch2)
        self.timestamp = time.time()

    # ── Access ─────────────────────────────────────────────────────────────────

    @property
    def ch1(self) -> Frame:
        f = self._frames[0]
        if f is None:
            raise RuntimeError("CH1 was not enabled in this acquisition.")
        return f

    @property
    def ch2(self) -> Frame:
        f = self._frames[1]
        if f is None:
            raise RuntimeError("CH2 was not enabled in this acquisition.")
        return f

    def __iter__(self):
        return (f for f in self._frames if f is not None)

    def __getitem__(self, idx):
        return self._frames[idx]

    # ── Multi-channel measurements ─────────────────────────────────────────────

    def phase_shift(self, degrees=True):
        """
        Phase shift between CH1 and CH2.

        Parameters
        ----------
        degrees : bool — return degrees (True) or radians (False)

        Returns
        -------
        float
        """
        period = 360 if degrees else 2 * pi
        _, p1 = self.ch1.freq(period=period, start=0)
        _, p2 = self.ch2.freq(period=period, start=0)
        if p1 is None or p2 is None:
            return None
        return ((p2 - p1 + period) % period)

    def power_factor(self):
        """
        Apparent power factor (cos φ) between CH1 (voltage) and CH2 (current).
        Both channels must be enabled.
        """
        v = self.ch1.y()
        i = self.ch2.y()
        p_real     = float(np.dot(v, i)) / len(v)
        p_apparent = _rms(v) * _rms(i)
        return round(p_real / p_apparent, 4) if p_apparent else None

    def diff(self):
        """
        Return a new Frames where CH1 = CH1 − CH2.
        Both channels must have the same volt range.
        """
        assert self._frames[0] and self._frames[1], "Both channels required"
        assert self.ch1.sy == self.ch2.sy, "Channels must have the same volt range"
        f = copy(self.ch1)
        f._pts = self.ch1._pts - (self.ch2._pts + np.float32(self.ch2.ty / self.ch2.sy))
        return Frames(ch1=f)

    def x(self):
        """Shared time axis (uses first enabled channel)."""
        for f in self:
            return f.x()
        return np.empty(0, np.float32)

    # ── Plotting ───────────────────────────────────────────────────────────────

    def plot(self, title=None, show=True, figsize=(12, 5), shared_y=False):
        """
        Plot all enabled channels in the same figure.

        Parameters
        ----------
        title    : str  — optional title
        show     : bool — call plt.show() immediately
        figsize  : tuple
        shared_y : bool — share the Y axis across channels

        Returns
        -------
        (fig, axes)
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.ticker as mticker
        except ImportError:
            raise ImportError("matplotlib is required: pip install matplotlib")

        active = list(self)
        n = len(active)
        if n == 0:
            raise RuntimeError("No channels to plot")

        fig, axes = plt.subplots(n, 1, figsize=figsize,
                                 sharex=True,
                                 sharey=shared_y,
                                 squeeze=False)
        axes = axes.flatten()

        colors = ['#2196F3', '#FF9800']

        def _fmt_time(x, _):
            ref = active[0].sx
            for unit, factor in [('ms', 1e3), ('µs', 1e6), ('ns', 1e9)]:
                if abs(ref) < 1 / factor * 10:
                    return f'{x * factor:.3g} {unit}'
            return f'{x:.4g} s'

        for ax, frame in zip(axes, active):
            xs, ys = frame.x(), frame.y()
            ax.plot(xs, ys, color=colors[frame.channel], linewidth=0.8, label=frame.name)
            ax.set_ylabel('Voltage (V)')
            ax.set_ylim(*frame.ylim)
            ax.set_xlim(xs[0], xs[-1])
            ax.grid(True, alpha=0.4)
            ax.legend(loc='upper right')
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.3g} V'))

        axes[-1].set_xlabel('Time')
        axes[-1].xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_time))

        if title:
            fig.suptitle(title)
        elif n > 1:
            descs = [f"{f.name}: {f.rms():.3g} Vrms" for f in active]
            fig.suptitle('  |  '.join(descs))

        fig.tight_layout()
        if show:
            plt.show()
        return fig, axes

    def plot_xy(self, title='XY Mode', show=True, figsize=(5, 5)):
        """
        X-Y mode plot (CH1 on X-axis, CH2 on Y-axis). Both channels required.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib is required: pip install matplotlib")

        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(self.ch1.y(), self.ch2.y(), linewidth=0.6, color='#4CAF50')
        ax.set_xlabel(f'{self.ch1.name} (V)')
        ax.set_ylabel(f'{self.ch2.name} (V)')
        ax.set_title(title)
        ax.grid(True, alpha=0.4)
        ax.set_xlim(*self.ch1.ylim)
        ax.set_ylim(*self.ch2.ylim)
        fig.tight_layout()
        if show:
            plt.show()
        return fig, ax

    def plot_spectrum(self, show=True, figsize=(12, 4), window=None, db=False):
        """
        Plot FFT spectrum of all active channels.

        Parameters
        ----------
        db     : bool — show dBV instead of Vpeak
        window : callable — windowing function (np.blackman default)
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.ticker as mticker
        except ImportError:
            raise ImportError("matplotlib is required: pip install matplotlib")

        if window is None:
            window = np.blackman

        active = list(self)
        fig, ax = plt.subplots(figsize=figsize)
        colors = ['#2196F3', '#FF9800']

        for frame in active:
            freqs, mags, _ = frame.spectrum(window=window)
            if db:
                mags = 20 * np.log10(np.maximum(mags, 1e-10))
            ax.plot(freqs, mags, color=colors[frame.channel],
                    linewidth=0.8, label=frame.name)

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('dBV' if db else 'Vpeak')
        ax.set_title('Spectrum')
        ax.grid(True, alpha=0.4)
        ax.legend()
        fig.tight_layout()
        if show:
            plt.show()
        return fig, ax

    # ── Protocol decoders ──────────────────────────────────────────────────────

    def decode_i2c(self):
        """Decode I2C: CH1=SCL, CH2=SDA. Returns list of I2CMsg namedtuples."""
        return _decode_i2c(self)

    def decode_uart(self, baud=None, bits=8, parity=None, msb=False):
        """Decode UART: CH1=TX, CH2=RX. Returns list of UARTMsg namedtuples."""
        return _decode_uart(list(self), baud=baud, bits=bits, parity=parity, msb=msb)

    # ── Export ─────────────────────────────────────────────────────────────────

    def describe(self):
        """Return list of describe() dicts for each active channel."""
        return [f.describe() for f in self]

    def to_csv(self, filepath):
        """
        Save all active channels to a single CSV file.

        Parameters
        ----------
        filepath : str
        """
        frames = list(self)
        xs = frames[0].x()
        header = ['time_s'] + [f.name + '_v' for f in frames]
        rows   = zip(xs.tolist(), *(f.y().tolist() for f in frames))
        with open(filepath, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)
        log.info("Saved to %s", filepath)

    def __repr__(self):
        parts = [f.__repr__() for f in self]
        return '\n\n'.join(parts) if parts else "Frames(empty)"


# ──────────────────────────────────────────────────────────────────────────────
# Protocol decoders (standalone, no import from other project files)
# ──────────────────────────────────────────────────────────────────────────────

import collections as _col

I2CMsg   = _col.namedtuple('I2CMsg',   ['start', 'stop', 'addr', 'rw', 'data', 'ack'])
UARTMsg  = _col.namedtuple('UARTMsg',  ['channel', 'start', 'stop', 'value', 'error'])
WireMsg  = _col.namedtuple('WireMsg',  ['channel', 'start', 'stop', 'value'])


def _decode_i2c(frames):
    """Decode I2C protocol from a Frames object (CH1=SCL, CH2=SDA)."""
    scl = frames[0].to_ttl()
    sda = frames[1].to_ttl()
    sx  = frames[0].sx
    tx  = frames[0].tx

    scl_diff = scl[1:] - scl[:-1]
    sda_diff = sda[1:] - sda[:-1]

    edges = [i for i in range(len(sda_diff))
             if sda_diff[i] and scl[i] and not scl_diff[i]]

    results = []
    for j, start in enumerate(edges):
        if sda_diff[start] < 0:  # falling SDA while SCL high → START
            stop = edges[j + 1] if j + 1 < len(edges) else len(scl_diff)
            bits  = [sda[i] for i in range(start, stop) if scl_diff[i] < 0]
            byt   = [_pack_msb(bits, i, 8) for i in range(1, len(bits), 9)]
            if byt:
                msg = I2CMsg(
                    start = tx + sx * start,
                    stop  = tx + sx * stop,
                    addr  = byt[0] >> 1,
                    rw    = byt[0] & 1,
                    data  = bytes(byt[1:]),
                    ack   = bytes(bits[9::9]),
                )
                results.append(msg)
    return results


def _pack_msb(bits, start, count):
    v = 0
    for b in bits[start: start + count]:
        v = (v << 1) | b
    shift = start + count - len(bits)
    return (v << shift) if shift > 0 else v


def _decode_uart(frame_list, baud=None, bits=8, parity=None, msb=False):
    """Decode UART from a list of Frame objects."""
    inputs    = []
    pulse_min = 1e9

    for frame in frame_list:
        ttl   = frame.to_ttl()
        diff  = ttl[1:] - ttl[:-1]
        edges = np.nonzero(diff)[0]
        if len(edges) > 1:
            pulse_min = min(pulse_min, int((edges[1:] - edges[:-1]).min()) or pulse_min)
        inputs.append((frame, ttl, diff, edges))

    if not baud:
        if pulse_min < 1e9:
            baud = round(1 / (pulse_min * frame_list[0].sx))
        else:
            baud = 9600

    size = 1 + bits + (0 if parity is None else 1) + 1
    last = -1 if parity is None else -2
    results = []

    for frame, ttl, diff, edges in inputs:
        bit_pts = 1.0 / baud / frame.sx
        p = 0
        for start in edges:
            if start >= p:
                p = start + 1 + bit_pts * 0.4
                try:
                    mbits = [ttl[round(p + i * bit_pts)] for i in range(size)]
                except IndexError:
                    continue

                if not mbits[0] and mbits[-1]:
                    val = 0
                    cs  = (parity or 0) & 1
                    for b in (mbits[1:last] if msb else mbits[last - 1:0:-1]):
                        val = (val << 1) | b
                        cs ^= b
                    err = parity is not None and cs != mbits[-2]
                    t0  = frame.tx + frame.sx * start
                    t1  = t0 + frame.sx * size
                    results.append(UARTMsg(frame.channel, t0, t1, val, err))
                    p = start + bit_pts * (size - 0.4)

    results.sort(key=lambda m: m.start)
    return results


def _decode_1wire(frame):
    """Decode 1-Wire from a single Frame."""
    sx     = frame.sx
    tx     = frame.tx
    ttl    = frame.to_ttl()
    diff   = ttl[1:] - ttl[:-1]
    edges  = np.nonzero(diff)[0]
    falls  = np.where(diff == -1)[0]

    if len(falls) < 2:
        return []

    bit_pts  = int((falls[1:] - falls[:-1]).min())
    half_pts = bit_pts / 2
    results  = []
    value    = 0
    n        = 0
    x_start  = None

    for i, idx in enumerate(edges):
        if diff[idx] != -1:
            continue
        try:
            pts = edges[i + 1] - idx
            if pts > bit_pts:
                n = 0
                continue
        except IndexError:
            break

        n   += 1
        bit  = int(pts < half_pts)
        value = (value >> 1) | (bit << 7)

        if n == 1:
            x_start = tx + sx * (1 + idx)
        elif n == 8:
            n = 0
            x_stop = tx + sx * (1 + idx + bit_pts)
            results.append(WireMsg(frame.channel, x_start, x_stop, value))

    return results


# ──────────────────────────────────────────────────────────────────────────────
# Main oscilloscope class
# ──────────────────────────────────────────────────────────────────────────────

class Oscilloscope:
    """
    Interface to the OWON VDS1022 / VDS1022I oscilloscope via USB.

    Usage
    -----
        # Context manager (recommended — ensures clean disconnect):
        with Oscilloscope() as osc:
            osc.set_channel(CH1, volt_range='10v', probe='x10')
            frames = osc.fetch()
            frames.plot()

        # Manual lifecycle:
        osc = Oscilloscope()
        ...
        osc.close()

    Constructor Parameters
    ----------------------
    firmware_dir : str  — path to directory containing FPGA .bin files.
                          Defaults to the same directory as this script.
    flash_file   : str  — path to a flash binary for disaster recovery.
    debug        : bool — print raw USB command traffic to stdout.
    """

    def __init__(self, firmware_dir=None, flash_file=None, debug=False):
        self._debug       = debug
        self._handle      = None
        self._usb         = None
        self._ep_write    = None
        self._ep_read     = None
        self._failures    = 0
        self._clock       = 0.0
        self._buf         = array('b', bytes(6000))
        self._lock        = threading.Lock()
        self._stop        = threading.Event()
        self._queue       = collections.OrderedDict()

        # Per-channel state
        self._on          = [False, False]
        self._coupling    = [DC, DC]
        self._volt_range  = [2.0, 2.0]   # full-scale V (before probe)
        self._volt_offset = [0.0, 0.0]   # fraction −0.5..+0.5
        self._probe       = [10.0, 10.0]

        # Acquisition state
        self._sampling_rate   = None
        self._trigger_pos     = 0.5
        self._sweep_mode      = None
        self._roll_mode       = False
        self._peak_mode       = False

        # Device identity / calibration (populated after connect)
        self.serial      = None
        self.version     = None
        self.calibration = None
        self._vfpga      = 1
        self._phasefine  = 0

        self._firmware_dir = firmware_dir or os.path.dirname(os.path.abspath(__file__))

        if not self._connect():
            raise IOError(
                f"OWON VDS1022 not found (USB {_USB_VID:04X}:{_USB_PID:04X}).\n"
                "Check the USB cable and that no other application is using the device."
            )

        self._load_flash(flash_file)
        self._load_calibration()
        self._load_fpga()
        self._reset_device()
        self._start_keepalive()

    # ── Context manager ────────────────────────────────────────────────────────

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    # ── USB connection ─────────────────────────────────────────────────────────

    def _connect(self):
        backend = _libusb1.get_backend() or _libusb0.get_backend()
        if backend is None:
            raise IOError("No libusb backend found. Install libusb.")

        for dev in backend.enumerate_devices():
            desc = backend.get_device_descriptor(dev)
            if desc.idVendor == _USB_VID and desc.idProduct == _USB_PID:
                try:
                    intf  = backend.get_interface_descriptor(dev, _USB_INTF, 0, 0)
                    addrs = [intf.endpoint[i].bEndpointAddress
                             for i in range(intf.bNumEndpoints)]
                    handle = backend.open_device(dev)
                    ep_wr  = next(a for a in addrs if (a & 0x80) == 0)
                    ep_rd  = next(a for a in addrs if (a & 0x80) != 0)
                    backend.claim_interface(handle, _USB_INTF)

                    self._usb      = backend
                    self._handle   = handle
                    self._ep_write = ep_wr
                    self._ep_read  = ep_rd

                    if self._send(CMD.GET_MACHINE, 86) == 1:  # 86 = ord('V')
                        log.info("Connected to VDS1022")
                        return True

                except Exception as exc:
                    if self._debug:
                        log.debug("connect attempt failed: %s", exc)
                    self._release()

        return False

    def _release(self):
        if self._handle:
            try: self._usb.release_interface(self._handle, _USB_INTF)
            except: pass
            try: self._usb.close_device(self._handle)
            except: pass
        self._usb = self._handle = self._ep_write = self._ep_read = None

    # ── USB I/O ────────────────────────────────────────────────────────────────

    def _bulk_write(self, data):
        gc.collect(0)
        self._usb.bulk_write(self._handle, self._ep_write, _USB_INTF,
                             data, _USB_TIMEOUT)
        self._clock = time.perf_counter()

    def _bulk_read(self, buf, expected=None):
        n = self._usb.bulk_read(self._handle, self._ep_read, _USB_INTF,
                                buf, _USB_TIMEOUT)
        if expected is not None and n != expected:
            raise IOError(f"Expected {expected} bytes, got {n}")
        self._failures = 0
        return n

    def _send(self, cmd, arg):
        """Send a command, return the 4-byte integer response value."""
        while True:
            try:
                self._bulk_write(cmd.pack(arg))
                self._bulk_read(self._buf, 5)
                _, value = struct.unpack_from('<BI', self._buf)
                if self._debug:
                    log.debug("[%s %s] -> %s", cmd.name, hex(arg), value)
                return value
            except USBError as exc:
                self._failures += 1
                if self._failures > 2:
                    raise
                self._stop.wait(0.01 * self._failures)

    def _push(self, cmd, arg):
        """Queue a command (de-duplicated by command identity)."""
        self._queue.pop(cmd, None)
        self._queue[cmd] = arg

    def _flush(self):
        """Send all queued commands."""
        while self._queue:
            self._send(*self._queue.popitem(last=False))

    # ── Flash ──────────────────────────────────────────────────────────────────

    def _read_flash(self):
        with self._lock:
            self._send(CMD.READ_FLASH, 1)
            buf = array('B', bytes(_FLASH_SIZE))
            self._bulk_read(buf, _FLASH_SIZE)
            return bytes(buf)

    def _load_flash(self, fname=None):
        raw = open(fname, 'rb').read() if fname else self._read_flash()
        f = _Flash(raw)

        hdr, ver = f.read('<HI')
        assert hdr in (0x55AA, 0xAA55), f"Bad flash header: {hdr:#X}"
        assert ver == 2, f"Unsupported flash version: {ver}"

        f.seek(6)
        self.calibration = [
            [list(f.read('<10H')) for _ in range(2)]
            for _ in (_GAIN, _AMPL, _COMP)
        ]

        f.seek(206)
        self._oem       = f.read('<B')
        self.version    = f.read_str()
        self.serial     = f.read_str()
        self._locales   = f.read('<100B')
        self._phasefine = f.read('<H')

        v = self.version.upper()
        if v.startswith('V2.7.0'):
            self._vfpga = 3
        elif v.startswith('V2.4.623') or v.startswith('V2.6.0'):
            self._vfpga = 2
        elif v.startswith('V2.') or v.startswith('V1.'):
            self._vfpga = 1
        elif v.startswith('V'):
            self._vfpga = int(v[1:v.index('.')])
        else:
            raise ValueError(f"Unexpected device version: {self.version!r}")

        log.info("Device: serial=%s  version=%s  FPGA_v%s",
                 self.serial, self.version, self._vfpga)

    # ── Calibration persistence ────────────────────────────────────────────────

    def _cal_path(self):
        return os.path.join(
            os.path.expanduser('~'),
            f'.owon_{self.serial}_cal.json'
        )

    def _load_calibration(self):
        p = self._cal_path()
        if os.path.isfile(p):
            try:
                with open(p) as fh:
                    saved = json.load(fh)
                self.calibration = saved['calibration']
                log.info("Loaded calibration from %s", p)
                return
            except Exception as exc:
                log.warning("Could not load calibration file %s: %s", p, exc)
        log.info("Using factory calibration from device flash.")

    def _save_calibration(self):
        p = self._cal_path()
        with open(p, 'w') as fh:
            json.dump({'serial': self.serial,
                       'version': self.version,
                       'calibration': self.calibration}, fh, indent=2)
        log.info("Calibration saved to %s", p)

    # ── FPGA firmware ──────────────────────────────────────────────────────────

    def _load_fpga(self):
        with self._lock:
            if self._send(CMD.QUERY_FPGA, 0) == 1:
                log.info("FPGA firmware already loaded.")
                return

            pattern = os.path.join(self._firmware_dir, f'VDS1022_FPGAV{self._vfpga}_*.bin')
            import glob
            paths = glob.glob(pattern)
            if not paths:
                raise FileNotFoundError(
                    f"FPGA firmware not found: {pattern}\n"
                    f"Download the firmware files from the OWON VDS1022 release package "
                    f"and place them in: {self._firmware_dir}"
                )

            fpath = sorted(paths)[-1]
            with open(fpath, 'rb') as fh:
                dump = fh.read()

            log.info("Loading FPGA firmware: %s", os.path.basename(fpath))
            frame_size = self._send(CMD.LOAD_FPGA, len(dump))
            header_fmt = struct.Struct('<I')
            payload    = frame_size - header_fmt.size
            chunks     = ceil(len(dump) / payload)

            for i, off in enumerate(range(0, len(dump), payload)):
                print(f"\r  FPGA firmware: {i+1}/{chunks}", end='', flush=True)
                pkt = array('B', header_fmt.pack(i) + dump[off: off + payload])
                self._bulk_write(pkt)
                self._bulk_read(self._buf, 5)
                _, idx = struct.unpack_from('<BI', self._buf)
                assert idx == i, f"FPGA frame mismatch: expected {i}, got {idx}"
            print()

    # ── Device initialisation ──────────────────────────────────────────────────

    def _reset_device(self):
        self._stop.clear()
        self._queue.clear()

        self._on          = [False, False]
        self._coupling    = [DC, DC]
        self._volt_range  = [2.0, 2.0]
        self._volt_offset = [0.0, 0.0]
        self._probe       = [10.0, 10.0]
        self._sampling_rate   = None
        self._trigger_pos     = 0.5
        self._sweep_mode      = None
        self._roll_mode       = False
        self._peak_mode       = False

        self._push(CMD.SET_CHL_ON,    0)
        self._push(CMD.SET_PHASEFINE, self._phasefine)
        self._push(CMD.SET_PEAKMODE,  0)
        self._push(CMD.SET_DEEPMEMORY, _ADC_SIZE)
        self._push(CMD.SET_PRE_TRG,   _ADC_SIZE)
        self._push(CMD.SET_SUF_TRG,   0)
        self._push(CMD.SET_MULTI,     0)
        self._push(CMD.SET_TRIGGER,   0)

        for chl in range(2):
            self._push(CMD.SET_TRG_HOLDOFF[chl], 0x8002)
            self._push(CMD.SET_EDGE_LEVEL[chl],  _u16(127, -128))
            self._push(CMD.SET_FREQREF[chl],     20)
            self._push_channel(chl)

        self._push_sampling(250e3, roll=False, peak=False)

        with self._lock:
            self._flush()

    def _start_keepalive(self):
        def run():
            while self._handle:
                clk = self._clock
                if self._stop.wait(3):
                    time.sleep(0.01)
                elif self._clock == clk:
                    try:
                        with self._lock:
                            self._send(CMD.SET_RUNSTOP, 1)
                    except USBError:
                        log.warning("Keepalive lost connection.")
                        self.close()
                        return
        threading.Thread(target=run, daemon=True).start()

    # ── Channel push helper ────────────────────────────────────────────────────

    def _push_channel(self, chl):
        vb      = VOLT_RANGES.index(self._volt_range[chl])
        pos0    = _ADC_RANGE * self._volt_offset[chl]
        atten   = (vb >= _ATTEN_IDX)
        cal_c   = self.calibration[_COMP][chl][vb]
        cal_a   = self.calibration[_AMPL][chl][vb]
        cal_g   = self.calibration[_GAIN][chl][vb]

        zero_arg = _clamp(round(cal_c - pos0 * cal_a / 100), 0, 4095)
        gain_arg = _clamp(cal_g, 0, 4095)

        self._push(CMD.SET_ZERO_OFF[chl],  zero_arg)
        self._push(CMD.SET_VOLT_GAIN[chl], gain_arg)

        chl_arg = (atten << 1) | (self._coupling[chl] << 5) | (self._on[chl] << 7)
        self._push(CMD.SET_CHANNEL[chl], chl_arg)

    # ── Sampling push helper ───────────────────────────────────────────────────

    def _push_sampling(self, rate, roll, peak):
        prescaler = max(1, round(SAMPLING_RATES[-1] / max(3, rate)))
        sr        = SAMPLING_RATES[-1] / prescaler
        rm        = (sr < _ROLL_THRESH) if roll is None else bool(roll)

        if sr != self._sampling_rate:
            self._sampling_rate = sr
            self._push(CMD.SET_TIMEBASE, prescaler)

        if rm != self._roll_mode:
            self._roll_mode = rm
            self._push(CMD.SET_ROLLMODE, int(rm))
            self._push(CMD.SET_DEEPMEMORY, _ADC_SIZE + (3 if rm else 0))

        if peak is not None and peak != self._peak_mode:
            self._peak_mode = bool(peak)
            self._push(CMD.SET_PEAKMODE, int(peak))

        if rm:
            self._trigger_pos = 1.0

    # ──────────────────────────────────────────────────────────────────────────
    # Public configuration API
    # ──────────────────────────────────────────────────────────────────────────

    def set_channel(self, channel, volt_range=20, offset=0.5, probe=10, coupling=DC):
        """
        Enable and configure a channel.

        Parameters
        ----------
        channel    : CH1 or CH2
        volt_range : float or str  — full-scale voltage at probe tip, e.g. '10v' or 10
        offset     : float         — vertical centre position as fraction [0..1]
                                     0 = top, 0.5 = centre, 1 = bottom
        probe      : float or str  — probe ratio, e.g. 10, 'x10', '10x'
        coupling   : DC, AC or GND

        Examples
        --------
        >>> osc.set_channel(CH1, volt_range='20v', probe='x10', coupling=DC)
        >>> osc.set_channel(CH2, volt_range='5v',  probe=1,     coupling=AC, offset=0.5)
        """
        chl      = _parse_const(channel) if isinstance(channel, str) else int(channel)
        coup     = _parse_const(coupling) if isinstance(coupling, str) else int(coupling)
        vr_ask   = _parse_volts(volt_range)
        offs     = _parse_ratio(offset)  if isinstance(offset, str) else float(offset)
        pb       = _parse_probe(probe)   if isinstance(probe,  str) else float(probe)

        assert chl in (CH1, CH2), f"Invalid channel: {channel}"
        assert 0 <= offs <= 1,    f"Offset must be 0..1, got {offset}"
        assert pb >= 1,            f"Probe ratio must be ≥ 1, got {probe}"

        raw_vr  = round(vr_ask / pb, 4)
        idx     = _find_ge(VOLT_RANGES, raw_vr)
        vr_new  = VOLT_RANGES[idx]
        if abs(vr_new - raw_vr) > 1e-9:
            print(f"Note: {vr_ask}V range → using {vr_new * pb:.4g}V (nearest available)")

        self._on[chl]          = True
        self._coupling[chl]    = coup
        self._volt_range[chl]  = vr_new
        self._volt_offset[chl] = offs - 0.5
        self._probe[chl]       = pb
        self._push_channel(chl)

    def set_sampling(self, rate, roll=None, peak=False):
        """
        Set the sampling rate.

        Parameters
        ----------
        rate : float or str  — samples per second, e.g. 1e6, '100k', '1M'
        roll : bool          — roll (slow-move) mode. Auto-set below 2500 S/s if None.
        peak : bool          — peak detection mode (captures narrow glitches)
        """
        r = _parse_freq(rate) if isinstance(rate, str) else float(rate)
        assert SAMPLING_RATES[0] <= r <= SAMPLING_RATES[-1], \
               f"Sampling rate out of range: {r}"
        self._push_sampling(r, roll, peak)

    def set_timerange(self, duration, roll=None, peak=False):
        """
        Set the sampling rate so that 5000 samples span the given duration.

        Parameters
        ----------
        duration : float or str — time span, e.g. '20ms', 0.02
        roll     : bool
        peak     : bool

        Examples
        --------
        >>> osc.set_timerange('100ms')   # 5000 samples over 100ms → 50 kS/s
        >>> osc.set_timerange('2us')     # 5000 samples over 2µs → 2.5 GS/s (clipped)
        """
        t = _parse_seconds(duration) if isinstance(duration, str) else float(duration)
        r = _SAMPLES / t
        idx = _find_le(SAMPLING_RATES, r)
        self._push_sampling(SAMPLING_RATES[idx], roll, peak)

    def set_trigger(self,
                    source,
                    mode=EDGE,
                    condition=RISE,
                    position=0.5,
                    level=0,
                    width=30e-9,
                    holdoff=100e-9,
                    sweep=ONCE):
        """
        Configure the trigger.

        Parameters
        ----------
        source    : CH1, CH2 or EXT
        mode      : EDGE, PULSE or SLOPE
        condition : RISE / FALL  (EDGE)
                    RISE_SUP / RISE_EQU / RISE_INF / FALL_SUP / FALL_EQU / FALL_INF
                    (PULSE / SLOPE)
        position  : float — trigger position fraction [0..1], 0.5 = centre
        level     : float or str — trigger level in volts, e.g. '2.5v'
                    For SLOPE: pass a (lo, hi) tuple
        width     : float or str — pulse/slope width, e.g. '2ms', 2e-3
        holdoff   : float or str — minimum time between triggers, e.g. '100ns'
        sweep     : AUTO, NORMAL or ONCE

        Examples
        --------
        >>> osc.set_trigger(CH1, EDGE, RISE, position=0.5, level='2v')
        >>> osc.set_trigger(CH1, PULSE, RISE_SUP, level='1v', width='500us')
        >>> osc.set_trigger(CH1, SLOPE, RISE_SUP, level=('0.5v', '3v'), width='1ms')
        """
        chl    = _parse_const(source)   if isinstance(source,    str) else int(source)
        mode   = _parse_const(mode)     if isinstance(mode,      str) else int(mode)
        cond   = _parse_const(condition)if isinstance(condition, str) else int(condition)
        pos    = _parse_ratio(position) if isinstance(position,  str) else float(position)
        sw     = _parse_const(sweep)    if isinstance(sweep,     str) else int(sweep)
        wid    = _parse_seconds(width)  if isinstance(width,     str) else float(width)
        hld    = _parse_seconds(holdoff)if isinstance(holdoff,   str) else float(holdoff)

        levels = [_parse_volts(v) for v in (level if isinstance(level, (tuple, list)) else (level,))]
        levels = [_parse_volts(l) if isinstance(l, str) else float(l) for l in levels]

        self._sweep_mode  = sw
        self._trigger_pos = pos

        alt = (chl != EXT
               and bool(self._queue)
               and next(reversed(self._queue)) is CMD.SET_TRIGGER)

        self._push(CMD.SET_MULTI, (_MULTI_OUT, _MULTI_IN)[chl == EXT])

        htp = round(_SAMPLES * _clamp(0.5 - pos, -0.5, 0.5))
        self._push(CMD.SET_PRE_TRG, (_ADC_SIZE >> 1) - htp - _HTP_ERR)
        self._push(CMD.SET_SUF_TRG, (_ADC_SIZE >> 1) + htp + _HTP_ERR)

        if chl != EXT:
            vr   = self._probe[chl] * self._volt_range[chl]
            lvls = [round((v / vr + self._volt_offset[chl]) * _ADC_RANGE) for v in levels]

            if mode in (EDGE, PULSE):
                assert len(lvls) == 1
                v = lvls[0] + (10 if cond < 0 else 0)
                assert _ADC_MIN + 10 <= v <= _ADC_MAX, f"Trigger level out of range: {levels[0]}"
                self._push(CMD.SET_EDGE_LEVEL[chl], _u16(v, v - 10))
                self._push(CMD.SET_FREQREF[chl],    _u8(v - 5))

            elif mode == SLOPE:
                assert len(lvls) == 2, "SLOPE mode requires two levels: (lo, hi)"
                self._push(CMD.SET_SLOPE_THRED[chl], _u16(max(lvls), min(lvls)))
                self._push(CMD.SET_FREQREF[chl],     _u8(sum(lvls) // 2))

            if mode in (PULSE, SLOPE):
                if self._vfpga < 3:
                    m, e = _iexp10(wid * 1e8, 1023)
                    if cond in (RISE_EQU, FALL_EQU):
                        self._push(CMD.SET_TRG_CDT_EQU_H[chl], int(m * 1.05) << 6 | (e & 7))
                        self._push(CMD.SET_TRG_CDT_EQU_L[chl], int(m * 0.95))
                    else:
                        self._push(CMD.SET_TRG_CDT_GL[chl], m)
                        self._push(CMD.SET_TRG_CDT_EQU_H[chl], e)
                else:
                    m = wid * 1e8
                    self._push(CMD.SET_TRG_CDT_GL[chl], int(m % 65536))
                    self._push(CMD.SET_TRG_CDT_HL[chl], int(m // 65536))

        m, e = _iexp10(hld * 1e8, 1023)
        self._push(CMD.SET_TRG_HOLDOFF[chl % 2], _swap16(m << 6 | (e & 7)))

        trg = int(chl == EXT) | (int(alt) << 15)
        if alt:
            trg |= (chl & 1) << 14 | (mode & 2) << 7 | (mode & 1) << 13
        else:
            trg |= (chl & 1) << 13 | (mode & 2) << 13 | (mode & 1) << 8

        if mode == EDGE:
            trg |= (cond < 0) << 12 | (not alt and sw & 3) << 10
        elif mode in (PULSE, SLOPE):
            trg |= (cond & 7) << 5 | (not alt and sw & 3) << 10

        self._push(CMD.SET_TRIGGER, trg)

    def disable_channel(self, channel):
        """Disable a channel."""
        chl = int(channel)
        self._on[chl] = False
        self._push_channel(chl)

    def force_trigger(self):
        """Force an immediate trigger."""
        with self._lock:
            self._send(CMD.SET_FORCETRG, 0x3)

    # ──────────────────────────────────────────────────────────────────────────
    # Data acquisition
    # ──────────────────────────────────────────────────────────────────────────

    def fetch(self, autorange=False, timeout=5.0):
        """
        Acquire one frame from all enabled channels.

        Parameters
        ----------
        autorange : bool  — auto-adjust volt range if signal clips or is tiny
        timeout   : float — seconds to wait for trigger

        Returns
        -------
        Frames
        """
        return next(self._fetch_iter(freq=None, autorange=autorange,
                                     autosense=False, timeout=timeout))

    def fetch_iter(self, freq=3, autorange=False, autosense=False):
        """
        Generator that continuously yields Frames at approximately `freq` Hz.

        Parameters
        ----------
        freq      : float — target yield rate in Hz (None = as fast as possible)
        autorange : bool  — auto-adjust volt range
        autosense : bool  — auto-adjust trigger to 50% of signal

        Yields
        ------
        Frames
        """
        yield from self._fetch_iter(freq=freq, autorange=autorange,
                                    autosense=autosense, timeout=5.0)

    def _fetch_iter(self, freq, autorange, autosense, timeout):

        with self._lock:
            self._push(CMD.SET_CHL_ON, _bit_mask(self._on))
            self._push(CMD.SET_RUNSTOP, 0)   # run
            self._flush()

        interval = (1.0 / freq) if freq else 0.0

        while not self._stop.is_set():
            t0 = time.perf_counter()

            with self._lock:
                self._flush()

                # Wait for data ready
                deadline = t0 + timeout
                while time.perf_counter() < deadline:
                    on_flags = [self._on[0] and 0x05 or 0x04,
                                self._on[1] and 0x05 or 0x04]
                    arg = on_flags[0] | (on_flags[1] << 8)
                    # Send GET_DATA
                    self._bulk_write(CMD.GET_DATA.pack(arg))
                    n = self._bulk_read(self._buf, None)

                    if n == 5 and self._buf[0] == ord('E'):
                        # Not ready yet
                        time.sleep(0.01)
                        continue

                    # Data available
                    break
                else:
                    if self._sweep_mode == ONCE:
                        # Force trigger on timeout
                        self._send(CMD.SET_FORCETRG, 0x3)
                    continue

                frames = self._parse_frames(n)

            if frames is None:
                continue

            if autorange:
                self._do_autorange(frames)

            if autosense:
                self._do_autosense(frames)

            yield frames

            if self._sweep_mode == ONCE:
                return

            elapsed = time.perf_counter() - t0
            if interval > elapsed:
                time.sleep(interval - elapsed)

    def _parse_frames(self, n):
        """Parse raw USB frame buffer into Frames object."""
        buf = bytes(self._buf)

        ch1_raw = None
        ch2_raw = None
        freq1 = freq2 = None

        # Parse however many 5211-byte channel frames arrived
        # The device sends CH1 first if both are on
        pos = 0
        while pos + _FRAME_SIZE <= n:
            chl_byte = buf[pos]
            time_sum, = struct.unpack_from('<I', buf, pos + 1)
            period_num, = struct.unpack_from('<I', buf, pos + 5)
            # ADC data starts at pos + 111 (after 11-byte header + 100 trigger buf)
            adc_start = pos + 111
            adc_end   = adc_start + _ADC_SIZE
            adc_buf   = buf[adc_start:adc_end]

            # Frequency from hardware meter
            freq = (time_sum / period_num / SAMPLING_RATES[-1]
                    if period_num > 1 else None)

            if chl_byte == 0:
                ch1_raw = (adc_buf, freq)
            else:
                ch2_raw = (adc_buf, freq)

            pos += _FRAME_SIZE

        ch1 = None
        ch2 = None

        if ch1_raw and self._on[0]:
            adc, fr = ch1_raw
            ch1 = Frame(CH1, self._volt_range[0], self._probe[0],
                        self._volt_offset[0], self._sampling_rate,
                        self._trigger_pos, adc[-_SAMPLES:], fr)

        if ch2_raw and self._on[1]:
            adc, fr = ch2_raw
            ch2 = Frame(CH2, self._volt_range[1], self._probe[1],
                        self._volt_offset[1], self._sampling_rate,
                        self._trigger_pos, adc[-_SAMPLES:], fr)

        if ch1 is None and ch2 is None:
            return None

        return Frames(ch1=ch1, ch2=ch2)

    # ── Auto-range / auto-sense helpers ────────────────────────────────────────

    def _do_autorange(self, frames):
        for frame in frames:
            chl = frame.channel
            pts = frame._pts
            lo, hi = float(pts.min()), float(pts.max())
            amp = max(abs(lo), abs(hi)) * 2

            vb  = VOLT_RANGES.index(self._volt_range[chl])

            if hi >= _ADC_MAX or lo <= _ADC_MIN:
                vb_new = min(vb + 1, len(VOLT_RANGES) - 1)
            elif amp < 16:
                continue
            else:
                vr_need = amp * 1.1 * self._volt_range[chl] / _ADC_RANGE
                vb_new  = _find_ge(VOLT_RANGES, vr_need)

            if vb_new != vb:
                self._volt_range[chl] = VOLT_RANGES[vb_new]
                self._push_channel(chl)
                with self._lock:
                    self._flush()

    def _do_autosense(self, frames):
        for frame in frames:
            chl = frame.channel
            pts = frame._pts
            centre = round((float(pts.max()) + float(pts.min())) / 2)
            v = _clamp(centre + 10, _ADC_MIN + 10, _ADC_MAX)
            self._push(CMD.SET_EDGE_LEVEL[chl], _u16(v, v - 10))
            self._push(CMD.SET_FREQREF[chl],    _u8(v - 5))

    # ──────────────────────────────────────────────────────────────────────────
    # Convenience measurements
    # ──────────────────────────────────────────────────────────────────────────

    def measure(self, channel=CH1):
        """
        Fetch one frame and return a measurement summary dict.

        Parameters
        ----------
        channel : CH1 or CH2

        Returns
        -------
        dict
        """
        chl = int(channel)
        assert self._on[chl], f"CH{chl+1} is not enabled. Call set_channel() first."
        frames = self.fetch()
        return frames[chl].describe()

    def rms(self, channel=CH1):
        """Return RMS voltage from a single fetch."""
        return self.fetch()[channel].rms()

    def freq_measure(self, channel=CH1):
        """Return (frequency_Hz, phase_deg) from a single fetch."""
        return self.fetch()[channel].freq()

    # ──────────────────────────────────────────────────────────────────────────
    # Auto-set
    # ──────────────────────────────────────────────────────────────────────────

    def autoset(self):
        """
        Automatically find the optimal volt range and time base.
        Equivalent to pressing AUTO on the front panel.

        Returns
        -------
        self  (for chaining)
        """
        log.info("Running autoset…")

        with self._lock:
            self._on[:] = [True, True]
            self._sweep_mode = AUTO
            self._trigger_pos = 0.5

            self._push_sampling(25000, roll=False, peak=False)
            self._push(CMD.SET_PEAKMODE, 1)
            self._push(CMD.SET_MULTI, 0)
            self._push(CMD.SET_PRE_TRG, (_ADC_SIZE >> 1) - _HTP_ERR)
            self._push(CMD.SET_SUF_TRG, (_ADC_SIZE >> 1) + _HTP_ERR)
            self._push(CMD.SET_TRIGGER, 0xC000)

            for chl in range(2):
                self._volt_offset[chl] = 0
                self._push(CMD.SET_TRG_HOLDOFF[chl], 0x8002)
                self._push(CMD.SET_EDGE_LEVEL[chl],  _u16(20, 10))
                self._push(CMD.SET_FREQREF[chl],     _u8(12))
                self._push_channel(chl)

            self._flush()

        # Iterate to converge
        hits = 0
        rate = SAMPLING_RATES[-1]
        on   = [True, True]

        for _ in range(10):
            if hits >= sum(on):
                break

            time.sleep(0.2)
            frames = self.fetch(autorange=False)

            for frame in frames:
                chl = frame.channel
                pts = frame._pts
                lo, hi = float(pts.min()), float(pts.max())
                amp = max(abs(lo), abs(hi)) * 2

                vb = VOLT_RANGES.index(self._volt_range[chl])

                if hi >= _ADC_MAX or lo <= _ADC_MIN:
                    vb_new = (vb + len(VOLT_RANGES)) >> 1
                elif amp < 16:
                    on[chl] = False
                    continue
                else:
                    vb_new = _find_ge(VOLT_RANGES, amp * 1.1 * self._volt_range[chl] / _ADC_RANGE)

                if vb_new == vb:
                    hits += 1
                else:
                    hits = 0
                    self._volt_range[chl] = VOLT_RANGES[vb_new]
                    self._push_channel(chl)

                if frame.frequency and frame.frequency > 0 and amp > 20:
                    r_new = SAMPLING_RATES[_find_le(SAMPLING_RATES,
                                                    _SAMPLES / (frame.frequency * 3))]
                    if r_new != self._sampling_rate and r_new < rate:
                        self._push_sampling(r_new, False, None)
                        rate = r_new
                        hits = 0

            with self._lock:
                self._flush()

        with self._lock:
            self._push(CMD.SET_PEAKMODE, 0)
            self._flush()

        return self

    # ──────────────────────────────────────────────────────────────────────────
    # Live monitoring
    # ──────────────────────────────────────────────────────────────────────────

    def monitor(self, channel=CH1, measurement='rms', freq=2, duration=None):
        """
        Print live measurements to the terminal.

        Parameters
        ----------
        channel     : CH1 or CH2
        measurement : str — one of 'rms', 'avg', 'freq', 'vpp', 'max', 'min'
        freq        : float — updates per second
        duration    : float — seconds to run (None = run until Ctrl+C)

        Examples
        --------
        >>> osc.monitor(CH1, 'rms', freq=4)
        """
        chl = int(channel)
        fn_map = {
            'rms' : Frame.rms,
            'avg' : Frame.avg,
            'vpp' : Frame.vpp,
            'max' : Frame.max,
            'min' : Frame.min,
            'freq': lambda f: f.freq()[0],
            'std' : Frame.std,
        }
        assert measurement in fn_map, f"Unknown measurement: {measurement}. Choose: {list(fn_map)}"
        fn    = fn_map[measurement]
        t_end = time.time() + duration if duration else None

        print(f"Monitoring CH{chl+1} {measurement.upper()} at {freq} Hz "
              f"({'∞' if not duration else str(duration)+'s'}). Ctrl+C to stop.\n")

        try:
            for frames in self.fetch_iter(freq=freq, autorange=False):
                f = frames[chl]
                if f is None:
                    continue
                val = fn(f)
                ts  = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                print(f"\r  [{ts}]  {measurement.upper()}: {val!s:>12}", end='', flush=True)
                if t_end and time.time() >= t_end:
                    break
        except KeyboardInterrupt:
            pass
        print()

    def log_to_csv(self, filepath, channel=CH1, measurements=('rms', 'avg', 'freq'),
                   freq=1, duration=None):
        """
        Continuously log measurements to a CSV file.

        Parameters
        ----------
        filepath     : str
        channel      : CH1 or CH2
        measurements : tuple of measurement names
        freq         : float — samples per second
        duration     : float — seconds to run (None = Ctrl+C to stop)

        Examples
        --------
        >>> osc.log_to_csv('log.csv', CH1, ('rms', 'avg', 'vpp'), freq=2, duration=60)
        """
        chl = int(channel)
        fn_map = {
            'rms' : Frame.rms,
            'avg' : Frame.avg,
            'vpp' : Frame.vpp,
            'max' : Frame.max,
            'min' : Frame.min,
            'freq': lambda f: f.freq()[0],
            'std' : Frame.std,
            'amp' : Frame.amp,
        }
        fns = {m: fn_map[m] for m in measurements}

        t_end = time.time() + duration if duration else None

        with open(filepath, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(['timestamp', 'elapsed_s'] + list(measurements))
            t_start = time.time()
            try:
                for frames in self.fetch_iter(freq=freq, autorange=False):
                    f = frames[chl]
                    if f is None:
                        continue
                    now  = time.time()
                    row  = [datetime.datetime.now().isoformat(),
                            round(now - t_start, 3)]
                    row += [fn(f) for fn in fns.values()]
                    w.writerow(row)
                    fh.flush()
                    print(f"\r  Logged {row[1]:.1f}s", end='', flush=True)
                    if t_end and now >= t_end:
                        break
            except KeyboardInterrupt:
                pass

        print(f"\nLog saved to {filepath}")

    # ──────────────────────────────────────────────────────────────────────────
    # Info & utilities
    # ──────────────────────────────────────────────────────────────────────────

    def info(self):
        """Print device information."""
        print(f"  Device   : OWON {self.version}")
        print(f"  Serial   : {self.serial}")
        print(f"  FPGA     : v{self._vfpga}")
        print(f"  Sampling : {self._sampling_rate:.4g} S/s")
        for chl in range(2):
            state = 'ON' if self._on[chl] else 'OFF'
            if self._on[chl]:
                vr = self._volt_range[chl] * self._probe[chl]
                print(f"  CH{chl+1}      : {state}  {vr:.4g}V range  "
                      f"x{self._probe[chl]:.0f} probe  "
                      f"{'AC' if self._coupling[chl]==AC else 'DC'}")
            else:
                print(f"  CH{chl+1}      : {state}")

    def stop(self):
        """Stop acquisition."""
        if self._handle:
            self._stop.set()
            with self._lock:
                self._queue.clear()
                try:
                    self._send(CMD.SET_RUNSTOP, 1)
                    self._stop.clear()
                    return True
                except USBError:
                    pass
            self._release()

    def close(self):
        """Disconnect and release USB resources."""
        self._stop.set()
        with self._lock:
            self._queue.clear()
            self._release()
        log.info("Disconnected.")

    def __repr__(self):
        return (f"Oscilloscope(serial={self.serial!r}, "
                f"version={self.version!r}, "
                f"sampling={self._sampling_rate:.4g}S/s)")


# ──────────────────────────────────────────────────────────────────────────────
# CLI quick-test
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='OWON VDS1022 quick measurement')
    parser.add_argument('--channel',     default='CH1', choices=['CH1', 'CH2'])
    parser.add_argument('--range',       default='10v',  help='Volt range, e.g. 10v')
    parser.add_argument('--probe',       default='x10',  help='Probe ratio, e.g. x10')
    parser.add_argument('--coupling',    default='DC',   choices=['DC', 'AC'])
    parser.add_argument('--timerange',   default='20ms', help='Time range, e.g. 20ms')
    parser.add_argument('--plot',        action='store_true', help='Show waveform plot')
    parser.add_argument('--csv',         default='',     help='Save samples to CSV file')
    parser.add_argument('--monitor',     action='store_true', help='Live RMS monitoring')
    parser.add_argument('--firmware-dir',default='',     help='FPGA firmware directory')
    args = parser.parse_args()

    chl  = CH1 if args.channel == 'CH1' else CH2
    coup = DC  if args.coupling == 'DC' else AC

    print("Connecting to OWON VDS1022…")
    with Oscilloscope(firmware_dir=args.firmware_dir or None) as osc:
        osc.info()
        osc.set_channel(chl, volt_range=args.range, probe=args.probe, coupling=coup)
        osc.set_timerange(args.timerange)
        osc.set_trigger(chl, EDGE, RISE, position=0.5, level='0v', sweep=AUTO)

        if args.monitor:
            osc.monitor(chl, 'rms', freq=4)
        else:
            print("Fetching frame…")
            frames = osc.fetch()
            frame  = frames[chl]

            d = frame.describe()
            print("\nMeasurements:")
            for k, v in d.items():
                print(f"  {k:12s}: {v}")

            if args.csv:
                frame.to_csv(args.csv)
                print(f"\nSaved to {args.csv}")

            if args.plot:
                frames.plot()
