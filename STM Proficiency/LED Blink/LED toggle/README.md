-----

## STM32 Nucleo-F446RE LED & Button Control

-----

### 📹 Demo Video

[![Watch the video](https://img.shields.io/badge/Watch-Video-blue)](https://drive.google.com/file/d/1dwYv9QqkCEuEoeAFwyfsn6z3Ukuloxz3/view?usp=drivesdk)

-----
### Project Overview

This project provides a fundamental embedded systems example on the **STM32 Nucleo-F446RE development board**. It highlights **bare-metal register programming** to control an on-board LED, demonstrating direct hardware interaction without relying on abstraction layers like HAL or LL libraries. This approach is excellent for showcasing a deep understanding of microcontroller peripherals in an embedded software portfolio.

-----

### Key Features

  * **Bare-Metal Register Programming**: Directly manipulates microcontroller registers (e.g., `RCC->AHB1ENR`, `GPIOA->MODER`, `GPIOC->IDR`, `GPIOA->BSRR`) for GPIO control.
  * **On-Board LED Control**: Toggles the **Green LED (LD2)** present on the Nucleo-F446RE board.
  * **User Button Input**: Reads the state of the **User Button (B1)** to control the LED's behavior.
  * **Simple Logic**: The LED illuminates when the button is pressed and turns off when it's released.

-----

### Hardware and Software

  * **Hardware**: STM32 Nucleo-F446RE Development Board
  * **Software**: STM32CubeIDE (Version 1.x.x or later), which includes the necessary ARM-compatible toolchain.

-----

### Pin Configuration

The code directly interfaces with these pins on the Nucleo-F446RE:

  * **Green LED (LD2)**: Connected to **PA5**
  * **User Button (B1)**: Connected to **PC13**

-----

### Code

```c
#include "stm32f4xx.h"
#define GPIOAEN			(1U<<0)
#define GPIOCEN			(1U<<2)
#define PIN5			(1U<<5)
#define PIN13			(1U<<13)
#define LED_PIN			PIN5
#define BTN_PIN			PIN13


int main(void)
{	/*Enable clock access to GPIOA and GPIOC */
	RCC->AHB1ENR |=GPIOCEN;
	RCC->AHB1ENR |=GPIOAEN;

	/*Set PA5 as output pin*/

	GPIOA->MODER |=(1U<<10);
	GPIOA->MODER &=~(1U<<11);

	/*Set PC13 as Input pin*/
	GPIOC->MODER &=~ (1U<<26);
	GPIOC->MODER &=~ (1U<<27);

	while(1)
	{	/** Check if button is pressed **/
		if (GPIOC->IDR & BTN_PIN){
		/*Turn on LED*/
		GPIOA->BSRR = LED_PIN;
		
		}
		else{
		/*Turn off LED*/	
		GPIOA->BSRR = (1U<<21);
		
		}

	}
}

```

-----

### How to Build & Flash

1.  **Create a New STM32 Project**:
    In STM32CubeIDE, create a new project. Select your board (`NUCLEO-F446RE`) from the Board Selector. You can close the `*.ioc` file if it automatically opens, as this project uses direct register access.

2.  **Integrate the Code**:
    Open `Core/Src/main.c` in your project and replace its entire content with the provided code.

3.  **Build the Project**:
    Connect your Nucleo-F446RE board to your PC via USB. In STM32CubeIDE, click the **hammer icon** (Build) or navigate to `Project > Build Project`.

4.  **Flash the Microcontroller**:
    Click the **green play button** (Run) in the toolbar or go to `Run > Debug`. This action will compile and program the code onto your Nucleo board.

-----

### Code Walkthrough (Bare-Metal)

The code directly interacts with the STM32F446RE's peripherals by accessing their memory-mapped registers.

  * **`#include "stm32f4xx.h"`**: This header file provides definitions for the microcontroller's peripheral registers.
  * **Bit Mask Definitions**: Macros like `GPIOAEN`, `GPIOCEN`, `PIN5`, `PIN13`, `LED_PIN`, and `BTN_PIN` make register manipulation clearer by representing specific bit positions.
  * **`main` Function**:
      * **Clock Enable (`RCC->AHB1ENR`)**: Before any GPIO port can be used, its clock must be enabled via the `RCC->AHB1ENR` register. This supplies power to the GPIO peripheral.
      * **GPIO Mode Configuration (`GPIOA->MODER`, `GPIOC->MODER`)**: The `MODER` (Mode Register) controls each pin's function.
          * **PA5 (LED)**: Bits 11 and 10 of `GPIOA->MODER` are set to `01` (binary) to configure PA5 as a General Purpose Output.
          * **PC13 (Button)**: Bits 27 and 26 of `GPIOC->MODER` are set to `00` (binary) to configure PC13 as a General Purpose Input.
      * **Main Loop (`while(1)`)**: This loop continuously checks the button state.
          * **Button Read (`GPIOC->IDR & BTN_PIN`)**: The `IDR` (Input Data Register) of GPIOC reflects the current logic level of the pins. The `& BTN_PIN` operation isolates the PC13 bit. The current `if` condition assumes the button reads `HIGH` when pressed.
          * **LED Control (`GPIOA->BSRR`)**: The `BSRR` (Bit Set/Reset Register) provides an atomic way to control pin states.
              * Setting the `LED_PIN` bit (bit 5) in the lower half of `BSRR` turns the LED ON.
              * Setting bit `21` (which is `LED_PIN + 16` for the reset section) in the upper half of `BSRR` turns the LED OFF.

