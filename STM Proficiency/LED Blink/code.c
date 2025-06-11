Author: Ram Tripathi
Board: STM32 Nucleo F446RE

// Where is the LED connected?
// Port: A
// Pin: 5

// Base address for peripherals
#define PERIPH_BASE         (0x40000000UL)

// AHB1 bus base address
#define AHB1PERIPH_OFFSET   (0x00020000UL)
#define AHB1PERIPH_BASE     (PERIPH_BASE + AHB1PERIPH_OFFSET)

// GPIOA peripheral base address
// Corrected GPIO_OFFSET to GPIOA_OFFSET
#define GPIOA_OFFSET        (0x0000UL)
#define GPIOA_BASE          (AHB1PERIPH_BASE + GPIOA_OFFSET)

// RCC peripheral base address
#define RCC_OFFSET          (0x3800UL)
#define RCC_BASE            (AHB1PERIPH_BASE + RCC_OFFSET)

// RCC AHB1 Enable Register
#define AHB1EN_R_OFFSET     (0x30UL)
#define RCC_AHB1EN_R        (*(volatile unsigned int *)(RCC_BASE + AHB1EN_R_OFFSET))

// GPIOA Mode Register
#define MODER_R_OFFSET      (0x00UL)
// Corrected MODE_R_OFFSET to MODER_R_OFFSET
#define GPIOA_MODE_R        (*(volatile unsigned int *) (GPIOA_BASE + MODER_R_OFFSET))

// GPIOA Output Data Register
#define OD_R_OFFSET         (0x14UL)
#define GPIOA_OD_R          (*(volatile unsigned int *) (GPIOA_BASE + OD_R_OFFSET))

// Bit to enable GPIOA clock
#define GPIOAEN             (1U << 0)

// Pin 5 definition
#define PIN5                (1U << 5)
#define LED_PIN             PIN5


int main(void)
{
    /* 1. Enable clock access to GPIOA */
    RCC_AHB1EN_R |= GPIOAEN;

    /* 2. Set PA5 as output pin */
    // For pin 5, we need to configure bits 11 and 10 of the MODE register.
    // Setting it to '01' makes it a general-purpose output.
    GPIOA_MODE_R |= (1U << 10);  // Set bit 10 to 1
    GPIOA_MODE_R &= ~(1U << 11); // Set bit 11 to 0

    while (1)
    {
        /* 3. Set PA5 high to turn on the LED */
        // This will keep the LED permanently on.
        GPIOA_OD_R ^= LED_PIN;
        for(int i=0; i<100000; i++){}


    }
}
