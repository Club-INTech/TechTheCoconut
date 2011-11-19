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

#define CAPTEUR1 6
#define CAPTEUR2 8

#define VITESSE 5
#define SENS 4
#define COURANT 15


//Variable Servo moteur
Servo myservo1;
Servo myservo2;
Servo myservo3;

int ledState = LOW;             // ledState used to set the LED
long previousMillis = 0;        // will store last time LED was updated

// the follow variables is a long because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long interval = 2000;           // interval at which to blink (milliseconds)



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
  pinMode(CAPTEUR1, INPUT);
  pinMode(CAPTEUR2, INPUT);
}

//Boucle infinie
void loop()
{
  unsigned long currentMillis = millis();
 
  if(currentMillis - previousMillis > interval) {
    // save the last time you blinked the LED 
    previousMillis = currentMillis;   

    // if the LED is off turn it on and vice-versa:
    if (ledState == LOW)
    {
      ledState = HIGH;
      analogWrite(VITESSE,64);
      myservo1.write(0);
      myservo2.write(180);
      myservo3.write(180);
    }
    else
    {
      ledState = LOW;
      analogWrite(VITESSE,200);
      myservo1.write(180);
      myservo2.write(0);
      myservo3.write(0);
    }

    // set the LED with the ledState of the variable:
    digitalWrite(SENS, ledState);
  }
  digitalWrite(LED1, digitalRead(CAPTEUR1));
  digitalWrite(LED2, digitalRead(CAPTEUR2));
  
}

