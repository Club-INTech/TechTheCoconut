/**
 * \file balise.cpp
 */
#include "balise.h"
#include <libintech/serial/serial_0.hpp>
#include <libintech/serial/serial_1.hpp>
#include "watchdog.h"
bool is_laser_on __attribute__((section (".noinit")));
bool is_moteur_on __attribute__((section (".noinit")));

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}

uint16_t Balise::max_counter(){
	return max_counter_;
}

int16_t Balise::getAngle(uint16_t offset) {
	if(max_counter_==0)
	  return -1;
	
	//temps à soustraire de l'angle pour avoir la valeur au moment du passage du laser
	int32_t diff = ((int32_t)Balise::T_TopTour::value() - (int32_t)offset*4/5);
		
	while(diff<0){ //Assez mystère...
	  diff+=(int32_t)max_counter_;
	}

	return diff *(float)360/(float)max_counter_ ;

}

Balise::Balise()
{
// 	asservissement_moteur_.consigne(0);
	serial_pc::init();
	serial_pc::change_baudrate(9600);
	serial_radio::init();
	serial_radio::change_baudrate(9600);
// 	T_Asservissement::init();
	T_TopTour::init();
    pin_activation_moteur::set_output();
    pin_activation_moteur2::set_output();
    
    //5V sur la pin 12 (B6) pour la direction laser
    sbi(DDRB,PORTB6);
    //On met la pin 13 (OC0A, B7) en OUT
    sbi(DDRB,PORTB7);
    cbi(TCCR0B,CS02);
    cbi(TCCR0B,CS01);
    sbi(TCCR0B,CS00);
    //Seuil (cf formule datasheet)
    //f_wanted=16000000/(2*prescaler*(1+OCR0A))
    // Valeur fixée = 48KHz (ne pas aller au dessus, le pont redresseur chauffe sinon)
    OCR0A= 170;
    if (not WDT_is_reset())
    {
        is_moteur_on = false;
        is_laser_on = false;
    }
    retablir_etat();
    
	sei();
}

void Balise::laser_on(){
    cbi(TCCR0A,WGM00);
    sbi(TCCR0A,WGM01);
    cbi(TCCR0B,WGM02);
    sbi(TCCR0A,COM0A0);
    cbi(TCCR0A,COM0A1);
    sbi(PORTB,PORTB6);
    is_laser_on=true;
}

void Balise::laser_off(){
    cbi(TCCR0A,WGM00);
    cbi(TCCR0A,WGM01);
    cbi(TCCR0B,WGM02);
    cbi(TCCR0A,COM0A0);
    cbi(TCCR0A,COM0A1);
    cbi(PORTB,PORTB6);
    is_laser_on=false;
}

void Balise::moteur_on(){
    pin_activation_moteur::set();
    pin_activation_moteur2::set();
    is_moteur_on = true;
}

void Balise::moteur_off(){
    pin_activation_moteur::clear();
    pin_activation_moteur2::clear();
    is_moteur_on = false;
}

void Balise::retablir_etat(){
    if(is_moteur_on){
        moteur_on();
    }
    if(is_laser_on){
        laser_on();
    }
}
// void Balise::asservir(int32_t vitesse_courante)
// {
// 	int16_t pwm = asservissement_moteur_.pwm(vitesse_courante);
// 	Serial<0>::print(pwm);
// 	moteur_.envoyerPwm(pwm);
// }

