 #include <libintech/serial/serial_0.hpp>
  #include <libintech/serial/serial_1.hpp>
//  #include <libintech/serial/serial_2.hpp>
//  #include <libintech/serial/serial_3.hpp>

 int main(){
   Serial<0> & serial0 = Serial<0>::Instance();
 //   Serial<1> & serial1 = Serial<1>::Instance();
 //   Serial<2> & serial2 = Serial<2>::Instance();
 //   Serial<3> & serial3 = Serial<3>::Instance();


   while(1){
     serial0.print(0);
 //     serial1.print(0);
 //     serial2.print(0);
 //     serial3.print(0);
   }
 }


//#define BAUD 9600
//#define MYUBRR (F_CPU/16)/BAUD-1

//#include <stdint.h>
//#include <string.h>
//#include <avr/pgmspace.h>
//#include <avr/io.h>
//#include <avr/interrupt.h>
//#include <util/delay.h>
//#include <util/setbaud.h>

//void USART_Init(unsigned int ubrr);
//void USART_Transmit(unsigned char data);

//int main(void)
//{
//   USART_Init(16); //MYUBRR = 51 for current settings

//   while(1)
//   {
//      USART_Transmit('A');
//     _delay_ms(500);
//   }
//}

//void USART_Init( unsigned int ubrr)
//{
//   /* Set baud rate */
//   UBRR0H = (unsigned char)(ubrr>>8);
//   UBRR0L = (unsigned char)ubrr;

//   /* Enable receiver and transmitter */
//   UCSR0B = (1<<RXEN0)|(1<<TXEN0);
//   /* Set frame format: 8data, 2stop bit */
//  // UCSR0C = (1<<USBS0)|(3<<UCSZ00);
   
//    UCSR0C = (!(1<<USBS0))|(1<<UCSZ01)|(1<<UCSZ00);
//}

//void USART_Transmit(unsigned char data)
//{
//   /* Wait for empty transmit buffer */
//   while ( !( UCSR0A & (1<<UDRE0)) );
//   /* Put data into buffer, sends the data */
//   UDR0 = data;
//}
