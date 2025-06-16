# STM32F4 Bare-Metal UART Communication Driver

A bare-metal firmware project for the STM32F446RE microcontroller that demonstrates a custom-built UART (Universal Asynchronous Receiver-Transmitter) driver. This project bypasses vendor-provided HAL libraries and directly manipulates peripheral registers, showcasing low-level embedded systems expertise.

## 📽️ Demo

[![Watch the Demo](https://img.shields.io/badge/Video-Demo-blue?style=for-the-badge&logo=youtube)](https://drive.google.com/file/d/your-drive-link-here/view)

## 🚀 Overview

The firmware listens for UART input and controls an LED based on the received character:

- `'1'` → LED ON (PA5)
- Any other character → LED OFF  
- Also includes `printf` redirection via UART for debug output.

## 🔑 Key Features

- Bare-metal register-level programming (no HAL)
- Custom UART2 driver (polling-based)
- GPIO setup for UART and LED control
- RCC configuration for UART and GPIO clocks
- Retargeted `printf` using `__io_putchar`

## 🛠 Hardware & Software Requirements

### Hardware
- NUCLEO-F446RE board
- USB-to-TTL converter (FTDI/CP2102)
- Onboard or external LED (with 330Ω resistor)
- Jumper wires, ST-Link (onboard)

### Software
- STM32CubeIDE (with built-in ARM GCC toolchain)
- Serial terminal (PuTTY, Tera Term, Minicom)

