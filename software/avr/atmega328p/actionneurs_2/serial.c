#include "serial.h"
#include "ax12.h"


#include <avr/io.h>
#include <avr/interrupt.h>


struct ring_buffer rx_buffer = { { 0 }, 0, 0 };


ISR(USART_RX_vect)
{
    unsigned char c = UDR0;
    store_char(c, &rx_buffer);
}

void uart_init( void )
{
    UBRR0H = (unsigned char)(UBRR >> 8);
    UBRR0L = (unsigned char)UBRR;
    
    UCSR0B |= ( 1 << RXCIE0 );  //Activation de l'interruption de réception
    
    
    UCSR0B |= ( 1 << RXEN0 );   //Activation de la réception
    UCSR0B |= ( 1 << TXEN0 );   //Activation de l'emission

    UCSR0C = (1 << USBS0)|(3<<UCSZ00);
    sei();
}


inline void uart_send_ln(void )
{
    uart_send_char('\r');
    uart_send_char('\n');
}

inline void uart_send_char(unsigned char byte)
{
//     setTX();
    while ( !( UCSR0A & (1<<UDRE0)) );
    UDR0 = byte;
//     setRX();
}

inline void uart_send_string(const char *string)
{
    unsigned char i;
    for (i = 0 ; string[i] != '\0' ; i++)
        uart_send_char(string[i]);
}



inline void printShortNumber(unsigned short n)
{
    unsigned char buf[8 * sizeof(long)]; // Assumes 8-bit chars. 
    unsigned int i = 0;

    if (n == 0)
    {
        uart_send_char('0');
        return;
    } 

    while (n > 0)
    {
        buf[i++] = n % 10;
        n /= 10;
    }

    for (; i > 0; i--)
        uart_send_char((char) (buf[i - 1] < 10 ? '0' + buf[i - 1] : 'A' + buf[i - 1] - 10));
}

void printlnChar( unsigned char c)
{
    uart_send_char( c );
    uart_send_ln();
}

void printlnString(const char *string )
{
    uart_send_string(string);
    uart_send_ln();
}

unsigned char uart_recv_char(void)
{
    while ( ! (UCSR0A & (1 << RXC0)) );
    
    return UDR0;
}

uint8_t available(void)
{
    return (RX_BUFFER_SIZE + rx_buffer.head - rx_buffer.tail) % RX_BUFFER_SIZE;
}

int read(void)
{
    if (rx_buffer.head == rx_buffer.tail)
    {
        return -1;
    }
    else
    {
        unsigned char c = rx_buffer.buffer[rx_buffer.tail];
        rx_buffer.tail = (rx_buffer.tail + 1) % RX_BUFFER_SIZE;
        return c;
    }
}

inline void store_char(unsigned char c, struct ring_buffer *rx_buffer)
{
    int i = (rx_buffer->head + 1) % RX_BUFFER_SIZE;
    
    if (i != rx_buffer->tail)
    {
        rx_buffer->buffer[rx_buffer->head] = c;
        rx_buffer->head = i;
    }
}




/**************************************************************************************
 *************************************************************************************/



void print(const char * val)
{
    unsigned int i;
    for(i = 0 ; i < strlen(val) ; i++)
    {
        uart_send_char(val[i]);
    }
    uart_send_ln();
}

uint8_t read_(char* string, uint8_t length)
{
    uint8_t i = 0;
    for (; i < length; i++)
    {
        while(!available()){ asm("nop"); }
        char tmp = read();
        if(tmp == '\0' || tmp == '\n' || tmp == '\r')
            return i;
        string[i] = tmp;
    }
    return i;
}