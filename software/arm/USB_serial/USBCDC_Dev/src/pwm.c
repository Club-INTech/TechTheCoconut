#include "LPC17xx.h"
#include "pwm.h"

unsigned int PWM_Init()
{

//	LPC_PINCON->PINSEL4 = 0x00001555;	/* set GPIOs for all PWM pins on PWM */
	LPC_PINCON->PINSEL3 &= ~(0x3 << 8);
	LPC_PINCON->PINSEL3 |= (0x2 << 8);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 10);
	LPC_PINCON->PINSEL3 |= (0x2 << 10);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 14);
	LPC_PINCON->PINSEL3 |= (0x2 << 14);

	LPC_PWM1->TCR = TCR_RESET;	/* Counter Reset */ 
	LPC_PWM1->PR = 0x00;		/* count frequency:Fpclk */

	LPC_PWM1->MR0 = PWM_CYCLE;		/* set PWM cycle */
	LPC_PWM1->MR1 = PWM_CYCLE * 1/2;
	LPC_PWM1->MR2 = PWM_CYCLE * 1/2;
	LPC_PWM1->MR3 = PWM_CYCLE * 1/2;
	LPC_PWM1->MR4 = PWM_CYCLE * 1/2;
	LPC_PWM1->MR5 = PWM_CYCLE * 1/2;
	LPC_PWM1->MR6 = 0;

	LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN ;

  return 1;
}

void PWM_Start( )
{
	LPC_PWM1->PCR = PWMENA2 | PWMENA3 | PWMENA4 ;
	LPC_PWM1->TCR = TCR_CNT_EN | TCR_PWM_EN;
  return;
}

void PWM_Stop(  )
{
	LPC_PWM1->PCR = 0;
	LPC_PWM1->TCR = 0x00;
  return;
}

void PWM_Update( unsigned int ChannelNum, unsigned int offset)
{
  if ( ChannelNum == VERT )
  {
		LPC_PWM1->MR2 = PWM_CYCLE * 1/2 + offset;
	LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN ;
  }
  if ( ChannelNum == BLEU )
  {
		LPC_PWM1->MR3 = PWM_CYCLE * 1/2 + offset;
  		LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN;
  }
  if ( ChannelNum == ROUGE )
  {
	  	LPC_PWM1->MR4 = PWM_CYCLE * 1/2 + offset;
  		LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN ;
  }
  return;
}
