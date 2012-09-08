include(atmega328p.cmake)
set(MICROCONTROLEURS actionneurs_arduino asservissement compteur capteurs balise_adverse table_maker print_serial mesure_impulsion infrarouges capteur_vieux jumper balise_adverse_4_fenetres balise_adverse_with_ntp ntp)
add_microcontrolers(m328p "${MICROCONTROLEURS}")
