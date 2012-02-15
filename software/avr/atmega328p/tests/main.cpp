#include <libintech/serial/serial_0.hpp>
#include <libintech/timer.hpp>
#include <util/delay.h>
//  #include <libintech/serial/serial_1.hpp>
//  #include <libintech/serial/serial_2.hpp>
//  #include <libintech/serial/serial_3.hpp>
int main(){
  Serial<0> & serial0 = Serial<0>::Instance();
  Timer<1,ModeCounter,64> counter;
//   Serial<1> & serial1 = Serial<1>::Instance();
//   Serial<2> & serial2 = Serial<2>::Instance();
//   Serial<3> & serial3 = Serial<3>::Instance();

 int i=0;
  while(1){
   // _delay_ms(500);
//    serial0.print(counter.value());

//     serial1.print(0);
//     serial2.print(0);
//     serial3.print(0);
  }
}


ISR(TIMER1_OVF_vect, ISR_NOBLOCK){
    Serial<0> & serial0 = Serial<0>::Instance();
    serial0.print(TCNT1);
}
