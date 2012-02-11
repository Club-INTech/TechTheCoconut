#ifndef SINGLETON_HPP
#define SINGLETON_HPP

template<class T>
class Singleton{
public:
  static T& Instance(){
    static T instance;
    return instance;
  }
protected:
  Singleton(){ }
};

__extension__ typedef int __guard __attribute__((mode (__DI__)));

extern "C" int __cxa_guard_acquire(__guard *);
extern "C" void __cxa_guard_release (__guard *);
extern "C" void __cxa_guard_abort (__guard *);

#endif