---
## README.md for STM32F4 Discovery Board LED Control (STM32CubeIDE)

This project demonstrates a basic input/output operation on an **STM32F4 Discovery board**. It controls an on-board LED (connected to **PA5**) using a user button (connected to **PC13**).

---
### Features

* Turns the LED on when the user button is pressed.
* Turns the LED off when the user button is released.

---
### Hardware Requirements

* STM32F4 Discovery Board

---
### Software Requirements

* **STM32CubeIDE** (Version 1.x.x or later)

---
### Pin Configuration

* **LED (Green)**: Connected to **PA5**
* **User Button (Blue)**: Connected to **PC13**

---
### How to Use with STM32CubeIDE

1.  **Create a New STM32 Project**:
    * Open STM32CubeIDE and go to `File > New > STM32 Project`.
    * Select your target board (e.g., `STM32F407G-DISC` for the STM32F4 Discovery board) and click `Next`.
    * Give your project a name (e.g., `LED_Button_Control`) and click `Finish`. This will generate a new project with a default configuration.

2.  **Copy the Code**:
    * Once the project is created and the `Device Configuration Tool` opens, you can close it for this simple example, as we're directly manipulating registers.
    * Navigate to the `Core/Src` folder in your Project Explorer and open `main.c`.
    * **Replace the entire content of `main.c`** with the provided code.

3.  **Build the Project**:
    * Click on the **hammer icon** (Build) in the toolbar or go to `Project > Build Project`. STM32CubeIDE will compile your code. You should see "Build Finished" in the console without errors.

4.  **Flash the Microcontroller**:
    * Ensure your STM32F4 Discovery board is connected to your PC via USB.
    * Click on the **green play button** (Run) in the toolbar or go to `Run > Debug` (this will automatically build and flash if not already done).
    * Confirm the debugger settings if prompted (usually the default ST-Link settings are correct).
    * The code will be programmed onto your board, and it will start executing.

---
### Code Explanation

#### Includes and Defines

* `#include "stm32f4xx.h"`: Includes the necessary header file for STM32F4 series microcontrollers, providing access to peripheral registers.
* `#define GPIOAEN (1U<<0)`: Defines a bit mask to enable the clock for GPIO Port A.
* `#define GPIOCEN (1U<<2)`: Defines a bit mask to enable the clock for GPIO Port C.
* `#define PIN5 (1U<<5)`: Defines a bit mask for Pin 5.
* `#define PIN13 (1U<<13)`: Defines a bit mask for Pin 13.
* `#define LED_PIN PIN5`: Assigns `PIN5` to `LED_PIN` for clarity.
* `#define BTN_PIN PIN13`: Assigns `PIN13` to `BTN_PIN` for clarity.

#### `main` function

1.  **Enable Clock Access**:
    ```c
    RCC->AHB1ENR |=GPIOCEN; // Enable clock for GPIOC
    RCC->AHB1ENR |=GPIOAEN; // Enable clock for GPIOA
    ```
    This step is crucial as **peripheral clocks must be enabled** before you can configure or use them. The `RCC->AHB1ENR` register controls the clock enable for GPIO ports on the AHB1 bus.

2.  **Configure PA5 as Output**:
    ```c
    GPIOA->MODER |=(1U<<10);  // Set bit 10
    GPIOA->MODER &=~(1U<<11); // Clear bit 11
    ```
    The **`MODER`** (Mode Register) for a GPIO port controls the pin's operating mode (input, general-purpose output, alternate function, analog). For PA5:
    * Bits `MODER5[1:0]` (i.e., bits 11 and 10) control the mode of PA5.
    * Setting `MODER5[1:0]` to `01` (binary) configures the pin as a general-purpose output.

3.  **Configure PC13 as Input**:
    ```c
    GPIOC->MODER &=~ (1U<<26); // Clear bit 26
    GPIOC->MODER &=~ (1U<<27); // Clear bit 27
    ```
    For PC13:
    * Bits `MODER13[1:0]` (i.e., bits 27 and 26) control the mode of PC13.
    * Setting `MODER13[1:0]` to `00` (binary) configures the pin as a general-purpose input.

4.  **Main Loop**:
    ```c
    while(1)
    {
        if (GPIOC->IDR & BTN_PIN){
            GPIOA->BSRR = LED_PIN;
        }
        else{
            GPIOA->BSRR = (1U<<21);
        }
    }
    ```
    * `GPIOC->IDR & BTN_PIN`: Reads the **Input Data Register (IDR)** of GPIOC. If the `BTN_PIN` (PC13) bit is set (meaning the button is pressed and the pin is high, assuming a pull-up resistor on the button, which is the case for the on-board user button), the condition is true.
    * `GPIOA->BSRR = LED_PIN;`: If the button is pressed, the **Bit Set/Reset Register (BSRR)** of GPIOA is used to set the `LED_PIN` (PA5) to high, turning the LED ON.
    * `GPIOA->BSRR = (1U<<21);`: If the button is not pressed, the `BSRR` is used to reset the `LED_PIN` (PA5) to low, turning the LED OFF. Note that the bit to reset PA5 is at position `5 + 16 = 21` in the BSRR register.

---
### License

This project is open-source and available under the MIT License.

---
