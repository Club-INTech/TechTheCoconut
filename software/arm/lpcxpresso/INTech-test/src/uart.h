
#ifndef UART_H_
#define UART_H_

// ***********************
// Uart 0 functions
void UART0_Init(int baudrate);
void UART0_Sendchar(char c);
char UART0_Getchar();
int  UART0_Getchar_NonBlocking();
int  UART0_isDataAvailable();
void UART0_PrintString(char *pcString);


// Uart 1 functions
void UART1_Init(int baudrate);
void UART1_Sendchar(char c);
char UART1_Getchar();
int  UART1_Getchar_NonBlocking();
int  UART1_isDataAvailable();
void UART1_PrintString(char *pcString);

// Uart 2 functions
void UART2_Init(int baudrate);
void UART2_Sendchar(char c);
char UART2_Getchar();
int  UART2_Getchar_NonBlocking();
int  UART2_isDataAvailable();
void UART2_PrintString(char *pcString);

// Uart 3 functions
void UART3_Init(int baudrate);
void UART3_Sendchar(char c);
char UART3_Getchar();
int  UART3_Getchar_NonBlocking();
int  UART3_isDataAvailable();
void UART3_PrintString(char *pcString);

// Generic Uart functions
int UART_Init(int uart, int baudrate);
void UART_Sendchar(int uart, char c);
char UART_Getchar(int uart);
int  UART_Getchar_NonBlocking(int uart);
int  UART_isDataAvailable(int uart);
void UART_PrintString(int uart, char *pcString);

int initUart(int uart, int baudRate);

#endif /*UART_H_*/
