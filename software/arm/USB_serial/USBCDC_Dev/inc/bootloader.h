
//#include <cr_section_macros.h>

/*place buffer in section .ram2*/
//static unsigned char boot_buffer[5] __attribute__ ((section (".ram2")))={0};
static unsigned char * boot_buffer = (unsigned char *)0x2007C000;

//static unsigned char boot_flag01;
//static unsigned char boot_flag02;
//static unsigned char boot_flag03;
//static unsigned char boot_flag04;
