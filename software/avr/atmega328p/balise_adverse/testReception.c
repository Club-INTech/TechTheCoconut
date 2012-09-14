#include <libintech/timer.hpp>

typedef Timer<0,ModeCounter,64> reception_timer;

volatile uint8_t reception_flag = 0;

void setup();

int main()
{
    setup();
    
    while(1)
    {
        char buffer[10];
        unsigned char order = Serial<0>::read_char();
        
        if(order == 'v')
        {
            sbi(PCINT, PCINT16);
        }
        
        if(emission_flag == 0)
        {
            emission_flag = 1;
            cbi(PCINT, PCINT16);
        }
    }
    
    
    
    return 0;
}

void setup()
{
    Serial<0>::init();
    Serial<0>::change_baudrate(9600);
    
        //Init timer
    reception_timer::init();
    
    sei();
}

//Interruption sur emission_timer (sur overflow)
ISR(TIMER0_0VF_vect)
{
    reception_flag = 0;
}