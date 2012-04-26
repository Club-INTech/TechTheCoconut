#include <stdint.h>
#include "infrarouge.h"


#define NB_VAL_ECHANTILLONAGE  8
uint16_t    val_ADCH[]   = {170, 150, 120, 100, 80,  50 , 30 , 20 };
uint16_t    val_mm[]     = {50 , 70 , 100, 130, 160, 280, 500, 650};

uint16_t conversion(uint16_t adch)
{
        uint8_t ind = indiceTab(adch);
        return regLin(val_ADCH[ind], val_ADCH[ind+1], val_mm[ind], val_mm[ind+1], adch);        
}


uint16_t indiceTab(uint16_t adch)
{
    uint16_t i;
    
    for (i = 1; i < NB_VAL_ECHANTILLONAGE -1; i++)
    {
        if (adch >= val_ADCH[i])
        {
            return i-1;
        }        
    }
    
    return NB_VAL_ECHANTILLONAGE - 2;
    
}

uint16_t regLin(uint16_t x1, uint16_t x2, uint16_t y1, uint16_t y2, uint16_t x)
{
    uint16_t pourcentage = ((x1-x)*100)/(x1-x2);
//     return pourcentage;
    return (pourcentage*y2 + (100-pourcentage)*y1)/100;
}
