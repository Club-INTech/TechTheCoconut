#include <libintech/timer.hpp>

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
            
        }
    }
    
    return 0;
}

void setup()
{
    Serial<0>::init();
    Serial<0>::change_baudrate(9600);
    
    
}