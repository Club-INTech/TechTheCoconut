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
Exemple
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
  //Aller
  for(int col=0; col<=13 ; col++)
  {
    lc.setEyeColumn(1,col,B11111111,true); //Switch ON
    lc.setEyeColumn(1,col+1,B11111111,true);
    if(col<7)
    delay(delaytime*col/3);
    else
    delay(delaytime*(13-col)/3);
    lc.setEyeColumn(1,col,(byte)0,true); //Switch OFF
    lc.setEyeColumn(1,col+1,(byte)0,true);
  }
  
  //Retour
  for(int col=13; col>=0 ; col--)
  {
    lc.setEyeColumn(1,col,B11111111,true); //Switch ON
    lc.setEyeColumn(1,col-1,B11111111,true);
    if(col<7)
    delay(delaytime*col/3);
    else
    delay(delaytime*(13-col)/3);
    lc.setEyeColumn(1,col,(byte)0,true); //Switch OFF
    lc.setEyeColumn(1,col-1,(byte)0,true);
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
  for(int eye=1 ; eye<=2 ; eye++)
    {
      for (int col=0;col<=13;col++)
      {
        lc.setEyeColumn(eye,col,B11111111,0);
        delay(delaytime);
        //lc.setEyeColumn(eye,col,(byte)0,0);
      }
  }
  
   // Retour
  for(int eye=2 ; eye>0 ; eye--)
    {
      for (int col=13;col>=0;col--)
      {
        lc.setEyeColumn(eye,col,B11111111,0);
        delay(delaytime);
        //lc.setEyeColumn(eye,col,(byte)0,0);
      }
  }
}

void animationyeux()
{
   int i,j;
   byte sprite[4]={B00111100,B00111100,B00111100,B00111100};
   int pos[4]={1,2,3,4};
   
   for (i=0 ; i < 10 ; i++)
     {
         for (j=0 ; j<4 ; j++)
         {
           lc.setEyeColumn(1,pos[j],sprite[j],0);
         } 
      delay(30);
        lc.setEyeColumn(1,pos[1]-1,(byte)0,0);
        for (j=0 ; j < 4 ; j++)
        {
          pos[j]+=i;
          
        }
        
   }
   
   for (i=0 ; i < 10 ; i++)
   {
     for (j=0 ; j<4 ; j++)
         {
           lc.setEyeColumn(1,pos[j],sprite[j], 0);
         } 
      delay(30);
        lc.setEyeColumn(1,pos[4]+1,(byte)0,0);
        for (j=0 ; j < 4 ; j++)
        {
          pos[j]-=i;
          
        }
        
   }
}

void gauchedroite() // Oeil qui regarde de gauche à droite
{
   byte sprite[6]={B00111001,B01111101,B11000111,B11000111,B01111101,B00111001}; 
   byte clignement[6]={B00110001,B00110001,B00110001,B00110001,B00110001,B00110001};
   
   for(int tour=0; tour<4 ; tour++)
   {
     //Aller
     for (int i=0; i<8 ; i ++)
     {
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, sprite[col], false); 
           lc.setEyeColumn(2, col+i, sprite[col], false); 
        }
        delay(delaytime);
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, (byte)0, false); 
           lc.setEyeColumn(2, col+i, (byte)0, false); 
        } 
     }
     
     //Retour
     for (int i=8; i>=0 ; i--)
      {
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, sprite[col], false); 
           lc.setEyeColumn(2, col+i, sprite[col], false); 
        }
        delay(delaytime);
        if(i==0 || i==8) delay(delaytime*10);
        for (int col=0; col<6; col++)
        {
           lc.setEyeColumn(1, col+i, (byte)0, false); 
           lc.setEyeColumn(2, col+i, (byte)0, false); 
        } 
     }
   }
   
   //Arrêt au mileu
   for (int i=0; i<4 ; i ++)
   {
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+i, sprite[col], false); 
         lc.setEyeColumn(2, col+i, sprite[col], false); 
      }
      delay(delaytime);
      if(i==3) delay(1000); //Pause
      
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+i, (byte)0, false); 
         lc.setEyeColumn(2, col+i, (byte)0, false); 
      } 
   }
   
   //Clignement
   for (int tour=0; tour<2; tour ++)
   {
     for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+3, clignement[col], false); 
         lc.setEyeColumn(2, col+3, clignement[col], false);
      }
      delay(300);
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+3, (byte)0, false); 
         lc.setEyeColumn(2, col+3, (byte)0, false); 
         lc.setEyeColumn(1, col+3, sprite[col], false); 
         lc.setEyeColumn(2, col+3, sprite[col], false); 
      }
      delay(500);
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+3, (byte)0, false); 
         lc.setEyeColumn(2, col+3, (byte)0, false); 
      }
   } 
  
  //Continuation de l'animation pour reprendre la boucle
  for (int i=2; i>=0 ; i --)
   {
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+i, sprite[col], false); 
         lc.setEyeColumn(2, col+i, sprite[col], false); 
      }
      delay(delaytime);
      if(i==3) delay(1000); //Pause
      
      for (int col=0; col<6; col++)
      {
         lc.setEyeColumn(1, col+i, (byte)0, false); 
         lc.setEyeColumn(2, col+i, (byte)0, false); 
      } 
   }
}
void cercle() // by cassou
{
   byte sprite1[14]={B11111110,B11111110,B00000000,B11111110,B11111110,B11000110,B11010110,B11010110,B11000110,B11111110,B11111110,B00000000,B11111110,B11111110};
   byte sprite2[14]={B11111110,B00000000,B11111110,B11111110,B10000010,B10111010,B10111010,B10111010,B10111010,B10000010,B11111110,B11111110,B00000000,B11111110};
   byte sprite3[14]={B00000000,B11111110,B11111110,B00000000,B01111100,B01111100,B01101100,B01101100,B01111100,B01111100,B00000000,B11111110,B11111110,B00000000}; 
   
   for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, sprite1[col], true); 
    }
    delay(delaytime*4);
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true); 
       lc.setEyeColumn(1, col, sprite2[col], true); 
    } 
    delay(delaytime*4);
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true); 
       lc.setEyeColumn(1, col, sprite3[col], true); 
    } 
    delay(delaytime*4);
    for (int col=0; col<13; col++)
    {
       lc.setEyeColumn(1, col, (byte)0, true); 
    } 
}

void emoticon(int mode)
{
  byte love[14]={B00000000,B00000000,B00000000,B01100000,B11110000,B11111000,B01111100,B00111110,B01111100,B11111000,B11110000,B01100000,B00000000,B00000000}; 
  byte exptdr[14]={B11000110,B11000110,B11000110,B11000110,B11000110,B11101110,B11101110,B11101100,B01101100,B01101100,B01101100,B00111000,B00111000,B00111000};
  byte smiley[14]={B00000111,B00011111,B00111001,B01100001,B11100001,B11000001,B11000001,B11000001,B11000001,B01100001,B01100001,B00111001,B00011111,B00000111};
  byte disturbed[14]={B00011100,B00100010,B01001000,B10010100,B10100010,B10101010,B10101010,B10101010,B10101010,B10101010,B10101010,B10010010,B01000100,B00111000};
  byte doublenote[14]={B00000000,B00000000,B00000100,B00001110,B00001110,B11111110,B11000000,B11000000,B11000100,B11001110,B11001110,B11111110,B00000000,B00000000};
  byte KO[14]={B00000000,B00000000,B00000000,B10000010,B01000100,B00101000,B00010000,B00101000,B01000100,B10000010,B00000000,B00000000,B00000000,B00000000};
  
  for (int col=0; col<13; col++)
   {
     switch(mode)
     {
       case 1: //love
         lc.setEyeColumn(1, col, love[col], true); 
         break;
         
       case 2: //exptdr
         lc.setEyeColumn(1, col, exptdr[col], true); 
         break;
         
       case 3: //smiley
         lc.setEyeColumn(1, col, smiley[col], true); 
         break;
        
        case 4: //disturbed
          lc.setEyeColumn(1, col, disturbed[col], false); 
          lc.setEyeColumn(2, col, disturbed[col], false); 
          break;
          
         case 5: //doublenote
          lc.setEyeColumn(1, col, doublenote[col], false); 
          lc.setEyeColumn(2, col, doublenote[col], false); 
          break;
          
         case 6: //KO
           lc.setEyeColumn(1, col, KO[col], true); 
           break;
          
          
     }
   }
 
  delay(1000); // pause
  
  //ClearDisplay
  for (int col=0; col<13; col++)
  {
     lc.setEyeColumn(1, col, (byte)0, true);
  }  
}

void loop() 
{ 
  //balayageV();
  //K2000(); 
  //cylon();
  for(int i=1;i<7;i++)
  emoticon(i);
  //gauchedroite();
  //cercle(); //by cassou
  //animationyeux();
  //balayageV();
}
