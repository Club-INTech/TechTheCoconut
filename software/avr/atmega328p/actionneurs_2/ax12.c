/*
  ax12.c - arbotiX Library for AX-12 Servos
  Copyright (c) 2008,2009 Michael E. Ferguson.  All right reserved.
*/

#include "ax12.h"
#include "actionneurs.h"
#include <avr/interrupt.h>
#include <avr/io.h>

#define bitRead(value, bit) (((value) >> (bit)) & 0x01)
#define bitSet(value, bit) ((value) |= (1UL << (bit)))
#define bitClear(value, bit) ((value) &= ~(1UL << (bit)))
#define bitWrite(value, bit, bitvalue) (bitvalue ? bitSet(value, bit) : bitClear(value, bit))

/******************************************************************************
 * Hardware Serial Level, this uses the same stuff as Serial, therefore 
 *  you should not use the Arduino Serial library.
 ******************************************************************************/

byte ax_rx_buffer[AX12_BUFFER_SIZE];
int status_id;
int status_error;
int status_data;

// volatile uint16_t ax_cons1 = 200;
// volatile uint16_t ax_cons2 = 800;

// making these volatile keeps the compiler from optimizing loops of available()
volatile byte ax_rx_Pointer;                       

/** helper functions to emulate half-duplex */
void setTX(){
    bitClear(UCSR0B, RXCIE0);
    bitClear(UCSR0B, RXEN0); 
    bitSet(UCSR0B, TXEN0); 
}
void setRX(){
    bitClear(UCSR0B, TXEN0);
    bitSet(UCSR0B, RXEN0);
    bitSet(UCSR0B, RXCIE0); 
    ax_rx_Pointer = 0;
}

/** Sends a character out the serial port */
byte ax12writeB(byte data){
    while (bit_is_clear(UCSR0A, UDRE0));
    UDR0 = data;
    return data; 
}

/** We have a one-way recieve buffer, which is reset after each packet is receieved.
    A wrap-around buffer does not appear to be fast enough to catch all bytes at 1Mbps. */
// ISR(USART_RX_vect){  
//     ax_rx_buffer[(ax_rx_Pointer++)] = UDR0;
// }

/** initializes serial0 transmit at baud, 8-N-1 */
void ax12Init(long baud){
    UBRR0H = ((F_CPU / 16 + baud / 2) / baud - 1) >> 8;
    UBRR0L = ((F_CPU / 16 + baud / 2) / baud - 1);

    /************************/
//     uint16_t UBRR  =(F_CPU/8/BAUD_RATE_SERIE - 1)/2;
//     UBRR0H = (unsigned char)(UBRR >> 8);
//     UBRR0L = (unsigned char)UBRR;
//     
//     UCSR0B |= ( 1 << RXCIE0 );  //Activation de l'interruption de réception
//     
//     
//     UCSR0B |= ( 1 << RXEN0 );   //Activation de la réception
//     UCSR0B |= ( 1 << TXEN0 );   //Activation de l'emission
// 
//     UCSR0C = (1 << USBS0)|(3<<UCSZ00);
//     sei();
    /***********************/
     
    ax_rx_Pointer = 0;                                    
    // enable rx
//     setRX();    
}

/******************************************************************************
 * Packet Level
 ******************************************************************************/

/** send instruction packet */
void ax12SendPacket (byte id, byte datalength, byte instruction, byte *data){
    byte checksum = 0;
//     setTX();    
    ax12writeB(0xFF);
    ax12writeB(0xFF);
    checksum += ax12writeB(id);
    checksum += ax12writeB(datalength + 2);
    checksum += ax12writeB(instruction);

    byte f;
    for (f=0; f<datalength; f++) {
      checksum += ax12writeB(data[f]);
    }
    // checksum = 
    ax12writeB(~checksum);
//     setRX();
}

/** read status packet */
byte ax12ReadPacket(){
    unsigned long ulCounter;
    byte timeout, error, status_length, checksum, offset;
    byte volatile bcount;
    offset = 0; timeout = 0; bcount = 0;
    while(bcount < 11){
        ulCounter = 0;
        while((bcount + offset) == ax_rx_Pointer){
            if(ulCounter++ > 1000L){  // was 3000
                timeout = 1;
                break;
            }
        }
        if (timeout) break;
        if ((bcount == 0) && (ax_rx_buffer[offset] != 0xff)) offset++;
        else bcount++;
    }


    error = 0;
    do {
        error++;
        offset++;
        bcount--;
    } while (ax_rx_buffer[offset] == 255);          
    if (error > 1) error =0;
 
    status_length = 2 + ax_rx_buffer[offset+1];
    if (bcount != status_length) error+=2;
    checksum = 0;

    byte f;
    for (f=0; f<status_length; f++)
        checksum += ax_rx_buffer[offset+f];
    if (checksum != 255) error+=4;
    if (error == 0) {
        status_id = ax_rx_buffer[offset];
        status_error = ax_rx_buffer[offset+2];
        switch (status_length) {
            case 5: status_data = ax_rx_buffer[offset+3]; break;   
            case 6: status_data = ax_rx_buffer[offset+3] + (ax_rx_buffer[offset+4]<<8); break;
            default: status_data = 0;
        }
    } else {
        status_id = -1;
        status_error = -1;
        status_data = -1; 
    }
    return error;
}

/******************************************************************************
 * Instruction Level
 ******************************************************************************/

/** ping */
byte ping (byte id) {
     byte *data = 0;
     ax12SendPacket (id, 0, AX_PING, data); 
     return ax12ReadPacket(); 
}

/** reset */
byte reset (byte id) {
     byte *data = 0;
     ax12SendPacket (id, 0, AX_RESET, data); 
     return ax12ReadPacket(); 
}

/** action */
byte action (byte id) {
     byte *data = 0;
     ax12SendPacket (id, 0, AX_ACTION, data); 
     return ax12ReadPacket(); 
}

/** read data */
byte readData (byte id, byte regstart, byte reglength) {
    byte data [2];
    data [0] = regstart; data [1] = reglength;
    ax12SendPacket (id, 2, AX_READ_DATA, data);
    return ax12ReadPacket();
}

/** write data */
byte writeData (byte id, byte regstart, byte reglength, int value) {
    byte data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_WRITE_DATA, data);
    return ax12ReadPacket();
}

/** reg write */
byte regWrite (byte id, byte regstart, byte reglength, int value) {
    byte data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_REG_WRITE, data);
    return ax12ReadPacket();
}


volatile uint16_t ax_cons1 = 511;
volatile uint16_t ax_cons2 = 511;
