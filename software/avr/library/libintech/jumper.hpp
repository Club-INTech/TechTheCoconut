#ifndef CAPTEUR_VIEUX_HPP
#define CAPTEUR_VIEUX_HPP

/** @file libintech/jumper.hpp
 *  @brief Ce fichier crée une classe jumper pour pouvoir l'utiliser simplement.
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 

/// Classe Jumper
template<class Pin>
class jumper
{
    public :
        /// Initialisation du jumper.
        static void init()
        {
            // Port en input
            Pin::set_input();
        }
        
        /// Retourne un 1 ou un 0 selon la valeur
        /// de la pin.
        static bool value()
        {
            return Pin::read();
        }
};

#endif
        