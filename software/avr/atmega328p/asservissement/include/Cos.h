#ifndef _FP_COS_H_
#define _FP_COS_H_

#include <math.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#define ABS(x) (x > 0 ? x : -x)
#define FP_PI 205887
#define FP_PI_OVER_TWO 102944
#define FP_TWO_PI 411775

#define CONVERSION_INT 65536
#define CONVERSION_FLOAT 65536.

#define TABLE_LENGTH 256
#define TABLE_STEP 402//.160757


float cos_table (float angle_rad);
float sin_table (float angle_rad);
float tan_table (float angle_rad);

int32_t fp_cos(int32_t theta);
int32_t fp_sin(int32_t theta);
int32_t fp_tan(int32_t theta);

int32_t fp_mult(int32_t a, int32_t b);
int32_t fp_div(int32_t a, int32_t b);

#endif