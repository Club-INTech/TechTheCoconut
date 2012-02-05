/* 
 * File:   serial.hpp
 * Author: philippe
 *
 * Created on 4 février 2012, 19:00
 */

#ifndef SERIAL_HPP
#define	SERIAL_HPP

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include <string.h>

#define BAUD_RATE 57600

/**
 * Define interne pour charger la bonne valeur dans les registres du microcontrôleur.
 * @warning NE PAS MODIFIER CE DEFINE
 * @fn UBRR
 * @def UBRR
 */
#define UBRR (F_CPU/8/BAUD_RATE - 1)/2

/**
 * Define interne de la taille du ring buffer de la liaison série
 * @fn rx_buffer__SIZE
 * @def rx_buffer__SIZE
 */
#define rx_buffer__SIZE 32

class Serial{
private:
    struct ring_buffer
    {
        ring_buffer(){
        }
        unsigned char buffer[rx_buffer__SIZE] ;
        int head;
        int tail;
    };
    
    volatile ring_buffer rx_buffer_;
    
private:
    inline void send_char(unsigned char byte)
    {
            while ( !( UCSR0A & (1<<UDRE0)) );
            UDR0 = byte;
    }
    
    inline bool available(void)
    {
    		return (rx_buffer__SIZE + rx_buffer_.head - rx_buffer_.tail) % rx_buffer__SIZE;
    }
    
    inline unsigned char read_char(){
			if (rx_buffer_.head == rx_buffer_.tail)
			{
				return -1;
			}
			else
			{
				unsigned char c = rx_buffer_.buffer[rx_buffer_.tail];
				rx_buffer_.tail = (rx_buffer_.tail + 1) % rx_buffer__SIZE;
				return c;
			}
    }
    
    inline void send_ln(){
    	send_char('\r');
    	send_char('\n');
    }

private:

    Serial(){
        UBRR0H = (unsigned char)(UBRR >> 8);
		UBRR0L = (unsigned char)UBRR;
		UCSR0B |= ( 1 << RXCIE0 );	//Activation de l'interruption de réception
		UCSR0B |= ( 1 << RXEN0 );	//Activation de la réception
		UCSR0B |= ( 1 << TXEN0 );	//Activation de l'emission
		UCSR0C = (1 << USBS0)|(3<<UCSZ00);
		sei();
    }

public:

    static Serial& Instance(){
    	static Serial instance;
    	return instance;
    }
    

    inline void store_char(unsigned char c)
    {
    	int i = (rx_buffer_.head + 1) % rx_buffer__SIZE;
    	if (i != rx_buffer_.tail)
    	{
    		rx_buffer_.buffer[rx_buffer_.head] = c;
    		rx_buffer_.head = i;
    	}
    }



    template<class T>
    inline void print(T val){
    	char buffer[sizeof(T)];
    	ltoa(val,buffer,10);
    	print((const char *)buffer);
    }

    inline void print(const char * val)
    {
    	for(unsigned int i = 0 ; i < strlen(val) ; i++)
    	{
    		send_char(val[i]);
    	}
    	send_ln();
    }

    template<class T>
    inline T read(void){
        T res = 0;
        char buffer[sizeof(T)];
        read(buffer,sizeof(T));
        return atol(buffer);
    }

    inline void read(char* string, int length){
        for (unsigned int i = 0; i < length; i++){
        	while(!available());
        	string[i] = read_char();
        }
    }
};

ISR(USART_RX_vect)
{
	Serial & serial = Serial::Instance();
	unsigned char c = UDR0;
	serial.store_char(c);
}

#endif	/* SERIAL_HPP */

