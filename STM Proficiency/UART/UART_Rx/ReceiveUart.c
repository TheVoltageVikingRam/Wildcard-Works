/********************************************************************************
 * FILE: recieveuart.c
 * DESCRIPTION:
 * Combined file for a simple UART receive application on an STM32F446xx.
 * This code initializes UART2 to receive characters and controls an LED
 * connected to PA5 based on the character received.
 *
 * - Original file: main.c (Application Logic)
 * - Original file: uart.c (UART Driver Implementation)
 * - Original file: uart.h (UART Driver Header)
 *
 ********************************************************************************/

/********************************************************************************
 * Section: Includes and Common Definitions
 * (Originally from uart.h, uart.c, and main.c)
 ********************************************************************************/
#include "stm32f446xx.h"
#include <stdio.h>
#include <stdint.h>

/* Peripheral and System Clock Definitions (from uart.c) */
#define GPIOAEN			(1U<<0)
#define UART2EN			(1U<<17)
#define SYS_FREQ		16000000
#define APB1_CLK		SYS_FREQ

/* UART Configuration Definitions (from uart.c) */
#define UART_BAUDRATE	115200
#define CR1_TE			(1U<<3)  // Transmit Enable
#define CR1_RE			(1U<<2)  // Receive Enable
#define CR1_UE			(1U<<13) // USART Enable
#define SR_TXE			(1U<<7)  // Transmit Data Register Empty
#define SR_RXNE			(1U<<5)  // Read Data Register Not Empty

/* LED Pin Definitions (from main.c) */
#define GPIOA_5			(1U<<5)
#define LED_PIN			GPIOA_5


/********************************************************************************
 * Section: Function Prototypes
 * (Originally from uart.h)
 ********************************************************************************/
void uart2_rxtx_init(void);
void uart2_write(int ch);
char uart2_read(void);


/********************************************************************************
 * Section: UART Driver Implementation
 * (Originally from uart.c)
 ********************************************************************************/

// Static (private) function prototypes
static void uart_set_baudrate(USART_TypeDef *USARTx, uint32_t PeriphClk, uint32_t BaudRate);
static uint16_t compute_uart_bd(uint32_t PeriphClk, uint32_t BaudRate);

/**
 * @brief Retargets printf to use UART for output.
 */
int __io_putchar(int ch)
{
	uart2_write(ch);
	return ch;
}

/**
 * @brief Initializes GPIOA pins PA2 (TX) and PA3 (RX) for UART2 and configures UART2.
 */
void uart2_rxtx_init(void){
	/******Configure uart gpio pins*******/
	/*Enable Clock access to gpioa*/
	RCC->AHB1ENR |= GPIOAEN;

	/*Set PA2 mode to alternate function mode*/
	GPIOA->MODER &= ~(1U<<4);
	GPIOA->MODER |= (1U<<5);

	/*Set PA2 Alternate function type to UART_TX (AF07)*/
	GPIOA->AFR[0] &= ~(0xF<<8); // Clear bits 11, 10, 9, 8
	GPIOA->AFR[0] |= (0x7<<8);  // Set to 0111 (AF7)

	/*Set PA3 mode to alternate function mode*/
	GPIOA->MODER &= ~(1U<<6);
	GPIOA->MODER |= (1U<<7);
	
	/*Set PA3 Alternate function type to UART_RX (AF07)*/
	GPIOA->AFR[0] &= ~(0xF<<12); // Clear bits 15, 14, 13, 12
	GPIOA->AFR[0] |= (0x7<<12);  // Set to 0111 (AF7)

	/***********Configure uart module*********/
	/*Enable clock access to uart2 ***/
	RCC->APB1ENR |= UART2EN;
	
	/***Configure baudrate****/
	uart_set_baudrate(USART2,APB1_CLK,UART_BAUDRATE);
	
	/***Configure the transfer direction*****/
	USART2->CR1 = (CR1_TE | CR1_RE); // Sets TE and RE
	
	/***Enable the uart module*****/
	USART2->CR1 |= CR1_UE; // Enables the UART peripheral
}

/**
 * @brief Reads a single character from UART2. Blocks until a character is received.
 * @return The character read from UART.
 */
char uart2_read(void)
{
	//Make sure the data receive register is not empty //
	while (!(USART2->SR & SR_RXNE)){}

	//Read data ///
	return USART2->DR;
}

/**
 * @brief Writes a single character to UART2. Blocks until the character is sent.
 * @param ch The character to write.
 */
void uart2_write(int ch)
{
	/**Make sure the trasmit data regiter is empty**/
	while (!(USART2->SR & SR_TXE)){}

	/*Write to transmit data register*/
	USART2->DR =  (ch & 0xFF);
}

/**
 * @brief Sets the baud rate for a given USART peripheral.
 */
static void uart_set_baudrate(USART_TypeDef *USARTx, uint32_t PeriphClk, uint32_t BaudRate )
{
	USARTx->BRR = compute_uart_bd(PeriphClk, BaudRate);
}

/**
 * @brief Computes the value for the Baud Rate Register (BRR).
 */
static uint16_t compute_uart_bd(uint32_t PeriphClk, uint32_t BaudRate)
{
	return (PeriphClk + (BaudRate/2U)) / BaudRate;
}


/********************************************************************************
 * Section: Main Application
 * (Originally from main.c)
 ********************************************************************************/

// Global variable to store the received character
char key;

/**
 * @brief Main program entry point.
 */
int main(void)
{
	/* Enable clock for GPIOA for the LED */
	RCC->AHB1ENR |= GPIOAEN;

	/* Set PA5 to output mode for the LED */
	GPIOA->MODER |= (1U<<10);
	GPIOA->MODER &=~ (1U<<11);

	// Initialize UART for communication
	uart2_rxtx_init();

	// Infinite loop to receive data and control LED
	while(1)
	{
		key = uart2_read();
		if (key == '1')
		{
			// Turn LED ON
			GPIOA->ODR |= LED_PIN;
		}
		else
		{
			// Turn LED OFF
			GPIOA->ODR &=~ LED_PIN;
		}
	}
}
