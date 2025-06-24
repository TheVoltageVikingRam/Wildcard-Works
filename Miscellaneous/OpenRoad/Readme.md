
# # OpenROAD Build (WSL2 - Ubuntu)

This repository contains a working log and build instructions for compiling [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD) completely from source inside **WSL2 (Ubuntu)**, **without Docker**. This setup is designed for **offline builds**—ideal for EDA toolchains in environments like **Cadence Virtuoso** without internet access.

---

## ✅ System Configuration

- **Host OS:** Windows 11 with WSL2
- **WSL Distro:** Ubuntu 22.04
- **RAM:** 16 GB  
- **CPU Cores:** 8  
- **Internet:** Not available inside VM  
- **Use Case:** Offline OpenROAD build for Virtuoso workflows

---

## 📦 Step-by-Step Build Instructions

### 1. Clone OpenROAD Flow Scripts

```bash
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git
cd OpenROAD-flow-scripts

## Installation Steps

### 1. Clone the Flow Scripts

```bash
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git
cd OpenROAD-flow-scripts
```

### 2. Install Dependencies

```bash
cd etc
sudo ./DependencyInstaller.sh -all
cd ..
```

This script handles all dependencies including:
- TCL
- Boost
- spdlog
- lemon
- GTest
- SWIG
- and other required packages

### 3. Setup Python Environment

```bash
python3 -m venv openroad-env
source openroad-env/bin/activate
```

### 4. Build OpenROAD

```bash
./build_openroad.sh --local
```

The build process will:
- Use 20 threads by default (or auto-detect available cores)
- Place the final binary in:  
  `tools/install/OpenROAD/bin/openroad`

### 5. Verify Installation

```bash
tools/install/OpenROAD/bin/openroad -version
```

Successful output will show:  
`OpenROAD v2.0-xxxxx`

## Troubleshooting

Common issues resolved by the dependency installer:
- Missing lemon headers
- spdlog compilation errors
- Boost library issues

For other problems, check the build logs or consult the OpenROAD project documentation.

## Notes

- All builds are performed locally (no internet required after cloning)
- Tested working in offline environments with Virtuoso
- Build time varies based on your system resources
```