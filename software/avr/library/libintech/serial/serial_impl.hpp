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
#include <libintech/singleton.hpp>

/**
 * Define interne pour charger la bonne valeur dans les registres du microcontrôleur.
 * @warning NE PAS MODIFIER CE DEFINE
 * @fn UBRR
 * @def UBRR
 */

/**
 * Define interne de la taille du ring buffer de la liaison série
 * @fn rx_buffer__SIZE
 * @def rx_buffer__SIZE
 */
#define rx_buffer__SIZE 32

template<uint8_t id>
class Serial : public Singleton<Serial<id> >{
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
    inline void send_char(unsigned char byte);
    
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

public:
    
    inline Serial();
    
    inline void change_baudrate(uint32_t BAUD_RATE);

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

    inline void print(char val){
    	send_char(val);
    	send_ln();
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
        char buffer[sizeof(T)];
        read(buffer,sizeof(T));
        return atol(buffer);
    }

    inline float read(){
        char buffer[sizeof(float)];
        read(buffer,sizeof(float));
        return atof(buffer);
    }

    inline uint8_t read(char* string, uint8_t length){
    	uint8_t i = 0;
    	for (; i < length; i++){
        	while(!available());
        	char tmp = read_char();
        	if(tmp == '\0' || tmp == '\n' || tmp == '\r')
        		return i;
        	string[i] = tmp;
        }
        return i;
    }
};

#endif	/* SERIAL_HPP */

