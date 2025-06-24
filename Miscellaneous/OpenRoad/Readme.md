---

# OpenROAD in WSL2

This repository documents the successful installation and build of the [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts) toolchain inside **WSL2 (Ubuntu)** on a Windows machine.

## ✅ System

- OS: Windows 11 with WSL2
- Distro: Ubuntu (WSL)
- RAM: 16 GB
- CPU: 8 cores

## 🚀 What Worked

### 1. Cloning the Repository

```bash
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git
cd OpenROAD-flow-scripts

2. Installing Dependencies

cd etc
sudo ./DependencyInstaller.sh -all
cd ..

3. Setting Up Python Environment

python3 -m venv openroad-env
source openroad-env/bin/activate

4. Building OpenROAD

./build_openroad.sh --local

> This compiled OpenROAD successfully. Binaries are located in: tools/install/OpenROAD/bin/openroad




---

🧪 Testing

To confirm installation:

tools/install/OpenROAD/bin/openroad -version


---

🛠 Notes

All dependencies were installed using the official DependencyInstaller.sh -all

No internet access was needed from within VirtualBox for Cadence Virtuoso workflows



---

👨‍💻 Maintained By

Ram Tripathi