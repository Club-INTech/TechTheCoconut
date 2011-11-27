/**
 * \file serie.h
 * 
 * Classe permettant de gérer la liaison série
 */

#ifndef Serie_h
#define Serie_h

#include <stdint.h>

#include "usart.h"

#include "asservissement.h"

class Serie {
	public:
		/**
		 * Constructeur
		 */
		Serie();
		
		/**
		 * Destructeur
		 */
		~Serie();
		
		/**
		 * Traite l'information reçue par l'AVR par port série
		 * 
		 * \return bool FALSE si traitement réussi, TRUE sinon
		 */
		bool traiter();
	private:
		/**
		 * Lit le message courant comme un long (int32_t) via la liaison série
		 * 
		 * \return int32_t Long renvoyé par la liaison série
		 */
		int32_t lireEntierLong();
		
		/**
		 * Lit le message courant comme un unsigned char via la liaison série
		 * 
		 * \return unsigned char Caractère renvoyé par la liaison série
		 */
		unsigned char lireCaractere();
		
		/**
		 * Traite le caractère donné en appelant les fonctions voulues
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractere(unsigned char caractereLu);
		
		/**
		 * Traite le caractère donné après avoir donné le caractère 'c', pour gérer les constantes d'asservissement
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractereC(unsigned char caractereLu);
		
		/**
		 * Traite le caractère donné après avoir donné les caractère 'c' et 't', pour gérer les constantes d'asservissement en translation
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractereCT(unsigned char caractereLu);
		
		/**
		 * Traite le caractère donné après avoir donné les caractère 'c' et 'r', pour gérer les constantes d'asservissement en rotation
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractereCR(unsigned char caractereLu);
		
		/**
		 * Traite le caractère donné après avoir donné le 'p', pour changer le PWM selon le type d'asservissement voulu (translation ou rotation)
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractereP(unsigned char caractereLu);
		
		/**
		 * Traite le caractère donné après avoir donné le 'x', pour afficher ou assigner un long dans une variable temporaire x
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractereX(unsigned char caractereLu);
		
		/**
		 * Traite le caractère donné après avoir donné le 'y', pour afficher ou assigner un long dans une variable temporaire y
		 * 
		 * \param unsigned char caractère en entrée de la série
		 */
		void traiterCaractereY(unsigned char caractereLu);
};


#endif
