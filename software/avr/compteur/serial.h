#ifndef _USART_H_
#define _USART_H_

/**
 * Librairie C avr pour atmega 168 et 328 pour l'utilisation de liaison série 
 * @file usart.h
 * @author Jérémy Cheynet avec le support psychologique de Yann Sionneau
 * @brief Librairie C avr pour liaison série
 * @version 1.0
 * @date 07/11/2010
 * @todo Régler le problème d'overflow lors de la lecture d'un unsigned lon dans la fonction readULongNumber.
 */

#include <avr/io.h>
#include <avr/interrupt.h>

/**
 * @defgroup inline
 * @brief Fonction private
 * Tout les fonctions commençant par inline sont des fonctions "interne" à la librairie.
 * Bien évidement, elle peuvent être appelée, mais il vaut mieux utiliser les fonctions faites pour ça
 * @warning NE PAS UTILISER
 */

/**
 * @defgroup print
 * @brief Fonction pour print des choses
 * Cette fonction permet de printer des données sans envoyer de retour chariot.
 */

/**
 * @defgroup println
 * @brief Fonction pour print d'autres choses
 * Cette fonction permet de printer des données avec un retour chariot automatique.
 */

/**
 * Permet de définir le débit de la liaison série.
 * Fonction bien pour les débit suivants :
 * @li 9600
 * @li 57600
 * @fn BAUD_RATE
 * @def BAUD_RATE
 */
#define BAUD_RATE 57600

/**
 * Define interne pour charger la bonne valeur dans les registres du microcontrôleur.
 * @warning NE PAS MODIFIER CE DEFINE
 * @fn UBRR
 * @def UBRR
 */
#define UBRR (F_CPU/8/BAUD_RATE - 1)/2

/**
 * Define interne de la taille du ring buffer de la liaison série
 * @fn RX_BUFFER_SIZE
 * @def RX_BUFFER_SIZE
 */
#define RX_BUFFER_SIZE 32

/**
 * Cette structure correspond au buffer circulaire de réception des DATA en série. Lors d'une réception (par interruption), les données reçues sont stockées dans ce buffer.
 * @struct ring_buffer
 * @brief Il s'agit du buffer circulaire de réception
 */
struct ring_buffer
{
	unsigned char buffer[RX_BUFFER_SIZE];
	int head;
	int tail;
};

//Fonction de base de la liaison série
/**
 * @fn void uart_init( void )
 * @brief Initialisation de la liaison série
 */
void uart_init(void);

/**
 * @fn unsigned char uart_recv_char( void )
 * @brief Réception bloquante d'un unsigned char
 * @return Le char reçu par la liaison série
 */
unsigned char uart_recv_char(void);

/**
 * @ingroup inline
 * @fn inline void uart_send_char( unsigned char )
 * @brief Permet d'envoyer un char par la liaison série
 * Cette fonction est plus une fonction utilisée pour la librairie elle-même (genre de private)
 * @param byte Correspond à l'octet à envoyer.
 */
inline void uart_send_char(unsigned char);

/**
 * @ingroup inline
 * @fn inline void uart_send_ln( void )
 * @brief Permet d'envoyer un retour chariot
 */
inline void uart_send_ln( void );

/**
 * @ingroup inline
 * @fn inline void uart_send_string( const char *)
 * @brief Permet d'envoyer toute une chaine de caractère
 * @param string Le pointeur vers la chaine de caractère à envoyer
 */
inline void uart_send_string(const char *);

//Fonction suplémentaire

/**
 * @ingroup inline
 * @fn inline void printShortNumber( unsigned short )
 * @brief Permet d'envoyer un nombre sur 1 octet et non signé
 * @param n C'est le short à envoyer
 * Cette fonction permet d'envoyer un unsigned short. Elle sert pour les fonctions de plus haut niveau.
 */
inline void printShortNumber( unsigned short );

/**
 * @ingroup inline
 * @fn inline void printIntNumber( unsigned int)
 * @brief Permet l'envoi d'un nombre sur 2 octet et non signé
 * @param n C'est l'int à envoyer
 */
inline void printIntNumber( unsigned int );

/**
 * @ingroup inline
 * @fn inline void printLongNumber( unsigned long)
 * @brief Permet d'envoyer un nombre sur 4 octets et non signé
 * @param n C'est le long à envoyer
 */
inline void printLongNumber( unsigned long );

//Définition des prints

/**
 * @ingroup print
 * @fn void printString( const char *)
 * @brief Permet d'envoyer une chaine de caractère
 * @param string Le pointeur vers la chaine de caractère à envoyer
 * Fonction qui permet d'envoyer toute une chaine de caractère sans aller à la ligne.
 */
void printString( const char * );

/**
 * @ingroup print
 * @fn void printShort( short )
 * @brief Permet d'envoyer un short
 * @param entier Le nombre a envoyer
 * Cette fonction permet d'envoyer un nombre codé sur 1 octet et signé et sans retour automatique à la ligne
 */
void printShort( short );

/**
 * @ingroup print
 * @fn void printUShort( unsigned short )
 * @brief Permet d'envoyer un unsigned short
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 1 octet, non signé et sans retour automatique à la ligne.
 */
void printUShort( unsigned short );

/**
 * @ingroup print
 * @fn void printInt( int )
 * @brief Permet d'envoyer un int
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 2 octet, signé et sans retour automatique à la ligne.
 */
void printInt( int );

/**
 * @ingroup print
 * @fn void printUInt( unsigned int )
 * @brief Permet d'envoyer un unsigned int
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 2 octet, non signé et sans retour automatique à la ligne.
 */
void printUInt( unsigned int );

/**
 * @ingroup print
 * @fn void printLong( long )
 * @brief Permet d'envoyer un long
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 4 octet, signé et sans retour automatique à la ligne.
 */
void printLong( long );

/**
 * @ingroup print
 * @fn void printULong( unsigned long )
 * @brief Permet d'envoyer un unsigned long
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 4 octet, non signé et sans retour automatique à la ligne.
 */
void printULong( unsigned long );

/**
 * @ingroup print
 * @fn void printChar( unsigned char )
 * @brief Permet d'envoyer un char
 * @param c Le caractère à envoyer
 */
void printChar( unsigned char );


//Définition des prints ln

/**
 * @ingroup println
 * @fn void println( void )
 * @brief Permet d'envoyer un retour chariot
 * Cette fonction se contente d'envoyer un retour chariot pour aller à la ligne.
 */
void println( void );

/**
 * @ingroup println
 * @fn void printlnString( const char *)
 * @brief Permet d'envoyer une chaine de caractère
 * @param string Le pointeur vers la chaine de caractère à envoyer
 * Fonction qui permet d'envoyer toute une chaine de caractère avec aller à la ligne.
 */
void printlnString( const char * );

/**
 * @ingroup println
 * @fn void printlnShort( short )
 * @brief Permet d'envoyer un short
 * @param entier Le nombre a envoyer
 * Cette fonction permet d'envoyer un nombre codé sur 1 octet et signé et avec retour automatique à la ligne
 */
void printlnShort( short );

/**
 * @ingroup println
 * @fn void printlnUShort( unsigned short )
 * @brief Permet d'envoyer un unsigned short
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 1 octet, non signé et avec retour automatique à la ligne.
 */
void printlnUShort( unsigned short );

/**
 * @ingroup println
 * @fn void printlnInt( int )
 * @brief Permet d'envoyer un int
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 2 octet, signé et avec retour automatique à la ligne.
 */
void printlnInt( int );

/**
 * @ingroup println
 * @fn void printlnUInt( unsigned int )
 * @brief Permet d'envoyer un unsigned int
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 2 octet, non signé et avec retour automatique à la ligne.
 */
void printlnUInt( unsigned int );

/**
 * @ingroup println
 * @fn void printlnLong( long )
 * @brief Permet d'envoyer un long
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 4 octet, signé et avec retour automatique à la ligne.
 */
void printlnLong( long );

/**
 * @ingroup println
 * @fn void printlnULong( unsigned long )
 * @brief Permet d'envoyer un unsigned long
 * @param entier Le nombre à envoyer
 * Cette fonction permet d'envoyer un ombre codé sur 4 octet, non signé et avec retour automatique à la ligne.
 */
void printlnULong( unsigned long );

/**
 * @ingroup println
 * @fn void printlnChar( unsigned char )
 * @brief Permet d'envoyer un caratère avec un retour à la ligne
 * @param c Le caractère à envoyer
 */
void printlnChar( unsigned char );

//Réception des données
/**
 * @ingroup reception
 * @fn uint8_t available( void )
 * @brief Permet de savoir si des DATA ont été reçues
 * @return 0 si pas de DATA, autre choses sinon.
 */
uint8_t available(void);

/**
 * @ingroup reception
 * @ingroup inline
 * @fn inline void store_char( unsigned char, struct ring_buffer *)
 * @brief Permet de stocker une DATA reçue dans le ring buffer
 * @param c la DATE reçue (1 octet)
 * @param *rx_buffer un pointeur vers le ring buffer
 */
inline void store_char(unsigned char, struct ring_buffer *);

/**
 * @ingroup reception
 * @fn int read( void )
 * @brief Permet à l'utilisateur de récupérer les DATA reçues
 * @return La DATA stockée dans le buffer circulaire
 */
int read(void);

#endif
