# Remote Android Control via ADB & Tailscale

Complete guide to control your Android phone remotely from anywhere in the world using ADB and Tailscale.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Enabling Wireless ADB](#enabling-wireless-adb)
- [Connecting Remotely](#connecting-remotely)
- [Screen Mirroring with scrcpy](#screen-mirroring-with-scrcpy)
- [Troubleshooting](#troubleshooting)
- [Useful ADB Commands](#useful-adb-commands)
- [Important Notes](#important-notes)

## 🔧 Prerequisites

### Required Software

1. **ADB (Android Debug Bridge)**
   - Download Platform Tools: https://developer.android.com/studio/releases/platform-tools
   - Extract to a folder (e.g., `C:\platform-tools\`)
   - Add to PATH or run from that directory

2. **Tailscale** (for secure remote access)
   - PC: https://tailscale.com/download
   - Android: Install from Play Store

3. **scrcpy** (for screen mirroring)
   - Download: https://github.com/Genymobile/scrcpy/releases/latest
   - Extract `scrcpy-win64-vX.XX.zip` anywhere
   - Run `scrcpy.exe`

### Phone Setup

1. Enable Developer Options:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Developer Options now appears in Settings

2. Enable USB Debugging:
   - Settings → Developer Options
   - Enable "USB Debugging"

3. **⚠️ IMPORTANT**: Keep Developer Options ON permanently for remote access!

## 🚀 Initial Setup

### Step 1: Install Tailscale on Both Devices

1. Install Tailscale on your PC
2. Install Tailscale on your Android phone
3. Sign in to the same account on both
4. Note down the Tailscale IPs:
   - Open Tailscale app to see IPs
   - IPs start with `100.x.x.x`

Example:
```
PC:    100.68.132.126
Phone: 100.78.106.87
```

### Step 2: Connect Phone via USB

```bash
# Connect phone to PC with USB cable
# Check connection
adb devices
```

You should see:
```
List of devices attached
XXXXXXXXXX    device
```

If you see "unauthorized", check your phone for the authorization prompt.

## 📡 Enabling Wireless ADB

### Method 1: Using ADB Command (Non-Root)

```bash
# Enable TCP mode on port 5555
adb tcpip 5555
```

Output:
```
restarting in TCP mode port: 5555
```

### Method 2: Wireless Debugging (Android 11+)

If the above doesn't work, use built-in Wireless Debugging:

1. Phone: Settings → Developer Options → Wireless debugging
2. Enable "Wireless debugging"
3. Tap "Pair device with pairing code"
4. Note the IP:PORT and pairing code

On PC:
```bash
# Pair first (use IP:PORT from phone)
adb pair 192.168.x.x:xxxxx
# Enter pairing code when prompted

# Connect (use different port shown in Wireless debugging main screen)
adb connect 192.168.x.x:xxxxx
```

## 🌐 Connecting Remotely

### Get Phone's Tailscale IP

**Option A: Check Tailscale App**
- Open Tailscale app on phone
- Note the IP (e.g., `100.78.106.87`)

**Option B: Via ADB**
```bash
adb shell ip addr | grep "100\."
```

### Connect via Tailscale

```bash
# Connect to phone's Tailscale IP
adb connect 100.78.106.87:5555

# Verify connection
adb devices
```

Expected output:
```
List of devices attached
100.78.106.87:5555    device
```

### Disconnect USB Cable

Once connected via Tailscale, **you can unplug the USB cable**!

Test it:
```bash
# Unplug USB, then check
adb devices
# Should still show: 100.78.106.87:5555    device
```

## 🖥️ Screen Mirroring with scrcpy

### Basic Usage

```bash
# Start screen mirroring
scrcpy
```

Your phone screen appears on PC with full mouse/keyboard control!

### Advanced Options

```bash
# Lower resolution for better performance
scrcpy --max-size 1024

# Higher quality
scrcpy --bit-rate 8M

# Turn off phone screen while mirroring
scrcpy --turn-screen-off

# Record while mirroring
scrcpy --record recording.mp4

# Specify device if multiple connected
scrcpy -s 100.78.106.87:5555

# Window always on top
scrcpy --always-on-top

# Borderless window
scrcpy --window-borderless
```

### Keyboard Shortcuts in scrcpy

- `Ctrl+f` - Fullscreen
- `Ctrl+g` - Resize window to 1:1
- `Ctrl+x` - Rotate device left
- `Ctrl+r` - Rotate device right
- `Ctrl+h` - Home button
- `Ctrl+b` - Back button
- `Ctrl+s` - Power button
- `Ctrl+n` - Expand notification panel
- `Ctrl+Shift+n` - Collapse notification panel
- `Ctrl+o` - Turn device screen off
- `Ctrl+Shift+o` - Turn device screen on

## 🔍 Troubleshooting

### Connection Issues

**Problem: "Device not found"**
```bash
# Reconnect
adb connect 100.78.106.87:5555
```

**Problem: "Connection refused"**
- Ensure Tailscale is running on both devices
- Check phone's Developer Options is still enabled
- Restart ADB server:
```bash
adb kill-server
adb start-server
adb connect 100.78.106.87:5555
```

**Problem: Connection keeps dropping**
- Disable battery optimization for Tailscale app on phone
- Keep phone's screen timeout longer
- Ensure stable internet on both devices

### Camera Service High CPU

If camera service is using excessive CPU:

```bash
# Check what's using camera
adb shell dumpsys media.camera

# Kill stuck camera services
adb shell
kill -9 1133 1369
exit
```

### Re-enabling After Developer Options Turned Off

**You MUST physically access the phone:**
1. Settings → About Phone → Tap Build Number 7 times
2. Settings → Developer Options → Enable USB Debugging
3. Connect USB and repeat wireless ADB setup
4. **Keep Developer Options ON!**

## 📱 Useful ADB Commands

### Process Management

```bash
# List running processes
adb shell ps -A

# Top processes (CPU usage)
adb shell top -m 10

# Kill an app
adb shell am force-stop com.package.name
```

### Screenshots & Recording

```bash
# Take screenshot
adb shell screencap /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .

# Record screen (Ctrl+C to stop)
adb shell screenrecord /sdcard/recording.mp4
adb pull /sdcard/recording.mp4 .

# Record with time limit
adb shell screenrecord --time-limit 30 /sdcard/demo.mp4
```

### Input Simulation

```bash
# Tap at coordinates
adb shell input tap 500 1000

# Swipe (x1 y1 x2 y2 duration_ms)
adb shell input swipe 300 1000 300 300 100

# Type text
adb shell input text "Hello"

# Press keys
adb shell input keyevent 3    # Home
adb shell input keyevent 4    # Back
adb shell input keyevent 26   # Power
adb shell input keyevent 24   # Volume up
adb shell input keyevent 25   # Volume down
```

### App Management

```bash
# List installed packages
adb shell pm list packages

# List user-installed apps only
adb shell pm list packages -3

# Install APK
adb install app.apk

# Uninstall app
adb shell pm uninstall com.package.name

# Clear app data
adb shell pm clear com.package.name

# Start an app
adb shell am start -n com.package.name/.MainActivity
```

### System Information

```bash
# Battery stats
adb shell dumpsys battery

# Memory info
adb shell dumpsys meminfo

# Network stats
adb shell dumpsys netstats

# Display info
adb shell dumpsys display

# Check Android version
adb shell getprop ro.build.version.release

# Device model
adb shell getprop ro.product.model
```

### File Transfer

```bash
# Push file to phone
adb push file.txt /sdcard/

# Pull file from phone
adb pull /sdcard/file.txt .

# List files
adb shell ls /sdcard/
```

## ⚠️ Important Notes

### Security Considerations

- **Tailscale is secure** - All traffic is encrypted
- **Keep Developer Options ON** but only enable USB Debugging when needed
- **Don't expose ADB to public internet** - Always use Tailscale or VPN
- **Authorize only trusted computers** when prompted on phone

### Battery & Performance

- Tailscale uses minimal battery
- scrcpy can drain battery faster - use lower resolution if needed
- Disable battery optimization for Tailscale app:
  - Settings → Apps → Tailscale → Battery → Unrestricted

### After Phone Restart

ADB over TCP is **NOT persistent** after reboot. You need to:
1. Connect via USB once
2. Run `adb tcpip 5555` again
3. Then reconnect wirelessly

To make it permanent, you need root access.

## 🎯 Quick Reference

### One-Time Setup
```bash
# 1. Install Tailscale on both devices
# 2. Connect phone via USB
adb devices
# 3. Enable wireless ADB
adb tcpip 5555
# 4. Get phone's Tailscale IP (from app or via adb)
# 5. Connect wirelessly
adb connect 100.78.106.87:5555
# 6. Disconnect USB cable
```

### Daily Use
```bash
# Connect
adb connect 100.78.106.87:5555

# Mirror screen
scrcpy

# That's it!
```

### Reconnect After Issues
```bash
adb kill-server
adb start-server
adb connect 100.78.106.87:5555
adb devices
scrcpy
```

## 📚 Additional Resources

- ADB Documentation: https://developer.android.com/studio/command-line/adb
- scrcpy GitHub: https://github.com/Genymobile/scrcpy
- Tailscale Docs: https://tailscale.com/kb/
- Android Developer Options: https://developer.android.com/studio/debug/dev-options

## 🤝 Contributing

Found an issue or have a suggestion? Feel free to improve this guide!

## 📄 License

This guide is provided as-is for educational purposes.

---

**Happy Remote Android Control! 🎉**
