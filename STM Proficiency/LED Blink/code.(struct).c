//Author: Ram Tripathi
//Board STM32 Nucelo F446RE
// Where is the LED connected?
// Port: A
// Pin: 5

#include <stdint.h>

// Base address for peripherals
#define PERIPH_BASE         (0x40000000UL)

// AHB1 bus base address
#define AHB1PERIPH_OFFSET   (0x00020000UL)
#define AHB1PERIPH_BASE     (PERIPH_BASE + AHB1PERIPH_OFFSET)

// GPIOA peripheral base address
#define GPIOA_OFFSET        (0x0000UL)
#define GPIOA_BASE          (AHB1PERIPH_BASE + GPIOA_OFFSET)

// RCC peripheral base address
#define RCC_OFFSET          (0x3800UL)
#define RCC_BASE            (AHB1PERIPH_BASE + RCC_OFFSET)

// Pin 5 definition
#define PIN5                (1U << 5)
#define LED_PIN             PIN5

// RCC AHB1 Enable Register offset
#define GPIOAEN             (1U << 0)  // Bit 0 for GPIOA clock enable

// RCC and GPIO typedefs
typedef struct {
    volatile uint32_t DUMMY[12];
    volatile uint32_t AHB1ENR;
} RCC_TypeDef;

typedef struct {
    volatile uint32_t MODER;
    volatile uint32_t OTYPER;
    volatile uint32_t OSPEEDR;
    volatile uint32_t PUPDR;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t LCKR;
    volatile uint32_t AFR[2];
} GPIO_TypeDef;

// RCC and GPIOA pointers
#define RCC     ((RCC_TypeDef *) RCC_BASE)
#define GPIOA   ((GPIO_TypeDef *) GPIOA_BASE)

int main(void)
{
    /* 1. Enable clock access to GPIOA */
    RCC->AHB1ENR |= GPIOAEN;

    /* 2. Set PA5 as output pin (MODER5 = 01) */
    GPIOA->MODER &= ~(3U << 10);  // Clear bits 11 and 10
    GPIOA->MODER |=  (1U << 10);  // Set bit 10

    while (1)
    {
        /* 3. Toggle PA5 */
        GPIOA->ODR ^= LED_PIN;

        /* Delay loop */
        for (volatile int i = 0; i < 100000; i++);
    }
}
