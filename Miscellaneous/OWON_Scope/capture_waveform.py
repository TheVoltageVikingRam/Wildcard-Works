#!/usr/bin/env python3
"""
capture_waveform.py — Capture the current waveform from an OWON VDS1022
                      oscilloscope, plot it, and export as JPG.

Usage:
    python capture_waveform.py
    python capture_waveform.py --channel CH2 --range 5v --timerange 10ms
    python capture_waveform.py --output my_capture.jpg --dpi 200
    python capture_waveform.py --both           # capture both CH1 & CH2

Dependencies:
    pip install pyusb numpy matplotlib pillow
"""

import argparse
import datetime
import os
import sys

# Ensure this script can import from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from owon_vds import (
    Oscilloscope, Frame, Frames,
    CH1, CH2, DC, AC,
    EDGE, RISE, AUTO, ONCE,
)


def make_plot(frames, output_path, dpi=150, dark=True):
    """
    Create a polished oscilloscope-style waveform plot and save as JPG.

    Parameters
    ----------
    frames     : Frames object from the oscilloscope
    output_path: str — output file path (e.g. 'waveform.jpg')
    dpi        : int — resolution
    dark       : bool — use dark oscilloscope theme
    """
    import matplotlib
    matplotlib.use('Agg')  # non-interactive backend for saving
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import numpy as np

    active = list(frames)
    n = len(active)
    if n == 0:
        print("ERROR: No channel data captured.")
        return

    # ── Theme ──────────────────────────────────────────────────────────────
    if dark:
        plt.style.use('dark_background')
        bg_color    = '#1a1a2e'
        grid_color  = '#2d3561'
        text_color  = '#e0e0e0'
        ch_colors   = ['#00d4ff', '#ff6b35']   # cyan for CH1, orange for CH2
        border_color = '#3a3a5c'
    else:
        bg_color    = '#f5f5f0'
        grid_color  = '#cccccc'
        text_color  = '#333333'
        ch_colors   = ['#1565c0', '#e65100']
        border_color = '#999999'

    fig_height = 4 * n + 1.5
    fig, axes = plt.subplots(n, 1, figsize=(14, fig_height),
                             sharex=True, squeeze=False)
    axes = axes.flatten()
    fig.patch.set_facecolor(bg_color)

    # ── Time formatter ─────────────────────────────────────────────────────
    ref_sx = active[0].sx

    def fmt_time(x, _):
        if ref_sx < 1e-6:
            return f'{x * 1e9:.1f} ns'
        elif ref_sx < 1e-3:
            return f'{x * 1e6:.1f} µs'
        elif ref_sx < 1:
            return f'{x * 1e3:.2f} ms'
        else:
            return f'{x:.3f} s'

    # ── Plot each channel ──────────────────────────────────────────────────
    for i, (ax, frame) in enumerate(zip(axes, active)):
        xs = frame.x()
        ys = frame.y()
        color = ch_colors[frame.channel]

        ax.set_facecolor(bg_color)
        ax.plot(xs, ys, color=color, linewidth=0.9, alpha=0.95,
                label=frame.name, zorder=3)

        # Subtle fill under the curve
        ax.fill_between(xs, ys, alpha=0.08, color=color, zorder=2)

        # Grid — oscilloscope style
        ax.grid(True, which='major', color=grid_color, linewidth=0.6, alpha=0.7)
        ax.grid(True, which='minor', color=grid_color, linewidth=0.3, alpha=0.3)
        ax.minorticks_on()

        # Trigger line at 0V
        ax.axhline(0, color=grid_color, linewidth=0.8, linestyle='--', alpha=0.5)
        # Trigger position vertical line
        ax.axvline(0, color='#ff4444', linewidth=0.8, linestyle='--', alpha=0.4,
                   label='Trigger')

        # Axis limits
        ax.set_xlim(xs[0], xs[-1])
        ax.set_ylim(*frame.ylim)

        # Labels
        ax.set_ylabel('Voltage (V)', color=text_color, fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(
            lambda v, _: f'{v:.3g} V'))

        # Measurements annotation box
        freq_hz, phase = frame.freq()
        freq_str = f'{freq_hz:.4g} Hz' if freq_hz else 'N/A'
        period_str = f'{1/freq_hz*1e3:.4g} ms' if freq_hz else 'N/A'

        info_text = (
            f'{frame.name}\n'
            f'Vpp: {frame.vpp():.4g} V\n'
            f'Vrms: {frame.rms():.4g} V\n'
            f'Vavg: {frame.avg():.4g} V\n'
            f'Freq: {freq_str}\n'
            f'Period: {period_str}'
        )
        props = dict(boxstyle='round,pad=0.5', facecolor=bg_color,
                     edgecolor=color, alpha=0.85, linewidth=1.5)
        ax.text(0.98, 0.95, info_text, transform=ax.transAxes,
                fontsize=8, verticalalignment='top', horizontalalignment='right',
                color=text_color, fontfamily='monospace', bbox=props, zorder=5)

        # Legend
        leg = ax.legend(loc='upper left', fontsize=9, framealpha=0.6,
                        edgecolor=border_color)
        for text in leg.get_texts():
            text.set_color(text_color)

        # Spine styling
        for spine in ax.spines.values():
            spine.set_color(border_color)
            spine.set_linewidth(0.8)
        ax.tick_params(colors=text_color, labelsize=8)

    # X-axis on bottom subplot
    axes[-1].set_xlabel('Time', color=text_color, fontsize=10)
    axes[-1].xaxis.set_major_formatter(mticker.FuncFormatter(fmt_time))

    # ── Title ──────────────────────────────────────────────────────────────
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    sr = active[0].sx and 1 / active[0].sx
    sr_str = f'{sr:.4g} S/s' if sr else ''
    title = f'OWON VDS1022  —  {sr_str}  —  {timestamp}'
    fig.suptitle(title, color=text_color, fontsize=12, fontweight='bold', y=0.98)

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    # ── Save ───────────────────────────────────────────────────────────────
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none',
                format='jpg', pil_kwargs={'quality': 95})
    plt.close(fig)
    print(f"\n[OK] Waveform saved to: {os.path.abspath(output_path)}")
    print(f"  Resolution: {dpi} DPI")
    print(f"  Channels: {', '.join(f.name for f in active)}")


def main():
    parser = argparse.ArgumentParser(
        description='Capture waveform from OWON VDS1022 and export as JPG')

    parser.add_argument('--channel', default='CH1', choices=['CH1', 'CH2'],
                        help='Channel to capture (default: CH1)')
    parser.add_argument('--single', action='store_true',
                        help='Capture only the specified channel (default: both)')
    parser.add_argument('--range', default='20v', dest='volt_range',
                        help='Voltage range (default: 20v)')
    parser.add_argument('--probe', default='x10',
                        help='Probe ratio (default: x10)')
    parser.add_argument('--coupling', default='DC', choices=['DC', 'AC'],
                        help='Coupling mode (default: DC)')
    parser.add_argument('--timerange', default='20ms',
                        help='Time range (default: 20ms)')
    parser.add_argument('--output', '-o', default='waveform.jpg',
                        help='Output JPG file path (default: waveform.jpg)')
    parser.add_argument('--dpi', type=int, default=150,
                        help='Output resolution in DPI (default: 150)')
    parser.add_argument('--autoset', action='store_true',
                        help='Run autoset before capturing')
    parser.add_argument('--trigger-level', default='0v',
                        help='Trigger level (default: 0v)')
    parser.add_argument('--sweep', default='AUTO',
                        choices=['AUTO', 'NORMAL', 'ONCE'],
                        help='Sweep mode (default: AUTO)')
    parser.add_argument('--light', action='store_true',
                        help='Use light theme instead of dark')
    parser.add_argument('--firmware-dir', default='',
                        help='FPGA firmware directory')
    parser.add_argument('--csv', default='',
                        help='Also save raw data to CSV')

    args = parser.parse_args()

    chl  = CH1 if args.channel == 'CH1' else CH2
    coup = DC if args.coupling == 'DC' else AC
    sweep_map = {'AUTO': AUTO, 'NORMAL': 1, 'ONCE': ONCE}
    sweep = sweep_map[args.sweep]
    capture_both = not args.single

    print("=" * 60)
    print("  OWON VDS1022 -- Waveform Capture")
    print("=" * 60)
    ch_label = 'CH1 + CH2' if capture_both else args.channel
    print(f"  Channel    : {ch_label}")
    print(f"  Range      : {args.volt_range}")
    print(f"  Probe      : {args.probe}")
    print(f"  Coupling   : {args.coupling}")
    print(f"  Time range : {args.timerange}")
    print(f"  Output     : {args.output}")
    print(f"  DPI        : {args.dpi}")
    print("=" * 60)

    print("\nConnecting to OWON VDS1022...")
    fw_dir = args.firmware_dir or None

    with Oscilloscope(firmware_dir=fw_dir) as osc:
        osc.info()

        if args.autoset:
            print("\nRunning autoset...")
            osc.autoset()
        else:
            # Configure primary channel
            osc.set_channel(chl, volt_range=args.volt_range,
                            probe=args.probe, coupling=coup)

            # Configure second channel (default: both)
            if capture_both:
                other = CH2 if chl == CH1 else CH1
                osc.set_channel(other, volt_range=args.volt_range,
                                probe=args.probe, coupling=coup)

            osc.set_timerange(args.timerange)
            osc.set_trigger(chl, EDGE, RISE, position=0.5,
                            level=args.trigger_level, sweep=sweep)

        # Allow the device to settle after channel configuration
        import time as _time
        _time.sleep(0.5)

        # Fetch with retry — first fetch after enabling channels may
        # only return one channel; a second attempt usually gets both.
        print("\nFetching waveform...")
        frames = None
        for attempt in range(3):
            frames = osc.fetch()
            active = list(frames)
            got_both = len(active) >= 2
            if not capture_both or got_both:
                break
            print(f"  Retry {attempt+1}: got {len(active)} channel(s), expecting 2...")
            _time.sleep(0.3)

        # Print measurements
        for frame in frames:
            d = frame.describe()
            print(f"\n  {frame.name} Measurements:")
            for k, v in d.items():
                if k != 'Channel':
                    print(f"    {k:12s}: {v}")

        # Save CSV if requested
        if args.csv:
            frames.to_csv(args.csv)
            print(f"\n  Raw data saved to: {args.csv}")

        # Plot and export JPG
        print(f"\nGenerating plot…")
        make_plot(frames, args.output, dpi=args.dpi, dark=not args.light)

    print("\nDone!")


if __name__ == '__main__':
    main()
