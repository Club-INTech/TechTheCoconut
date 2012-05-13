#define pa 10
#define pb 11
#define top 6

#define PERIOD 60 //1000/17Hz

int cmd = 10;//commande de départ

void setup(){
  pinMode(pa, OUTPUT);
  pinMode(pb, OUTPUT);
  pinMode(top, INPUT);
  Serial.begin(9600);

  digitalWrite(pa,LOW);
  analogWrite(pb,cmd);
}


void loop(){
  if(digitalRead(2)==HIGH){
    long total=0;
    long period=0;
    
    total+=pulseIn(top,LOW);
    total+=pulseIn(top,HIGH);
    period = total/1000.;
    
    if((period>PERIOD && cmd<250) || period==0) //0=timeout
      cmd++;
    if(period<PERIOD && cmd>0)
      cmd-=1;  
    
    analogWrite(pb,cmd);
    Serial.println(cmd);
    Serial.println(period);
    delay(300);
  }
}