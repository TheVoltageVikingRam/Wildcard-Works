#include "stm32f446xx.h"
#include <stdio.h>
#include <stdint.h>


#define GPIOAEN			(1U<<0)
#define UART2EN			(1U<<17)

#define SYS_FREQ		16000000
#define APB1_CLK		SYS_FREQ

#define UART_BAUDRATE	115200
#define CR1_TE			(1U<<3)
#define CR1_UE			(1U<<13)  // CORRECTED: USART Enable is bit 13, not bit 3
#define SR_TXE			(1U<<7)

// Function prototypes from the original code
static void uart_set_baudrate(USART_TypeDef *USARTx, uint32_t PeriphClk, uint32_t BaudRate );
static uint16_t compute_uart_bd(uint32_t PeriphClk, uint32_t BaudRate);
void uart2_tx_init(void);
void uart2_write(int ch);

int __io_putchar(int ch)
{
	uart2_write(ch);
	return ch;

}


int main(void)
{
	uart2_tx_init(); 
	while(1)
	{
		printf("Hello My name is Ram Tripathi. My github ID is TheVoltageVikingRam\n\r");
	}
}

void uart2_tx_init(void){
	/******Configure uart gpio pins*******/
	/*Enable Clock access to gpioa*/
	RCC->AHB1ENR |=GPIOAEN;


	/*Set PA2 mode to alternate function mode*/
	GPIOA->MODER &=~(1U<<4);
	GPIOA->MODER |= (1U<<5);

	/*Set PA2 Alternate function type to UART_TX (AF07)*/

	GPIOA->AFR[0] &=~ (0xF<<8); // Clear bits 11, 10, 9, 8
	GPIOA->AFR[0] |= (0x7<<8);  // Set to 0111 (AF7)


	/***********Configure uart module*********/
	/*Enable clock access to uart2 ***/
	RCC->APB1ENR |= UART2EN;
	/***Configure baudrate****/
	uart_set_baudrate(USART2,APB1_CLK,UART_BAUDRATE);
	/***Configure the transfer direction*****/
	USART2->CR1 = CR1_TE; // Sets TE and clears everything else

	/***Enable the uart module*****/
	USART2->CR1 |= CR1_UE; // Enables the UART peripheral

}

void uart2_write(int ch)
{
	/**Make sure the trasmit data regiter is empty**/

	while (!(USART2->SR & SR_TXE)){

	}
	/*Write to transmit data register*/
	// CORRECTED: Peripheral is named USART2, not UART2, in the header.
	USART2->DR =  (ch & 0xFF);

}

static void uart_set_baudrate(USART_TypeDef *USARTx, uint32_t PeriphClk, uint32_t BaudRate )
{
	USARTx->BRR = compute_uart_bd(PeriphClk, BaudRate);

}

static uint16_t compute_uart_bd(uint32_t PeriphClk, uint32_t BaudRate)
{
	// This calculation is a correct and clever shortcut for finding the BRR value
	return	(PeriphClk + (BaudRate/2U))/BaudRate;
}
