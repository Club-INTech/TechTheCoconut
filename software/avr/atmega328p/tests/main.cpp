#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
// #include <libintech/timer.hpp>
// #include <util/delay.h>
//  #include <libintech/serial/serial_1.hpp>
//  #include <libintech/serial/serial_2.hpp>
//  #include <libintech/serial/serial_3.hpp>
int main(){
//   Timer<1,ModeCounter,64>::init();
//   Serial<1> & serial1 = Serial<1>::Instance();
//   Serial<2> & serial2 = Serial<2>::Instance();
//   Serial<3> & serial3 = Serial<3>::Instance();

//  int i=0;
  Serial<0>::init();
  Serial<0>::change_baudrate(9600);
  sei();
  unsigned char trame[4] = {0};
  unsigned long res;
  while(1){
//       Serial<0>::read(trame,4);
      res = Serial<0>::read_int();
      Serial<0>::print(res);
//       Serial<0>::print_binary(trame,4);
//       Serial<0>::print("\n");
   // _delay_ms(500);
//    serial0.print(counter.value());

//     serial1.print(0);
//     serial2.print(0);
//     serial3.print(0);
  }
}

/*
ISR(TIMER1_OVF_vect, ISR_NOBLOCK){
    Serial<0>::print(TCNT1);
}*/
