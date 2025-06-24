# 🛠️ OpenROAD in WSL2 — Working Build Guide

This repository documents a **fully working installation of [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts)** inside **WSL2 Ubuntu** on a Windows machine.

> ✅ Built from source  
> ✅ Verified with 20-thread compilation  
> ✅ WSL2 resource-tuned  
> ✅ No Docker, no container mess  

---

## 💻 System Specs

| Component       | Info             |
|----------------|------------------|
| Host OS        | Windows 11       |
| WSL Distro     | Ubuntu 22.04     |
| RAM            | 16 GB            |
| CPU            | 8 cores          |
| Storage        | 50 GB+ SSD       |

---

## 🚀 Step-by-Step Setup

### 1. Clone the OpenROAD Flow Scripts

```bash
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git
cd OpenROAD-flow-scripts

---
##
cd etc
sudo ./DependencyInstaller.sh -all
cd ..
