/**
* \file communicationPC.h
* 
* Namespace permettant de gérer les différentes communications
*
* Ordres :
*  '?' Ping de la liaison série (renvoi 0)
*  'c' Changer les constantes
*      'c' Couleur
*          'r' Rouge
*          'v' Violet
*      'm' Mettre le Max du PWM
*          'r' de rotation à [EntierLong]
*          't' de translation à [EntierLong]
*      'r' Rotation
*          'd' Dérivée à [EntierLong]
*          'i' Intégration à [EntierLong]
*          'p' Proportionnel à [EntierLong]
*      't' Translation
*          'd' Dérivée à [EntierLong]
*          'i' Intégration à [EntierLong]
*          'p' Proportionnel à [EntierLong]
*  'd' Avancer/Reculer
*      'a' en avançant de [EntierLong] mm
*      'r' en reculant de [EntierLong] mm
*  'e' Afficher la valeur de
*      'c' Couleur
*      'i' État des interruptions sur le timer 1
*      'm' Max du PWM
*          'r' de rotation
*          't' de translation
*      'r' Rotation
*          'd' Dérivée
*          'i' Intégration
*          'p' Proportionnel
*      's' Type d'asservissement
*      't' Translation
*          'd' Dérivée
*          'i' Intégration
*          'p' Proportionnel
*  'i' Interruptions sur le timer 1
*      'a' Activer
*      'd' Désactiver
*  'r' Vider la liste des consignes
*  's' Changer de type d'asservissement
*      'r' Rotation
*      't' Translation
*  't' Tourner
*      'a' dans le sens anti-horaire (= trigo) de [EntierLong]/10000 radians
*      'h' dans le sens horaire de [EntierLong]/10000 radians
*  'x' Variable x position en abscisse en mm
*      'c' Changer la valeur à [EntierLong]
*      'e' Afficher la valeur
*  'y' Variable y position en ordonnée en mm
*      'c' Changer la valeur à [EntierLong]
*      'e' Afficher la valeur
*/

#ifndef CommunicationPC_h
#define CommunicationPC_h

#include "robot.h"

namespace CommunicationPC
{
	/**
	* Traite l'information reçue par l'AVR par port série
	* 
	* \return bool FALSE si traitement réussi, TRUE sinon
	*/
	bool traiter(Robot &);

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
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractere(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné le caractère 'c', pour modifier les constantes
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereC(unsigned char caractereLu, Robot &);

	/**
	* Traite le caractère donné après avoir donné les caractères 'c' et 'm', pour changer les constantes du max de PWM
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereCM(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné les caractères 'c' et 'r', pour gérer les constantes d'asservissement en rotation
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereCR(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné les caractères 'c' et 't', pour modifier les constantes d'asservissement en translation
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereCT(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné le le caractère 'd', pour avancer/Reculer (asservissement en translation)
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereD(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné le caractère 'e', pour afficher des valeurs
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereE(unsigned char caractereLu, Robot &);

	/**
	* Traite le caractère donné après avoir donné les caractères 'e' et 'm', pour afficher les constantes du maximum du PWM
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereEM(unsigned char caractereLu, Robot &);

	/**
	* Traite le caractère donné après avoir donné les caractères 'e' et 'r', pour afficher les constantes de l'asservissement en rotation
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereER(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné les caractères 'e' et 't', pour afficher les constantes de l'asservissement en translation
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereET(unsigned char caractereLu, Robot &);

	/**
	* Traite le caractère donné après avoir donné le caractère 'i', pour activer ou désactiver les interruptions sur le timer 1
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereI(unsigned char caractereLu, Robot &);

	/**
	* Traite le caractère donné après avoir donné le caractère 's', pour changer le type d'asservissement
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereS(unsigned char caractereLu, Robot &);

	/**
	* Traite le caractère donné après avoir donné le caractère 't', pour tourner dans un sens
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereT(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné le caractère 'x', pour afficher ou assigner un long en variable x (position en abscisse) en mm
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereX(unsigned char caractereLu, Robot &);
	
	/**
	* Traite le caractère donné après avoir donné le caractère 'y', pour afficher ou assigner un long en variable y (position en ordonnée) en mm
	* 
	* \param unsigned char caractère en entrée de la série
	* \param Robot Référence à l'objet Robot
	*/
	void traiterCaractereY(unsigned char caractereLu, Robot &);
}
#endif
