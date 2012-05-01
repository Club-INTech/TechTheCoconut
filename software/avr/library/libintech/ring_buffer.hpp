#ifndef RING_BUFFER_HPP
#define RING_BUFFER_HPP

#include "serial/serial_0.hpp"

template<typename T,uint16_t BUFFER_SIZE>
class ring_buffer {
private:
    T buffer[BUFFER_SIZE];
    uint16_t current_element;
public:
    typedef T value_type;
    
    ring_buffer() : current_element(0) {
    }
  
    ~ring_buffer() { }

    void append(T value) {
	current_element++;
        if(current_element == BUFFER_SIZE) {
            current_element = 0;
        }
        buffer[current_element] = value;
    }
    
    uint16_t size(){
      return BUFFER_SIZE;
    }
    
    T* data(){
      return buffer;
    }

    uint16_t current() {
        return current_element;
    }
}; 

#endif