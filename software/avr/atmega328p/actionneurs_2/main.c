#include <util/delay.h>
#include "ax12.h"
#include "actionneurs.h"


int main()
{
    
    // Initialisation de la freq de la serie pour AX12
    writeData_(0XFE, 0X04, 1, 0XCF  );


    
    // Initialisation pour l'AX12 gauche
    AX12Init (0xFE, 211, 811, 511);
    
    AX12GoTo(0xFE, 500);


    
    while(1)
    {
            // Initialisation de la freq de la serie pour AX12
    writeData_(0XFE, 0X04, 1, 0XCF  );
    
    // Initialisation pour l'AX12 gauche
    AX12Init (0xFE, 211, 811, 511);
    
    AX12GoTo(0xFE, 500);
        
    }
    
    return 0;
}