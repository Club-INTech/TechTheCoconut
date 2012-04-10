Project(Intech)
cmake_minimum_required(VERSION 2.8)
option(FOR_ARDUINO "Compile pour le quartz d'une carte arduino - 16MHz" OFF)
add_subdirectory(${CMAKE_SOURCE_DIR}/avr/)
