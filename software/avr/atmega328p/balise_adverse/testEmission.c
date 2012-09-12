#include <libintech/timer.hpp>

typedef Timer<0,ModeCounter,1024> emission_timer;

volatile uint8_t emission_flag = 0;

void setup();

int main()
{
    setup();
    
    while(1)
    {
        if(emission_flag == 0)
            Serial<0>::print_noln('v');
    }
    
    return 0;
}

void setup()
{
    //Init série
    Serial<0>::init();
    Serial<0>::change_baudrate(9600);
    
    //Init timer
    emission_timer::init();
    
    //On utilise lesi nterruptions
    sei();
}

//Interruption sur emission_timer (sur overflow)
ISR(TIMER0_0VF_vect)
{
    emission_flag = 0;
}