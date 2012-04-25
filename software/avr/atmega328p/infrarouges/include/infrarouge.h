#ifndef HEADER_INFRAROUGE
#define HEADER_INFRAROUGE

#include <stdint.h>

// Converti la valeur donnée sur ADCH en mm
        uint16_t conversion(uint16_t adch);

//----------------------//
// Fonctions bas-niveau //
//----------------------//



// Cette fonction permet de se placer dans l'interval du tableau val_ADCH
// tel que la valeur mesurée de ADCH soit entre indiceTab() et indiceTab() + 1
//      Exemple :   Si ADCH = 70, alors indiceTab(70) = 2
//      --------
//
        uint16_t indiceTab(uint16_t adch);
        
        
// Cette fonction réalise la regression linéaire des points M1(x1, y1) et M2(x2, y2)
// pour le point M d'abscisse x.
        uint16_t regLin(uint16_t x1, uint16_t x2, uint16_t y1, uint16_t y2, uint16_t x);


#endif