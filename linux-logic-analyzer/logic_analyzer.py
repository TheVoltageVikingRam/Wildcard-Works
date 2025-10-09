#!/usr/bin/env python3
"""
Enhanced Logic Analyzer for Raspberry Pi 5
Uses libgpiod (gpiod) for modern GPIO access
Supports up to 8 channels with improved performance
"""

import gpiod
import time
import sys
import argparse
import signal
from collections import deque
from datetime import datetime

class LogicAnalyzer:
    def __init__(self, pins, labels=None, trig_chan=0, trig_edge='rising', 
                 trig_mode='auto', width=80, rate=0.001, chip='/dev/gpiochip4'):
        """
        Initialize Logic Analyzer
        
        Args:
            pins: List of GPIO pin numbers (BCM numbering)
            labels: Optional list of channel labels
            trig_chan: Channel index to use for trigger (0-based)
            trig_edge: 'rising', 'falling', or 'both'
            trig_mode: 'auto' or 'normal'
            width: Display width in characters
            rate: Sampling period in seconds
            chip: GPIO chip device (Pi 5 uses gpiochip4)
        """
        self.pins = pins
        self.num_channels = len(pins)
        self.labels = labels or [f"GPIO-{p}" for p in pins]
        self.trig_chan = min(trig_chan, self.num_channels - 1)
        self.trig_edge = trig_edge
        self.trig_mode = trig_mode
        self.width = width
        self.rate = rate
        self.chip_path = chip
        
        self.running = True
        self.chip = None
        self.lines = None
        self.buffer = [deque(maxlen=width) for _ in range(self.num_channels)]
        self.last_trigger_state = 0
        
        # Statistics
        self.samples_captured = 0
        self.triggers_detected = 0
        
    def setup_gpio(self):
        """Initialize GPIO lines using libgpiod"""
        try:
            self.chip = gpiod.Chip(self.chip_path)
            self.lines = self.chip.get_lines(self.pins)
            self.lines.request(consumer="logic_analyzer", type=gpiod.LINE_REQ_DIR_IN)
            print(f"✓ GPIO initialized on {self.chip_path}")
            return True
        except Exception as e:
            print(f"✗ GPIO initialization failed: {e}")
            print(f"  Note: Raspberry Pi 5 uses /dev/gpiochip4")
            print(f"  Ensure you have permissions: sudo usermod -a -G gpio $USER")
            return False
    
    def cleanup(self):
        """Release GPIO resources"""
        if self.lines:
            self.lines.release()
        if self.chip:
            self.chip.close()
    
    def check_trigger(self, values):
        """Check if trigger condition is met"""
        if self.trig_mode == 'auto':
            return True
        
        current = values[self.trig_chan]
        triggered = False
        
        if self.trig_edge == 'rising':
            triggered = (self.last_trigger_state == 0 and current == 1)
        elif self.trig_edge == 'falling':
            triggered = (self.last_trigger_state == 1 and current == 0)
        elif self.trig_edge == 'both':
            triggered = (self.last_trigger_state != current)
        
        self.last_trigger_state = current
        
        if triggered:
            self.triggers_detected += 1
        
        return triggered
    
    def read_pins(self):
        """Read all pins simultaneously"""
        return self.lines.get_values()
    
    def draw_waveform(self, value):
        """Return ASCII character for signal level"""
        return '─' if value else '_'
    
    def draw_screen(self):
        """Draw the logic analyzer display"""
        # Clear screen and move cursor to top
        print("\033[2J\033[H", end='')
        
        # Header
        print("╔" + "═" * (self.width + 20) + "╗")
        print("║ \033[1;36mRaspberry Pi 5 Logic Analyzer\033[0m" + " " * (self.width - 9) + "║")
        print("╠" + "═" * (self.width + 20) + "╣")
        print(f"║ Samples: {self.samples_captured:6d}  Triggers: {self.triggers_detected:4d}  Rate: {1/self.rate:.0f} Hz" + " " * (self.width - 38) + "║")
        print("╠" + "═" * (self.width + 20) + "╣")
        
        # Draw each channel
        for i in range(self.num_channels):
            # Channel label with color
            color = 31 + (i % 6)  # Cycle through colors
            label = f"{self.labels[i]:12s}"
            
            # Trigger indicator
            trig_marker = ""
            if i == self.trig_chan and self.trig_mode != 'auto':
                if self.trig_edge == 'rising':
                    trig_marker = "↑"
                elif self.trig_edge == 'falling':
                    trig_marker = "↓"
                else:
                    trig_marker = "↕"
            
            print(f"║ \033[{color}m{label}\033[0m {trig_marker:1s} │ ", end='')
            
            # Draw waveform
            for val in self.buffer[i]:
                print(f"\033[{color}m{self.draw_waveform(val)}\033[0m", end='')
            
            # Fill remaining space
            remaining = self.width - len(self.buffer[i])
            print(" " * remaining + " ║")
        
        print("╚" + "═" * (self.width + 20) + "╝")
        print(f"Mode: {self.trig_mode.upper():6s} | Press Ctrl+C to stop")
        
        sys.stdout.flush()
    
    def run(self):
        """Main acquisition loop"""
        if not self.setup_gpio():
            return
        
        print("\nStarting acquisition...")
        time.sleep(0.5)
        
        triggered = (self.trig_mode == 'auto')
        
        try:
            # Initialize last state for trigger detection
            self.last_trigger_state = self.read_pins()[self.trig_chan]
            
            while self.running:
                # Read all pins
                values = self.read_pins()
                
                # Check trigger condition
                if not triggered:
                    triggered = self.check_trigger(values)
                    if not triggered:
                        time.sleep(self.rate * 0.1)  # Fast polling while waiting
                        continue
                
                # Store samples
                for i, val in enumerate(values):
                    self.buffer[i].append(val)
                
                self.samples_captured += 1
                
                # Update display
                if self.samples_captured % max(1, int(0.1 / self.rate)) == 0:
                    self.draw_screen()
                
                # Reset trigger for normal mode
                if self.trig_mode == 'normal' and len(self.buffer[0]) >= self.width:
                    triggered = False
                    for buf in self.buffer:
                        buf.clear()
                
                time.sleep(self.rate)
                
        except KeyboardInterrupt:
            print("\n\nStopping acquisition...")
        finally:
            self.cleanup()
            print(f"\nCaptured {self.samples_captured} samples")
            print(f"Detected {self.triggers_detected} triggers")

def main():
    parser = argparse.ArgumentParser(
        description='Logic Analyzer for Raspberry Pi 5',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor 3 channels with auto trigger
  %(prog)s --pins 4 3 2 --labels CLK DATA CS
  
  # Trigger on falling edge of channel 0
  %(prog)s --pins 4 3 2 --trig-chan 0 --trig-edge falling --trig-mode normal
  
  # High-speed capture (1000 Hz)
  %(prog)s --pins 17 27 22 --rate 0.001 --width 120
        """
    )
    
    parser.add_argument('--pins', type=int, nargs='+', required=True,
                        help='GPIO pin numbers (BCM numbering)')
    parser.add_argument('--labels', type=str, nargs='+',
                        help='Channel labels (optional)')
    parser.add_argument('--trig-chan', type=int, default=0,
                        help='Trigger channel index (default: 0)')
    parser.add_argument('--trig-edge', choices=['rising', 'falling', 'both'],
                        default='rising', help='Trigger edge type')
    parser.add_argument('--trig-mode', choices=['auto', 'normal'],
                        default='auto', help='Trigger mode')
    parser.add_argument('--width', type=int, default=80,
                        help='Display width in characters')
    parser.add_argument('--rate', type=float, default=0.01,
                        help='Sampling period in seconds (default: 0.01 = 100Hz)')
    parser.add_argument('--chip', type=str, default='/dev/gpiochip4',
                        help='GPIO chip device (default: /dev/gpiochip4 for Pi 5)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if len(args.pins) > 8:
        print("Error: Maximum 8 channels supported")
        sys.exit(1)
    
    if args.labels and len(args.labels) != len(args.pins):
        print("Error: Number of labels must match number of pins")
        sys.exit(1)
    
    if args.trig_chan >= len(args.pins):
        print(f"Error: Trigger channel {args.trig_chan} out of range")
        sys.exit(1)
    
    # Create and run analyzer
    analyzer = LogicAnalyzer(
        pins=args.pins,
        labels=args.labels,
        trig_chan=args.trig_chan,
        trig_edge=args.trig_edge,
        trig_mode=args.trig_mode,
        width=args.width,
        rate=args.rate,
        chip=args.chip
    )
    
    analyzer.run()

if __name__ == '__main__':
    main()
