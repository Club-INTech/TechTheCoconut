#ifndef ULTRASON_HPP
#define ULTRASON_HPP

#include <libintech/timer.hpp>
#include <libintech/register.hpp>
#include <libintech/ring_buffer.hpp>
#include <libintech/algorithm.hpp>
  
    template<class Timer, class Pin>
class ultrason
{
  private:
    /** Attributs */
    typedef uint16_t mesure_t;
    ring_buffer<uint16_t, 3> mesures_;
    uint16_t derniere_valeur_;

  public:
    /** Fonction d'initialisation */
    static void init()
    {
        Timer::init();
        
        /// Initialisation des entrées-sortie.
        //Pin D2 et D3en INPUT
        cbi(DDRD,PORTD2);
        cbi(DDRD,PORTD3);

        //Activation des interruptions pour tout changement logique pour pin2
        cbi(EICRA,ISC01);
        sbi(EICRA,ISC00);
        sbi(EIMSK,INT0);//Activation proprement dite

        //Activation des interruptions pour tout changement logique pour pin3
        cbi(EICRA,ISC11);
        sbi(EICRA,ISC10);
        sbi(EIMSK,INT1);//Activation proprement dite
    
        /// Activation de toutes les interruptions.
        sei();
    }
    
    /** Fonction update */
    template<typename T,uint16_t BUFFER_SIZE>
    void update(ring_buffer<T,BUFFER_SIZE> & mesures)
    {
        if(Pin::read())
        {
            derniere_valeur_ = Timer::value();
        }
        
        else
        {//Front descendant
        // prescaler/fcpu*inchToCm/tempsParInch
            if(Timer::value() <derniere_valeur_)
                mesures.append((Timer::value() + 65536 - derniere_valeur_  )*0.0884353741496);
            else
                mesures.append((Timer::value() - derniere_valeur_ )*0.0884353741496);
        }
    }
    
    /** Fonction update */
    void update()
    {
        if(Pin::read())
        {
            derniere_valeur_ = Timer::value();
        }
        
        //Front descendant
        else
        {
            // prescaler/fcpu*inchToCm/tempsParInch
            if(Timer::value() <derniere_valeur_)
                mesures_.append((Timer::value() + 65536 - derniere_valeur_  )*0.0884353741496);
            else
                mesures_.append((Timer::value() - derniere_valeur_ )*0.0884353741496);
        }
    }
    
    /** Fonction value */
    uint16_t value()
    {
        return mediane(mesures_);
    }
  
};

#endif
