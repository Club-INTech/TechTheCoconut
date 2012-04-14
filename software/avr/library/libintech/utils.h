#ifndef UTILS_H
#define UTILS_H

#define sbi(port,bit) (port) |= (1 << (bit))
#define cbi(port,bit) (port) &= ~(1 << (bit))

template<class T>
T max(T a, T b){
	if(a>b){
		return a;
	}
	return b;
}

template<class T>
T min(T a, T b){
	if(a<b){
		return a;
	}
	return b;
}

#endif