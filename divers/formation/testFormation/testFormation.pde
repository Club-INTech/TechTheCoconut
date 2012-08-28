/*
Programme de validation de la carte de la formation.

Test des servo moteurs : OK
Test des capteurs optiques : OK
Test du PWM : OK
Test de la direction : OK

*/

//Chargement de la lib servomoteur
#include <Servo.h> 

//Define de mes entrées -- Sorties
#define LED1 13
#define LED2 12

#define SERVO1 9
#define SERVO2 10
#define SERVO3 11

#define CAPTEURD 6 //Droite
#define CAPTEURG 8 //Gauche

#define VITESSE 5
#define SENS 4
#define COURANT 15

#define GAUCHE 30
#define DROITE 150


//Variable Servo moteur
Servo myservo1; //Direction
Servo myservo2;
Servo myservo3;

int volant = 90; //Variable du volant en degrès (90 = tout droit)

//Fonction d'initialisation exécuté une fois au début du programme
void setup() {
  
  //Définition des sorties :
  pinMode(SENS, OUTPUT); 
  pinMode(LED1, OUTPUT);  
  pinMode(LED2, OUTPUT);
  pinMode(VITESSE, OUTPUT);
  
  //Attach des servos moteurs :
  myservo1.attach(SERVO1);
  myservo2.attach(SERVO2);
  myservo3.attach(SERVO3);
  
  //Définition des sorties :
  pinMode(CAPTEURG, INPUT);
  pinMode(CAPTEURD, INPUT);
 
  //Init direction
  myservo1.write(volant); // Tout droit chauffeur ;)
  
  //Démarrage du moteur
  analogWrite(VITESSE,200); // VROUMMMMMMM !
 
}

//Boucle infinie
void loop()
{
  //Test des capteurs avec les LEDs de contrôle => Led allumée quand on est sur la ligne noire
  digitalWrite(LED1,digitalRead(CAPTEURG));
  digitalWrite(LED2,digitalRead(CAPTEURD));
  
  //Correction de la trajectoire
  volant = volant - digitalRead(CAPTEURG)*5 + digitalRead(CAPTEURD)*5;
  myservo1.write(volant);
  
  delay(20);
  
  //Limite de débatement du volant
  if(volant<GAUCHE)volant = GAUCHE;
  if(volant>DROITE)volant = DROITE;
}
