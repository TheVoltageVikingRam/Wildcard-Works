# GDS3D – Windows Quick-Start Guide

GDS3D renders IC chip layouts (GDSII files) in real-time 3D using OpenGL.  
Supports **SkyWater SKY130**, **IHP SG13G2**, and custom process files.

---

## Running GDS3D on Windows

### Step 1 – Open the Launcher

Double-click **`LAUNCH GDS3D.cmd`** in this folder.

A GUI window will appear:

```
┌──────────────────────────────────────────────────┐
│  GDS3D Launcher  v1.9                            │
├──────────────────────────────────────────────────┤
│  1. GDS File     [ path/to/your.gds ] [Browse]  │
│  Recent Files:   last_design.gds                 │
│                  counter_4bit.gds                │
├──────────────────────────────────────────────────┤
│  2. Technology   [ SkyWater SKY130 (130nm)  v ]  │
├──────────────────────────────────────────────────┤
│  3. Options   [x] Verbose  [ ] Fullscreen        │
│  ──────────────────────────────────────────────  │
│           [ Launch GDS3D >>> ]                   │
└──────────────────────────────────────────────────┘
```

1. Click **Browse** and pick any `.gds` file
2. Choose your **technology** from the dropdown
3. Click **Launch GDS3D**

> The launcher remembers the last 6 files you opened.

---

## Available Technology Files

| Technology | Use for |
|-----------|---------|
| **SkyWater SKY130 (130nm)** | Open-source CMOS – Efabless, Google shuttle chips |
| **SkyWater SKY130 S10** | SKY130 S10 SRAM variant |
| **IHP SG13G2 (130nm SiGe)** | IHP BiCMOS open-source process |
| **Generic / Example** | Mock 8-metal process (bundled example GDS) |
| **Browse for custom...** | Point to any `.txt` tech file you wrote |

---

## 3D Navigation Controls

| Action | Control |
|--------|---------|
| Move forward / back / left / right | **W A S D** or arrow keys |
| Move up / down | **Q** / **Z** |
| Rotate view | Left mouse drag |
| Walk & strafe | Right mouse drag |
| Zoom | Scroll wheel |
| Reset camera | **R** |
| Toggle layer legend | **L** |
| Explode layers apart | **E** |
| Net / trace highlight | **H** then click a metal |
| Select top cell | **T** |
| Performance counter | **P** |
| Take screenshot | **F8** |
| Full keymap | **F1** |
| Exit | **ESC** or close window |

---

## Command-Line Usage

You can also launch GDS3D directly from a terminal:

```bat
cd <project folder>
win32\GDS3D.exe -p techfiles\sky130.txt -i path\to\your.gds
```

**All options:**

| Flag | Description |
|------|-------------|
| `-p <file>` | Process / tech definition file (required) |
| `-i <file>` | Input GDSII file (required) |
| `-t <cell>` | Specify top cell name |
| `-f` | Start in fullscreen |
| `-u` | Disable GDS file monitoring |
| `-v` | Verbose output |
| `-h` | Show help |

---

## Writing a Custom Tech File

Tech files are plain text. Each layer block looks like:

```
LayerStart: Metal 1
Layer:      68        # GDS layer number
Datatype:   20        # GDS datatype (0 = any)
Height:     1376      # Bottom height in nm
Thickness:  360       # Layer thickness in nm
Red:        0.40      # RGB colour 0.0–1.0
Green:      0.60
Blue:       0.90
Filter:     0.0       # Transparency (keep 0.0)
Metal:      1         # 1 = metal (traceable), 0 = via/implant
Shortkey:   1         # Key 0-9 to toggle visibility
Show:       1         # 1 = visible by default
LayerEnd
```

> The **first layer must always be the Substrate** with `Layer: 255`.

See `techfiles/example.txt` for a fully commented reference.

---

## Rebuilding from Source (Visual Studio)

1. Open `win32\GDS3D.sln` in Visual Studio 2017 or later
2. Select **Release | x64**
3. Build → the executable is output to `win32\x64\Release\GDS3D.exe`
4. Update `LAUNCH GDS3D.cmd` to point to the new path if needed

Dependencies (all bundled in source):
- OpenGL / GLU / WGL  (Windows built-in)
- Clipper library  (`libgdsto3d/clipper/`)
- Voro++ library   (`libgdsto3d/voro++/`)

---

## System Requirements

| Item | Minimum |
|------|---------|
| OS | Windows 7 or later (64-bit recommended) |
| GPU | Any with **OpenGL 1.5+** (Intel, AMD, NVIDIA) |
| RAM | 512 MB |
| Storage | ~25 MB |

---

## License

GDS3D is free software distributed under the **GNU GPL v2**.  
See `LICENSE.txt` and `LGPLLicense.txt` for full details.

Original authors: Jasper Velner & Michiel Soer, IC-Design Group, University of Twente.  
Extended by: Bertrand Pigeard (assembly, GMSH export, SKY130 support).  
GitHub: <https://github.com/trilomix/GDS3D>
