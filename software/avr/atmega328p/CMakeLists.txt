include(atmega328p.cmake)
set(MICROCONTROLEURS actionneurs_arduino asservissement compteur capteurs tests balise_adverse table_maker print_serial)
add_microcontrolers(m328p "${MICROCONTROLEURS}")
