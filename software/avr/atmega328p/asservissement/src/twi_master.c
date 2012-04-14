#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "twi_master.h"

union TWI_statusReg
{
    unsigned char all;
    struct
    {
        unsigned char lastTransOK:1;
        unsigned char unusedBits:7;
    };
};

extern union TWI_statusReg TWI_statusReg;

static unsigned char TWI_buf[ TWI_BUFFER_SIZE ];    // Transceiver buffer
static unsigned char TWI_msgSize;                   // Number of bytes to be transmitted.
static unsigned char TWI_state = TWI_NO_STATE;      // State byte. Default set to TWI_NO_STATE.

static unsigned char TWI_targetSlaveAddress  = 0x10;

unsigned char buffer_r[TWI_BUFFER_SIZE];
unsigned char buffer_t[TWI_BUFFER_SIZE];

union TWI_statusReg TWI_statusReg = {0};            // TWI_statusReg is defined in TWI_Master.h

void TWI_init( void )
{
    TWI_Master_Initialise();
    sei();

    buffer_t[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS) | (FALSE<<TWI_READ_BIT);
    buffer_t[1] = 0x00;
    TWI_Start_Transceiver_With_Data( buffer_r, 2 );
}

void send_reset ( void )
{
    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    buffer_t[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS);
    buffer_t[1] = MASTER_CMD_RESET;
    TWI_Start_Transceiver_With_Data( buffer_t, 2 );

    _delay_us(1);
}

void get_all ( int32_t infos[2]){
	while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    buffer_t[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS);
    buffer_t[1] = MASTER_CMD_ALL;
    TWI_Start_Transceiver_With_Data( buffer_t, 2 );

    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    _delay_us(1);

    buffer_r[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS) | (TRUE<<TWI_READ_BIT);
    TWI_Start_Transceiver_With_Data( buffer_r, 9 );

    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    TWI_Get_Data_From_Transceiver( buffer_r, 9 );

    int32_t angle;
    int32_t distance;
    int32_t temp;

    angle = buffer_r[1];
    temp = buffer_r[2];
    angle += (temp << 8);
    temp = buffer_r[3];
    angle += (temp << 16);
    temp = buffer_r[4];
    angle += (temp << 24);
    infos[0] = angle;
    
    distance = buffer_r[5];
    temp = buffer_r[6];
    distance += (temp << 8);
    temp = buffer_r[7];
    distance += (temp << 16);
    temp = buffer_r[8];
    distance += (temp << 24);
    infos[1]=distance;
}

int32_t get_angle ( void )
{
    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    buffer_t[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS);
    buffer_t[1] = MASTER_CMD_ANGLE;
    TWI_Start_Transceiver_With_Data( buffer_t, 2 );

    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    _delay_us(1);

    buffer_r[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS) | (TRUE<<TWI_READ_BIT);
    TWI_Start_Transceiver_With_Data( buffer_r, 5 );

    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    TWI_Get_Data_From_Transceiver( buffer_r, 5 );

    int32_t angle;
    int32_t temp;

    angle = buffer_r[1];
    temp = buffer_r[2];
    angle += (temp << 8);
    temp = buffer_r[3];
    angle += (temp << 16);
    temp = buffer_r[4];
    angle += (temp << 24);

    return angle;

}

int32_t get_distance ( void )
{
    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    buffer_t[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS);
    buffer_t[1] = MASTER_CMD_DISTANCE;
    TWI_Start_Transceiver_With_Data( buffer_t, 2 );

    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    _delay_us(1);

    buffer_r[0] = (TWI_targetSlaveAddress<<TWI_ADR_BITS) | (TRUE<<TWI_READ_BIT);
    TWI_Start_Transceiver_With_Data( buffer_r, 5 );

    while ( TWI_Transceiver_Busy() && !TWI_statusReg.lastTransOK );

    TWI_Get_Data_From_Transceiver( buffer_r, 5 );

    int32_t distance;
    int32_t temp;

    distance = buffer_r[1];
    temp = buffer_r[2];
    distance += (temp << 8);
    temp = buffer_r[3];
    distance += (temp << 16);
    temp = buffer_r[4];
    distance += (temp << 24);

    return distance;

}
    
/****************************************************************************
Call this function to set up the TWI master to its initial standby state.
Remember to enable interrupts from the main application after initializing the TWI.
****************************************************************************/
void TWI_Master_Initialise(void)
{
  TWBR = TWI_TWBR;                                  // Set bit rate register (Baudrate). Defined in header file.
// TWSR = TWI_TWPS;                                  // Not used. Driver presumes prescaler to be 00.
  TWDR = 0xFF;                                      // Default content = SDA released.
  TWCR = (1<<TWEN)|                                 // Enable TWI-interface and release TWI pins.
         (0<<TWIE)|(0<<TWINT)|                      // Disable Interupt.
         (0<<TWEA)|(0<<TWSTA)|(0<<TWSTO)|           // No Signal requests.
         (0<<TWWC);                                 //
}    
    
/****************************************************************************
Call this function to test if the TWI_ISR is busy transmitting.
****************************************************************************/
unsigned char TWI_Transceiver_Busy( void )
{
  return ( TWCR & (1<<TWIE) );                  // IF TWI Interrupt is enabled then the Transceiver is busy
}

/****************************************************************************
Call this function to fetch the state information of the previous operation. The function will hold execution (loop)
until the TWI_ISR has completed with the previous operation. If there was an error, then the function 
will return the TWI State code. 
****************************************************************************/
unsigned char TWI_Get_State_Info( void )
{
  while ( TWI_Transceiver_Busy() );             // Wait until TWI has completed the transmission.
  return ( TWI_state );                         // Return error state.
}

/****************************************************************************
Call this function to send a prepared message. The first byte must contain the slave address and the
read/write bit. Consecutive bytes contain the data to be sent, or empty locations for data to be read
from the slave. Also include how many bytes that should be sent/read including the address byte.
The function will hold execution (loop) until the TWI_ISR has completed with the previous operation,
then initialize the next operation and return.
****************************************************************************/
void TWI_Start_Transceiver_With_Data( unsigned char *msg, unsigned char msgSize )
{
  unsigned char temp;

  while ( TWI_Transceiver_Busy() );             // Wait until TWI is ready for next transmission.

  TWI_msgSize = msgSize;                        // Number of data to transmit.
  TWI_buf[0]  = msg[0];                         // Store slave address with R/W setting.
  if (!( msg[0] & (TRUE<<TWI_READ_BIT) ))       // If it is a write operation, then also copy data.
  {
    for ( temp = 1; temp < msgSize; temp++ )
      TWI_buf[ temp ] = msg[ temp ];
  }
  TWI_statusReg.all = 0;      
  TWI_state         = TWI_NO_STATE ;
  TWCR = (1<<TWEN)|                             // TWI Interface enabled.
         (1<<TWIE)|(1<<TWINT)|                  // Enable TWI Interupt and clear the flag.
         (0<<TWEA)|(1<<TWSTA)|(0<<TWSTO)|       // Initiate a START condition.
         (0<<TWWC);                             //
}

/****************************************************************************
Call this function to resend the last message. The driver will reuse the data previously put in the transceiver buffers.
The function will hold execution (loop) until the TWI_ISR has completed with the previous operation,
then initialize the next operation and return.
****************************************************************************/
void TWI_Start_Transceiver( void )
{
  while ( TWI_Transceiver_Busy() );             // Wait until TWI is ready for next transmission.
  TWI_statusReg.all = 0;      
  TWI_state         = TWI_NO_STATE ;
  TWCR = (1<<TWEN)|                             // TWI Interface enabled.
         (1<<TWIE)|(1<<TWINT)|                  // Enable TWI Interupt and clear the flag.
         (0<<TWEA)|(1<<TWSTA)|(0<<TWSTO)|       // Initiate a START condition.
         (0<<TWWC);                             //
}

/****************************************************************************
Call this function to read out the requested data from the TWI transceiver buffer. I.e. first call
TWI_Start_Transceiver to send a request for data to the slave. Then Run this function to collect the
data when they have arrived. Include a pointer to where to place the data and the number of bytes
requested (including the address field) in the function call. The function will hold execution (loop)
until the TWI_ISR has completed with the previous operation, before reading out the data and returning.
If there was an error in the previous transmission the function will return the TWI error code.
****************************************************************************/
unsigned char TWI_Get_Data_From_Transceiver( unsigned char *msg, unsigned char msgSize )
{
  unsigned char i;

  while ( TWI_Transceiver_Busy() );             // Wait until TWI is ready for next transmission.

  if( TWI_statusReg.lastTransOK )               // Last transmission competed successfully.              
  {                                             
    for ( i=0; i<msgSize; i++ )                 // Copy data from Transceiver buffer.
    {
      msg[ i ] = TWI_buf[ i ];
    }
  }
  return( TWI_statusReg.lastTransOK );                                   
}

// ********** Interrupt Handlers ********** //
/****************************************************************************
This function is the Interrupt Service Routine (ISR), and called when the TWI interrupt is triggered;
that is whenever a TWI event has occurred. This function should not be called directly from the main
application.
****************************************************************************/
ISR(TWI_vect){
  static unsigned char TWI_bufPtr;
  
  switch (TWSR)
  {
    case TWI_START:             // START has been transmitted  
    case TWI_REP_START:         // Repeated START has been transmitted
      TWI_bufPtr = 0;                                     // Set buffer pointer to the TWI Address location
    case TWI_MTX_ADR_ACK:       // SLA+W has been tramsmitted and ACK received
    case TWI_MTX_DATA_ACK:      // Data byte has been tramsmitted and ACK received
      if (TWI_bufPtr < TWI_msgSize)
      {
        TWDR = TWI_buf[TWI_bufPtr++];
        TWCR = (1<<TWEN)|                                 // TWI Interface enabled
               (1<<TWIE)|(1<<TWINT)|                      // Enable TWI Interupt and clear the flag to send byte
               (0<<TWEA)|(0<<TWSTA)|(0<<TWSTO)|           //
               (0<<TWWC);                                 //  
      }else                    // Send STOP after last byte
      {
        TWI_statusReg.lastTransOK = TRUE;                 // Set status bits to completed successfully. 
        TWCR = (1<<TWEN)|                                 // TWI Interface enabled
               (0<<TWIE)|(1<<TWINT)|                      // Disable TWI Interrupt and clear the flag
               (0<<TWEA)|(0<<TWSTA)|(1<<TWSTO)|           // Initiate a STOP condition.
               (0<<TWWC);                                 //
      }
      break;
    case TWI_MRX_DATA_ACK:      // Data byte has been received and ACK tramsmitted
      TWI_buf[TWI_bufPtr++] = TWDR;
    case TWI_MRX_ADR_ACK:       // SLA+R has been tramsmitted and ACK received
      if (TWI_bufPtr < (TWI_msgSize-1) )                  // Detect the last byte to NACK it.
      {
        TWCR = (1<<TWEN)|                                 // TWI Interface enabled
               (1<<TWIE)|(1<<TWINT)|                      // Enable TWI Interupt and clear the flag to read next byte
               (1<<TWEA)|(0<<TWSTA)|(0<<TWSTO)|           // Send ACK after reception
               (0<<TWWC);                                 //  
      }else                    // Send NACK after next reception
      {
        TWCR = (1<<TWEN)|                                 // TWI Interface enabled
               (1<<TWIE)|(1<<TWINT)|                      // Enable TWI Interupt and clear the flag to read next byte
               (0<<TWEA)|(0<<TWSTA)|(0<<TWSTO)|           // Send NACK after reception
               (0<<TWWC);                                 // 
      }    
      break; 
    case TWI_MRX_DATA_NACK:     // Data byte has been received and NACK tramsmitted
      TWI_buf[TWI_bufPtr] = TWDR;
      TWI_statusReg.lastTransOK = TRUE;                 // Set status bits to completed successfully. 
      TWCR = (1<<TWEN)|                                 // TWI Interface enabled
             (0<<TWIE)|(1<<TWINT)|                      // Disable TWI Interrupt and clear the flag
             (0<<TWEA)|(0<<TWSTA)|(1<<TWSTO)|           // Initiate a STOP condition.
             (0<<TWWC);                                 //
      break;      
    case TWI_ARB_LOST:          // Arbitration lost
      TWCR = (1<<TWEN)|                                 // TWI Interface enabled
             (1<<TWIE)|(1<<TWINT)|                      // Enable TWI Interupt and clear the flag
             (0<<TWEA)|(1<<TWSTA)|(0<<TWSTO)|           // Initiate a (RE)START condition.
             (0<<TWWC);                                 //
      break;
    case TWI_MTX_ADR_NACK:      // SLA+W has been tramsmitted and NACK received
    case TWI_MRX_ADR_NACK:      // SLA+R has been tramsmitted and NACK received    
    case TWI_MTX_DATA_NACK:     // Data byte has been tramsmitted and NACK received
//    case TWI_NO_STATE              // No relevant state information available; TWINT = 0
    case TWI_BUS_ERROR:         // Bus error due to an illegal START or STOP condition
    default:     
      TWI_state = TWSR;                                 // Store TWSR and automatically sets clears noErrors bit.
                                                        // Reset TWI Interface
      TWCR = (1<<TWEN)|                                 // Enable TWI-interface and release TWI pins
             (0<<TWIE)|(0<<TWINT)|                      // Disable Interupt
             (0<<TWEA)|(0<<TWSTA)|(0<<TWSTO)|           // No Signal requests
             (0<<TWWC);                                 //
  }
}