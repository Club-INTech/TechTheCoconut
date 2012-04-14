#ifndef _PORTTYPES
#define _PORTTYPES
/*****************************************************************************/

typedef unsigned char   byte;           // 8-bit unsigned integer
typedef          char   sbyte;          // 8-bit integer
typedef unsigned short  word;           // 16-bit unsigned integer
typedef short           sword;          // 16-bit integer
typedef	unsigned long   dword;          // 32-bit unsigned integer
typedef	long		    sdword;         // 32-bit integer

typedef unsigned short  UINT;           // 16-bit unsigned integer
typedef	unsigned long   _ULONG;         // 32-bit unsigned long
typedef	unsigned short  _USHORT;        // 16-bit unsigned short
typedef	         long   _LONG;          // 32-bit signed long
typedef	unsigned char   _BOOL;          //  8-bit unsigned char
typedef unsigned long   DWORD;          // 32-bit unsigned long
typedef long            SDWORD;         // 32-bit signed long
typedef unsigned short  WORD;           // 16-bit unsigned short
typedef short           SWORD;          // 16-bit signed short
typedef unsigned char   _UCHAR;         //  8-bit unsigned long
typedef char            _CHAR;          //  7-bit signed long

typedef unsigned char  BYTE;
typedef unsigned int   BOOL;

#ifndef FALSE
#define FALSE   (0)
#endif

#ifndef TRUE
#define TRUE    (1)
#endif
#endif //_PORTTYPES
