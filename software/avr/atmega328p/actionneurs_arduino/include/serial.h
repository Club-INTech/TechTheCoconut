#ifndef SERIAL_H_
#define SERIAL_H_

#include <avr/io.h>
#include <avr/interrupt.h>

#include "actionneurs.h"

#define RX_BUFFER_SIZE 32
struct ring_buffer
{
    unsigned char buffer[RX_BUFFER_SIZE];
    int head;
    int tail;
};

#define UBRR (F_CPU/8/BAUD_RATE_SERIE - 1)/2


//Fonction de base de la liaison série
/**
 * @fn void uart_init( void )
 * @brief Initialisation de la liaison série
 */
void uart_init(void);


/**
 * @ingroup inline
 * @fn inline void uart_send_ln( void )
 * @brief Permet d'envoyer un retour chariot
 */
inline void uart_send_ln( void );

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
 * @fn inline void uart_send_char( unsigned char )
 * @brief Permet d'envoyer un char par la liaison série
 * Cette fonction est plus une fonction utilisée pour la librairie elle-même (genre de private)
 * @param byte Correspond à l'octet à envoyer.
 */
inline void uart_send_char(unsigned char);

/**
 * @ingroup inline
 * @fn inline void uart_send_string( const char *)
 * @brief Permet d'envoyer toute une chaine de caractère
 * @param string Le pointeur vers la chaine de caractère à envoyer
 */
inline void uart_send_string(const char *);


/**
 * @ingroup println
 * @fn void printlnString( const char *)
 * @brief Permet d'envoyer une chaine de caractère
 * @param string Le pointeur vers la chaine de caractère à envoyer
 * Fonction qui permet d'envoyer toute une chaine de caractère avec aller à la ligne.
 */
void printlnString( const char * );

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
 * @fn unsigned char uart_recv_char( void )
 * @brief Réception bloquante d'un unsigned char
 * @return Le char reçu par la liaison série
 */
unsigned char uart_recv_char(void);


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
 * @fn int read( void )
 * @brief Permet à l'utilisateur de récupérer les DATA reçues
 * @return La DATA stockée dans le buffer circulaire
 */
int read(void);

inline long readLongNumber( void );










void print(const char * val);

#endif