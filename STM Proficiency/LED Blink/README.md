# STM32F446RE Bare-Metal LED Blink

This project is a fundamental **"Hello, World!"** example for embedded systems development. It demonstrates a simple **bare-metal C** program that blinks the user LED on an **STM32 Nucleo-64 F446RE** development board by directly manipulating hardware registers.

---

## 🛠 Hardware

- **Board:** STMicroelectronics NUCLEO-F446RE  
- **MCU:** STM32F446RE  
- **User LED:** Green LED connected to **Port A, Pin 5 (PA5)**  

---

## ⚙️ How It Works

This program **does not use any HAL or LL libraries** provided by STMicroelectronics. Instead, it interacts **directly with memory-mapped registers** of the microcontroller.

### Core Logic:

1. **Enable GPIO Clock**  
   Set the appropriate bit in the **RCC_AHB1ENR** register to enable the clock for **GPIOA**.

2. **Configure Pin Mode**  
   Set **PA5** as a general-purpose output by configuring the **GPIOA_MODER** register (bits 11:10) to `01`.

3. **Toggle the LED**  
   Inside an infinite loop, toggle the **GPIOA_ODR** register to turn the LED ON and OFF. A crude delay loop provides the visible blinking effect.

---

## 🎥 Demonstration

> *(Insert your blinking LED GIF or video here for visual reference)*

---

## 🔧 Building and Flashing

### Requirements

- **Toolchain:** [GNU Arm Embedded Toolchain](https://developer.arm.com/downloads/-/gnu-rm) (`arm-none-eabi-gcc`)
- **Flashing Utility:** 
  - [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html)  
  - or `st-flash` (from [stlink](https://github.com/stlink-org/stlink) utilities)

### Build Steps

1. Compile the source:
   ```bash
   arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -nostdlib -T linker_script.ld -o blink.elf main.c