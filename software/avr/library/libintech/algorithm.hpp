#ifndef ALGORITHM_HPP
#define ALGORITHM_HPP
#include "ring_buffer.hpp"

template<typename T,uint16_t BUFFER_SIZE>
void bubble_sort(ring_buffer<T,BUFFER_SIZE> & buff)
{
  T* buffer = buff.data();
  for(uint16_t i=0;i<BUFFER_SIZE;i++)
  {
	for(uint16_t j=0;j<i;j++)
	{
		if(buffer[i]>buffer[j])
		{
			T temp=buffer[i];
			buffer[i]=buffer[j];
			buffer[j]=temp;
		}
	  }
  }
}

template<typename T,uint16_t BUFFER_SIZE>
uint16_t mediane(ring_buffer<T,BUFFER_SIZE> & buff){
  bubble_sort(buff);
  return buff.data()[buff.current()];
}

#endif