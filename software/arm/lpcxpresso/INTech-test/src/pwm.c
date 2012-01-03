#include "LPC17xx.h"
#include "pwm.h"

int pwm_rouge=0, pwm_bleu=0, pwm_vert=0;
unsigned char pwm_pulse = 0;

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
		pwm_vert = offset+600;
		LPC_PWM1->MR2 = PWM_CYCLE * 1/2 + offset;
		LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN ;
	}
	if ( ChannelNum == BLEU )
	{
		pwm_bleu = offset + 600;
		LPC_PWM1->MR3 = PWM_CYCLE * 1/2 + offset;
		LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN;
	}
	if ( ChannelNum == ROUGE )
	{
		pwm_rouge = offset + 600;
		LPC_PWM1->MR4 = PWM_CYCLE * 1/2 + offset;
		LPC_PWM1->LER = LER0_EN | LER2_EN | LER3_EN | LER4_EN ;
	}
	return;
}

void PWM_pulse_update(unsigned char channel)
{
	if( (pwm_pulse & (1<<ROUGE)) && (channel == ROUGE))
	{
		if( pwm_pulse & (1<<PULSE_ROUGE))
		{
			if( pwm_rouge == 1200)
			{
				pwm_rouge--;
				pwm_pulse &= ~(1 << PULSE_ROUGE );
				PWM_Update(ROUGE,pwm_rouge-600);
			}
			else
			{
				pwm_rouge++;
				PWM_Update(ROUGE,pwm_rouge-600);
			}
		}
		else
		{
			if( pwm_rouge == 0)
			{
				pwm_rouge++;
				pwm_pulse |= (1 << PULSE_ROUGE );
				PWM_Update(ROUGE,pwm_rouge-600);
			}
			else
			{
				pwm_rouge--;
				PWM_Update(ROUGE,pwm_rouge-600);
			}
		}
	}
	if( (pwm_pulse & (1<<BLEU)) && (channel == BLEU))
	{
		if( pwm_pulse & (1<<PULSE_BLEU))
		{
			if( pwm_bleu == 1200)
			{
				pwm_bleu--;
				pwm_pulse &= ~(1 << PULSE_BLEU );
				PWM_Update(BLEU,pwm_bleu-600);
			}
			else
			{
				pwm_bleu++;
				PWM_Update(BLEU,pwm_bleu-600);
			}
		}
		else
		{
			if( pwm_bleu == 0)
			{
				pwm_bleu++;
				pwm_pulse |= (1 << PULSE_BLEU );
				PWM_Update(BLEU,pwm_bleu-600);
			}
			else
			{
				pwm_bleu--;
				PWM_Update(BLEU,pwm_bleu-600);
			}
		}
	}
	if( (pwm_pulse & (1<<VERT)) && (channel == VERT))
	{
		if( pwm_pulse & (1<<PULSE_VERT))
		{
			if( pwm_vert == 1200)
			{
				pwm_vert--;
				pwm_pulse &= ~(1 << PULSE_VERT );
				PWM_Update(VERT,pwm_vert-600);
			}
			else
			{
				pwm_vert++;
				PWM_Update(VERT,pwm_vert-600);
			}
		}
		else
		{
			if( pwm_vert == 0)
			{
				pwm_vert++;
				pwm_pulse |= (1 << PULSE_VERT );
				PWM_Update(VERT,pwm_vert-600);
			}
			else
			{
				pwm_vert--;
				PWM_Update(VERT,pwm_vert-600);
			}
		}
	}
}

void PWM_pulse(unsigned int channel, unsigned int etat)
{
	if ( channel == VERT )
	{
		if( etat == 0 )
			pwm_pulse &= ~(1<<VERT);
		else
			pwm_pulse |= (1<<VERT);
	}
	if ( channel == BLEU )
	{
		if( etat == 0 )
			pwm_pulse &= ~(1<<BLEU);
		else
			pwm_pulse |= (1<<BLEU);
	}
	if ( channel == ROUGE )
	{
		if( etat == 0 )
			pwm_pulse &= ~(1<<ROUGE);
		else
			pwm_pulse |= (1<<ROUGE);
	}
	return;
}
