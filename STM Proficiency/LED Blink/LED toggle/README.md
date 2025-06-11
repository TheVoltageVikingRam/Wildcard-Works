````markdown
## README.md for STM32 Nucleo-F446RE LED & Button Control

---
### Project Title: STM32 Nucleo-F446RE LED & Button Control (Bare-Metal Register Programming)

---
### Overview

This project demonstrates a fundamental embedded systems application on the **STM32 Nucleo-F446RE development board**. It showcases direct hardware manipulation through **bare-metal register programming** to control an on-board LED based on the state of a user button. This approach highlights a deep understanding of microcontroller peripherals, making it a strong addition to an embedded software portfolio.

---
### Features

* **Bare-Metal Register Programming**: Directly configures GPIO ports by manipulating microcontroller registers (e.g., `RCC->AHB1ENR`, `GPIOA->MODER`, `GPIOC->IDR`, `GPIOA->BSRR`).
* **On-Board LED Control**: Toggles the **Green LED (LD2)** on the Nucleo-F446RE board.
* **User Button Input**: Reads the state of the **User Button (B1)** to control the LED.
* **Simple Logic**: The LED turns ON when the button is pressed and OFF when the button is released.

---
### Hardware Used

* **STM32 Nucleo-F446RE Development Board**

---
### Software Used

* **STM32CubeIDE** (Version 1.x.x or later) - Used for project setup, compilation, and flashing.
* **ARM-compatible toolchain** (integrated within STM32CubeIDE).

---
### Pin Configuration

On the STM32 Nucleo-F446RE board:

* **Green LED (LD2)**: Connected to **PA5**
* **User Button (B1)**: Connected to **PC13**

---
### Code

```c
#include "stm32f4xx.h"
#define GPIOAEN         (1U<<0)
#define GPIOCEN         (1U<<2)
#define PIN5            (1U<<5)
#define PIN13           (1U<<13)
#define LED_PIN         PIN5
#define BTN_PIN         PIN13

int main(void)
{   /*Enable clock access to GPIOA and GPIOC */
    RCC->AHB1ENR |=GPIOCEN;
    RCC->AHB1ENR |=GPIOAEN;

    /*Set PA5 as output pin*/

    GPIOA->MODER |=(1U<<10);
    GPIOA->MODER &=~(1U<<11);

    /*Set PC13 as Input pin*/
    GPIOC->MODER &=~ (1U<<26);
    GPIOC->MODER &=~ (1U<<27);

    while(1)
    {   /** Check if button is pressed **/
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
````

### Code Explanation (Bare-Metal)

This project directly configures the STM32F446RE's General Purpose Input/Output (GPIO) and Reset and Clock Control (RCC) peripherals by accessing their memory-mapped registers.

1.  **`#include "stm32f4xx.h"`**: Includes the standard peripheral header file for the STM32F4 series, providing access to register definitions.

2.  **Define Bit Masks**: Macros like `GPIOAEN`, `GPIOCEN`, `PIN5`, `PIN13`, `LED_PIN`, and `BTN_PIN` are used to provide clear, named bit positions for register manipulation.

3.  **`main` Function**:

      * **Enable Peripheral Clocks (`RCC->AHB1ENR`)**: Before using any GPIO port, its corresponding clock must be enabled in the Reset and Clock Control (RCC) peripheral. `AHB1ENR` controls clocks for peripherals on the AHB1 bus.

      * **Configure PA5 as Output (`GPIOA->MODER`)**: The `MODER` (Mode Register) for each GPIO port consists of two bits per pin. For PA5, bits 11 and 10 of `GPIOA->MODER` are set to `01` (binary) to configure it as a General Purpose Output pin for the LD2 LED.

      * **Configure PC13 as Input (`GPIOC->MODER`)**: For PC13, bits 27 and 26 of `GPIOC->MODER` are set to `00` (binary) to configure it as a General Purpose Input pin for the User Button (B1). The Nucleo board's User Button on PC13 typically uses an internal pull-up, making it active-low.

      * **Main Loop (`while(1)`)**:

          * **`GPIOC->IDR & BTN_PIN`**: Reads the **Input Data Register (IDR)** of GPIOC. This register reflects the current logic level of the input pins. The `& BTN_PIN` isolates the bit corresponding to PC13.
          * **`if (GPIOC->IDR & BTN_PIN)`**: Checks if the button is pressed.
          * **`GPIOA->BSRR = LED_PIN;`**: If the button is pressed, the **Bit Set/Reset Register (BSRR)** of GPIOA is used to set `PA5` high, turning the LED ON.
          * **`GPIOA->BSRR = (1U<<21);`**: If the button is not pressed, the `BSRR` is used to reset `PA5` low, turning the LED OFF.

-----

### Demonstration

*Replace `path/to/your/led_toggle.gif` with the actual path or URL to your GIF file.*

-----

### Contribution

Feel free to fork this repository, explore the code, and suggest improvements.

-----

### License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

```
```
