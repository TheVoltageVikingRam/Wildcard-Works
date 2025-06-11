-----

## README.md for STM32 Nucleo-F446RE LED & Button Control

-----

### Project Title: STM32 Nucleo-F446RE LED & Button Control (Bare-Metal Register Programming)

-----

### Overview

This project showcases a fundamental embedded systems application on the **STM32 Nucleo-F446RE development board**. It demonstrates direct hardware manipulation through **bare-metal register programming** to control an on-board LED based on the state of a user button. This approach highlights a deep understanding of microcontroller peripherals, making it a strong addition to an embedded software portfolio.

-----

### Features

  * **Bare-Metal Register Programming**: Directly configures GPIO ports by manipulating microcontroller registers (e.g., `RCC->AHB1ENR`, `GPIOA->MODER`, `GPIOC->IDR`, `GPIOA->BSRR`).
  * **On-Board LED Control**: Toggles the **Green LED (LD2)** on the Nucleo-F446RE board.
  * **User Button Input**: Reads the state of the **User Button (B1)** to control the LED.
  * **Simple Logic**: The LED turns ON when the button is pressed and OFF when the button is released.

-----

### Hardware Used

  * **STM32 Nucleo-F446RE Development Board**

-----

### Software Used

  * **STM32CubeIDE** (Version 1.x.x or later) - Used for project setup, compilation, and flashing.
  * **ARM-compatible toolchain** (integrated within STM32CubeIDE).

-----

### Pin Configuration

On the STM32 Nucleo-F446RE board:

  * **Green LED (LD2)**: Connected to **PA5**
  * **User Button (B1)**: Connected to **PC13**

-----

### How to Build & Flash with STM32CubeIDE

1.  **Create a New STM32 Project**:
    Open STM32CubeIDE. Go to `File > New > STM32 Project`. In the "Board Selector" tab, search for and select `NUCLEO-F446RE`. Provide a project name (e.g., `Nucleo_LED_Button_BareMetal`) and click `Finish`. You can close the Device Configuration Tool (`.ioc` file) if it opens.

2.  **Integrate the Code**:
    Navigate to the `Core/Src` folder in your Project Explorer and open `main.c`. **Replace the entire content of `main.c`** with the following code:

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

3.  **Build the Project**:
    Connect your Nucleo-F446RE board to your PC via USB. In STM32CubeIDE, click on the **hammer icon** (Build) in the toolbar, or go to `Project > Build Project`.

4.  **Flash the Microcontroller**:
    Click on the **green play button** (Run) in the toolbar, or go to `Run > Debug`. This will automatically program your board with the compiled code.

-----

### Code Explanation (Bare-Metal)

This project directly configures the STM32F446RE's General Purpose Input/Output (GPIO) and Reset and Clock Control (RCC) peripherals by accessing their memory-mapped registers.

1.  **`#include "stm32f4xx.h"`**: Includes the standard peripheral header file for the STM32F4 series, providing access to register definitions.

2.  **Define Bit Masks**: Macros like `GPIOAEN`, `GPIOCEN`, `PIN5`, `PIN13`, `LED_PIN`, and `BTN_PIN` are used to provide clear, named bit positions for register manipulation.

3.  **`main` Function**:

      * **Enable Peripheral Clocks (`RCC->AHB1ENR`)**: Before using any GPIO port, its corresponding clock must be enabled in the Reset and Clock Control (RCC) peripheral. `AHB1ENR` controls clocks for peripherals on the AHB1 bus.

      * **Configure PA5 as Output (`GPIOA->MODER`)**: The `MODER` (Mode Register) for each GPIO port consists of two bits per pin. For PA5, bits 11 and 10 of `GPIOA->MODER` are set to `01` (binary) to configure it as a General Purpose Output pin for the LD2 LED.

      * **Configure PC13 as Input (`GPIOC->MODER`)**: For PC13, bits 27 and 26 of `GPIOC->MODER` are set to `00` (binary) to configure it as a General Purpose Input pin for the User Button (B1). The Nucleo board's User Button on PC13 typically uses an internal pull-up, making it active-low.

      * **Main Loop (`while(1)`)**:

          * **`!(GPIOC->IDR & BTN_PIN)`**: Reads the **Input Data Register (IDR)** of GPIOC. Since the Nucleo user button is active-low (reads 0 when pressed), the `!` operator makes the `if` condition true when the button is pressed.
          * **`GPIOA->BSRR = LED_PIN;`**: If the button is pressed, the **Bit Set/Reset Register (BSRR)** of GPIOA is used to set `PA5` high, turning the LED ON.
          * **`GPIOA->BSRR = (1U<<(LED_PIN + 16));`**: If the button is not pressed, the `BSRR` is used to reset `PA5` low, turning the LED OFF. The `BSRR` is divided into two 16-bit halves: bits `0-15` for setting pins and bits `16-31` for resetting pins.

-----

### Video Demonstration

See the LED toggling in action on the STM32 Nucleo-F446RE board\!

[](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DYOUR_VIDEO_ID)
*Click the image above to watch the video demonstration.*



-----
