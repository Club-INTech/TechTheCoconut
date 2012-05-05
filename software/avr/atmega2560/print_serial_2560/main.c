#include <libintech/serial/serial_1_interrupt.hpp>
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_1.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/ring_buffer.hpp>
#include <avr/io.h>
#include <stdint.h>  

uint16_t moyenne(uint16_t data[], int size);

int main() 
{
	ring_buffer<uint16_t, 10> mesures_;
 	//Initialisation série
 	Serial<0>::init();
	Serial<0>::change_baudrate(9600);
	Serial<1>::init();
	Serial<1>::change_baudrate(9600);
	sei();
	
	while(1){
		mesures_.append(Serial<1>::read_int());
		Serial<0>::print(moyenne(mesures_.data(),mesures_.size()));
	}
	
	return 0;
}

uint16_t moyenne(uint16_t data[], int size)
{
  uint16_t result=0;
  for(int i=0;i<size;i++)
  {
      result+=data[i];    
  }    
  result/=size;
  
  return result;
}