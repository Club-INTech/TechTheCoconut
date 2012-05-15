//We always have to include the library
#include "LedControl.h"

/*
 By Fabien BERNARD
 
 Configuration : 
 pin 12 is connected to the DataIn 
 pin 11 is connected to the CLK 
 pin 10 is connected to LOAD 
 We have four MAX7219.
 */
LedControl lc=LedControl(12,11,10,4);

/* we always wait a bit between updates of the display */
unsigned long delaytime=30;

void setup() {
  /*
   The MAX72XX is in power-saving mode on startup,
   
   */
   for(int addr=0;addr<=3;addr++)
   {
    // we have to do a wakeup call
    lc.shutdown(addr,false);
    
    // Set the brightness to a maximum value
    lc.setIntensity(addr,15);
    
    // and clear the display
    lc.clearDisplay(addr); 
    
    // and set size off matrix
    lc.setScanLimit(addr, 6);
   }
}

/*
 This method will display the characters for the
 word "Arduino" one after the other on the matrix. 
 (you need at least 5x7 leds to see the whole chars)
 */
void writeArduinoOnMatrix() {
  /* here is the data for the characters */
  byte a[5]={B01111110,B10001000,B10001000,B10001000,B01111110};
  byte r[5]={B00111110,B00010000,B00100000,B00100000,B00010000};
  byte d[5]={B00011100,B00100010,B00100010,B00010010,B11111110};
  byte u[5]={B00111100,B00000010,B00000010,B00000100,B00111110};
  byte i[5]={B00000000,B00100010,B10111110,B00000010,B00000000};
  byte n[5]={B00111110,B00010000,B00100000,B00100000,B00011110};
  byte o[5]={B00011100,B00100010,B00100010,B00100010,B00011100};

  /* now display them one by one with a small delay */
  lc.setRow(1,0,a[0]);
  lc.setRow(1,1,a[1]);
  lc.setRow(1,2,a[2]);
  lc.setRow(1,3,a[3]);
  lc.setRow(1,4,a[4]);
  delay(delaytime);
  lc.setRow(1,0,r[0]);
  lc.setRow(1,1,r[1]);
  lc.setRow(1,2,r[2]);
  lc.setRow(1,3,r[3]);
  lc.setRow(1,4,r[4]);
  delay(delaytime);
  lc.setRow(1,0,d[0]);
  lc.setRow(1,1,d[1]);
  lc.setRow(1,2,d[2]);
  lc.setRow(1,3,d[3]);
  lc.setRow(1,4,d[4]);
  delay(delaytime);
  lc.setRow(1,0,u[0]);
  lc.setRow(1,1,u[1]);
  lc.setRow(1,2,u[2]);
  lc.setRow(1,3,u[3]);
  lc.setRow(1,4,u[4]);
  delay(delaytime);
  lc.setRow(1,0,i[0]);
  lc.setRow(1,1,i[1]);
  lc.setRow(1,2,i[2]);
  lc.setRow(1,3,i[3]);
  lc.setRow(1,4,i[4]);
  delay(delaytime);
  lc.setRow(1,0,n[0]);
  lc.setRow(1,1,n[1]);
  lc.setRow(1,2,n[2]);
  lc.setRow(1,3,n[3]);
  lc.setRow(1,4,n[4]);
  delay(delaytime);
  lc.setRow(1,0,o[0]);
  lc.setRow(1,1,o[1]);
  lc.setRow(1,2,o[2]);
  lc.setRow(1,3,o[3]);
  lc.setRow(1,4,o[4]);
  delay(delaytime);
  lc.setRow(1,0,0);
  lc.setRow(1,1,0);
  lc.setRow(1,2,0);
  lc.setRow(1,3,0);
  lc.setRow(1,4,0);
  delay(delaytime);
}
void K2000()
{
  // Aller
  for(int addr=0;addr<=3;addr++)
    {
      for (int row=0;row<7;row++)
      {
        lc.setRow(addr,row,B11111111);
        delay(delaytime);
        lc.setRow(addr,row,(byte)0);
      }
  }
  
  // Retour
  for(int addr=3;addr>=0;addr--)
  {
    for (int row=6;row>=0;row--)
    {
      lc.setRow(addr,row,B11111111);
      delay(delaytime);
      lc.setRow(addr,row,(byte)0);
    }
  }
}

void cylon()
{
  //Aller (de gauche à droite)
  for(int i=0;i<14;i++)
  {
     if(i<7) //MAX 01 & 04
     {
       //Switch ON
       lc.setRow(0,i,B11111111);
       lc.setRow(3,6-i,B11111111);
       //2eme colonne
       lc.setRow(0,i+1,B11111111);
       lc.setRow(3,6-i+1,B11111111);
       delay(delaytime*i/3);
       
       //Switch OFF
       lc.setRow(0,i,(byte)0);
       lc.setRow(3,6-i,(byte)0);
       //2eme colonne
       lc.setRow(0,i+1,(byte)0);
       lc.setRow(3,6-i+1,(byte)0);
     }
     else //MAX 02 & 03
     {
       //Switch ON
        lc.setRow(1,i-7,B11111111);
        lc.setRow(2,13-i,B11111111);
        //2eme colonne
        lc.setRow(1,i-7+1,B11111111);
        lc.setRow(2,13-i+1,B11111111);
        delay(delaytime*(i-7)/3);
        
        //Switch OFF
        lc.setRow(1,i-7,(byte)0);
        lc.setRow(2,13-i,(byte)0);
        //2eme colonne
        lc.setRow(1,i-7+1,(byte)0);
        lc.setRow(2,13-i+1,(byte)0);
     }
  }
  
  //Retour (de droite à gauche)
  for(int i=14;i>=0;i--)
  {
     if(i<7) //MAX 01 & 04
     {
       //Switch ON
       lc.setRow(0,i,B11111111);
       lc.setRow(3,6-i,B11111111);
       //2eme colonne
       lc.setRow(0,i+1,B11111111);
       lc.setRow(3,6-i+1,B11111111);
       delay(delaytime*i/3);
       
       //Switch OFF
       lc.setRow(0,i,(byte)0);
       lc.setRow(3,6-i,(byte)0);
       //2eme colonne
       lc.setRow(0,i+1,(byte)0);
       lc.setRow(3,6-i+1,(byte)0);
     }
     else //MAX 02 & 03
     {
       //Switch ON
        lc.setRow(1,i-7,B11111111);
        lc.setRow(2,13-i,B11111111);
        //2eme colonne
        lc.setRow(1,i-7+1,B11111111);
        lc.setRow(2,13-i+1,B11111111);
        delay(delaytime*(i-7)/3);
        
        //Switch OFF
        lc.setRow(1,i-7,(byte)0);
        lc.setRow(2,13-i,(byte)0);
        //2eme colonne
        lc.setRow(1,i-7+1,(byte)0);
        lc.setRow(2,13-i+1,(byte)0);
     }
  }
}
void balayageH()
{
  // Aller
  for(int addr=0;addr<=3;addr++)
    {
      for (int row=0;row<7;row++)
      {
        lc.setRow(addr,row,B11111111);
        delay(delaytime);
        //lc.setRow(addr,row,(byte)0);
      }
  }
  
  // Retour
  for(int addr=3;addr>=0;addr--)
  {
    for (int row=6;row>=0;row--)
    {
      //lc.setRow(addr,row,B11111111);
      delay(delaytime);
      lc.setRow(addr,row,(byte)0);
    }
  }
}

void balayageV()
{
  // Aller
  for(int addr=0;addr<=3;addr++)
    {
      for (int row=0;row<7;row++)
      {
        lc.setColumn(addr,row,B11111111);
        delay(delaytime);
        //lc.setRow(addr,row,(byte)0);
      }
  }
  
  // Retour
  for(int addr=3;addr>=0;addr--)
  {
    for (int row=6;row>=0;row--)
    {
      //lc.setRow(addr,row,B11111111);
      delay(delaytime);
      lc.setColumn(addr,row,(byte)0);
    }
  }
}

void loop() 
{ 
  //balayageV();
  //K2000(); 
 cylon(); 
}
