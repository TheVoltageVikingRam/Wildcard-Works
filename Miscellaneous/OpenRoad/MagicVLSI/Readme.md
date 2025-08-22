# Magic VLSI on Windows using WSL

This guide walks through the installation and setup of **Magic VLSI** on a Windows system using **WSL (Windows Subsystem for Linux)**.
It covers everything from scratch: installing WSL → setting up Magic → running the GUI successfully.

---

## 1. Install WSL

Open **PowerShell (Admin)** and run:

```powershell
wsl --install
```

This installs **Ubuntu on WSL2**. After installation:

* Restart your system
* Open Ubuntu from Start Menu
* Set your **username** and **password**

Verify WSL version:

```powershell
wsl --status
```

---

## 2. Update Linux Packages

Inside WSL (Ubuntu terminal):

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 3. Install Magic VLSI

Install dependencies:

```bash
sudo apt install -y build-essential tcsh csh libx11-dev libx11-xcb-dev \
    libxrender-dev libx11-6 libglu1-mesa-dev freeglut3-dev mesa-common-dev \
    tcl-dev tk-dev libcairo2-dev
```

Install Magic:

```bash
sudo apt install -y magic
```

Check version:

```bash
magic -version
```

---

## 4. Install an X Server on Windows

WSL needs an **X server** to display GUI:

* Download **VcXsrv**: [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/)
* Launch **XLaunch** with:

  * Multiple windows
  * Start no client
  * Disable access control

If you’re on **Windows 11 with WSLg**, skip this step (GUI apps work out-of-the-box).

---

## 5. Configure Display in WSL

For **WSL2**, add these lines to `~/.bashrc`:

```bash
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0.0
export LIBGL_ALWAYS_INDIRECT=1
```

Apply changes:

```bash
source ~/.bashrc
```

Check:

```bash
echo $DISPLAY
```

Example output: `192.168.x.x:0.0`

---

## 6. Run Magic

Launch Magic:

```bash
magic
```

The **Magic VLSI GUI** should now appear on Windows.

---

## 7. Quick Test

Run Magic with the **SCMOS tech file**:

```bash
magic -T scmos
```

---

## 8. Troubleshooting

* Error: **Can't open display** → Check `echo $DISPLAY` and ensure **VcXsrv** is running
* Laggy graphics → run `magic -nowrapper`
* Windows 11 WSLg → No X server needed, just run `magic`

---

## Summary

You now have **Magic VLSI running on Windows through WSL**, ready for schematic capture, layout, and DRC/LVS experiments.

