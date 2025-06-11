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

> [![Blinking LED Demo](https://via.placeholder.com/400x200.png?text=View+GIF)](https://drive.google.com/file/d/1dncVYLXKyS7a2w23sBotAOIPoXEAzlIN/view?usp=drivesdk)
---

Building and Running with STM32CubeIDE
This project can be easily built and run using STM32CubeIDE, which integrates a text editor, compiler, and debugger in one place.
 * Create a Project: Open STM32CubeIDE and create a new STM32 Project.
 * Select Target: In the Target Selector, choose the NUCLEO-F446RE board or the STM32F446RE microcontroller directly.
 * Initialize Project: Give your project a name and finish the setup wizard. You can let it initialize the peripherals with default settings, though this code won't use the generated HAL code.
 * Replace main.c: Navigate to the Core/Src folder in the Project Explorer. Open the main.c file and replace its entire content with the code from this project.
 * Build: Click the Build button (the hammer icon) in the toolbar.
 * Run: Connect your Nucleo board to your computer. Click the Run button (the green play icon) to flash the program onto the board. The IDE will handle the compilation and flashing automatically.
The user LED should now be blinking!