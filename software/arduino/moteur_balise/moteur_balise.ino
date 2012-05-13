#define p1 10
#define p2 11
#define top 6
#define pinEnable 2

#define PERIOD 60 //1000/17Hz

int cmd = 65;//commande de départ

void setup(){
  pinMode(p1, OUTPUT);
  pinMode(p2, OUTPUT);
  pinMode(top, INPUT);
  pinMode(pinEnable,INPUT);
  Serial.begin(9600);

  digitalWrite(p1,LOW);
  analogWrite(p2,cmd);
}

void loop(){

  /*long total=0;
  long period=0;
  
  total+=pulseIn(top,LOW);
  total+=pulseIn(top,HIGH);
  period = total/1000.;*/
  
  if(digitalRead(pinEnable)==HIGH)
  {
    //Commande fixe
     analogWrite(p2,cmd);
      /*Asservissement
    if((period>PERIOD && cmd<250) || period==0) //0=timeout
      cmd++;
    if(period<PERIOD && cmd>0)
      cmd-=1;  
    
    analogWrite(p2,cmd);
    Serial.println(cmd);*/
  }
  else
  {
     analogWrite(p2,0); 
  }
 /*
  Serial.println(period);
  delay(300);*/
}
