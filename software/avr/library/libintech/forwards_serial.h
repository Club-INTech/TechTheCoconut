#ifndef FORWARDS_SERIAL_H_
#define FORWARDS_SERIAL_H_

template<uint8_t id>
class Serial{
public:
	
	static inline void change_baudrate(uint32_t BAUD_RATE);
	
	static inline void store_char(unsigned char c);
	
	template<class T>
	static inline void print(T val);
	
	static inline void print(char val);
	
	static inline void print(const char * val);
	template<class T>
	static inline T read(void);
	
	static inline float read();
	
	static inline uint8_t read(char* string, uint8_t length);
};


#endif /* FORWARDS_SERIAL_H_ */
