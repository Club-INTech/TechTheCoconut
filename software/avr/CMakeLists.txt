cmake_minimum_required(VERSION 2.8)

set(LIBRARY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/library)
#aux_source_directory(${LIBRARY_DIR}/libintech LIBINTECH_SRC)
#add_library(intech STATIC ${LIBINTECH_SRC})
include_directories(${LIBRARY_DIR})
macro(add_microcontrolers MMCU MICROCONTROLEURS)
    foreach(MICROCONTROLEUR ${MICROCONTROLEURS})
        include_directories(${CMAKE_CURRENT_SOURCE_DIR}/${MICROCONTROLEUR}/include)
        set(${MICROCONTROLEUR}_SRC)
        AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/${MICROCONTROLEUR}/src ${MICROCONTROLEUR}_SRC)
        AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/${MICROCONTROLEUR}/ ${MICROCONTROLEUR}_SRC)
        set_directory_properties(PROPERTIES ADDITIONAL_MAKE_CLEAN_FILES ${MICROCONTROLEUR}.hex)

        add_executable(${MICROCONTROLEUR}.out ${${MICROCONTROLEUR}_SRC} ${LIBRARY_DIR}/libintech/avr_cpp_compatibility.cpp)
# 	set(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "")
	target_link_libraries(${MICROCONTROLEUR}.out c m c)
	set_target_properties(${MICROCONTROLEUR}.out PROPERTIES LINKER_LANGUAGE CXX)
        

	add_custom_target(${MICROCONTROLEUR}.hex ALL DEPENDS ${MICROCONTROLEUR}.out)
        add_custom_command(TARGET ${MICROCONTROLEUR}.hex
                            COMMAND avr-objcopy 
                            ARGS -O ihex -R .eeprom ${MICROCONTROLEUR}.out ${MICROCONTROLEUR}.hex
                            )
        add_custom_target(upload_${MICROCONTROLEUR} DEPENDS ${MICROCONTROLEUR}.hex)
        add_custom_command(	TARGET upload_${MICROCONTROLEUR}
                            COMMAND avrdude
                            ARGS -c usbasp -p ${MMCU} -U  flash:w:${MICROCONTROLEUR}.hex)
   endforeach()
endmacro()

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/atmega324p)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/atmega328p)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/atmega1280)
