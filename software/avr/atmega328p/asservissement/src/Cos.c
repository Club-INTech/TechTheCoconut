#include "Cos.h"

/* fonctions de conversion de flottants permettant d'utiliser les calculs 
 * d'interpolations sur la table, se faisant exclusivement sur des entiers
 * Pi/2 rad => 102944 angle dans cette lib
 * 1 réel   => 65536 distance dans cette lib
 */

float cos_table (float angle_rad)
{
    //65536 = 102944/(PI/2), conversion radian <--> angle entier pour cette lib
    return fp_cos(int32_t (angle_rad* CONVERSION_INT ))/ CONVERSION_FLOAT;
}

float sin_table (float angle_rad)
{
    //65536 = 102944/(PI/2), conversion radian <--> angle entier pour cette lib
    return fp_sin(int32_t (angle_rad* CONVERSION_INT ))/ CONVERSION_FLOAT;
}

float tan_table (float angle_rad)
{
    //65536 = 102944/(PI/2), conversion radian <--> angle entier pour cette lib
    return fp_tan(int32_t (angle_rad* CONVERSION_INT ))/ CONVERSION_FLOAT;
}

////////////////////////////////////////////////////////////////////////////
static int32_t linspace[TABLE_LENGTH] PROGMEM = {
0,402,804,1206,1608,2010,2412,2814,
3216,3618,4020,4422,4824,5226,5628,6030,
6432,6834,7236,7638,8040,8442,8844,9246,
9648,10050,10452,10854,11256,11658,12060,12462,
12864,13266,13668,14070,14472,14874,15276,15678,
16080,16482,16884,17286,17688,18090,18492,18894,
19296,19698,20100,20502,20904,21306,21708,22110,
22512,22914,23316,23718,24120,24522,24924,25326,
25728,26130,26532,26934,27336,27738,28140,28542,
28944,29346,29748,30150,30552,30954,31356,31758,
32160,32562,32964,33366,33768,34170,34572,34974,
35376,35778,36180,36582,36984,37386,37788,38190,
38592,38994,39396,39798,40200,40602,41004,41406,
41808,42210,42612,43014,43416,43818,44220,44622,
45024,45426,45828,46230,46632,47034,47436,47838,
48240,48642,49044,49446,49848,50250,50652,51054,
51456,51858,52260,52662,53064,53466,53868,54270,
54672,55074,55476,55878,56280,56682,57084,57486,
57888,58290,58692,59094,59496,59898,60300,60702,
61104,61506,61908,62310,62712,63114,63516,63918,
64320,64722,65124,65526,65928,66330,66732,67134,
67536,67938,68340,68742,69144,69546,69948,70350,
70752,71154,71556,71958,72360,72762,73164,73566,
73968,74370,74772,75174,75576,75978,76380,76782,
77184,77586,77988,78390,78792,79194,79596,79998,
80400,80802,81204,81606,82008,82410,82812,83214,
83616,84018,84420,84822,85224,85626,86028,86430,
86832,87234,87636,88038,88440,88842,89244,89646,
90048,90450,90852,91254,91656,92058,92460,92862,
93264,93666,94068,94470,94872,95274,95676,96078,
96480,96882,97284,97686,98088,98490,98892,99294,
99696,100098,100500,100902,101304,101706,102108,102510
};

static int32_t fp_cos_table[TABLE_LENGTH] PROGMEM = {
65536,65535,65531,65525,65516,65505,65492,65476,
65457,65436,65413,65387,65359,65328,65294,65259,
65221,65180,65137,65091,65043,64993,64940,64885,
64827,64767,64704,64639,64572,64502,64429,64355,
64278,64198,64116,64031,63945,63855,63764,63670,
63573,63474,63373,63269,63163,63055,62944,62831,
62716,62598,62478,62355,62230,62103,61974,61842,
61707,61571,61432,61291,61147,61002,60853,60703,
60550,60395,60238,60079,59917,59753,59587,59418,
59248,59075,58900,58722,58543,58361,58177,57991,
57802,57612,57419,57224,57027,56828,56627,56423,
56218,56010,55800,55588,55374,55158,54940,54720,
54498,54274,54047,53819,53588,53356,53122,52885,
52647,52406,52164,51920,51673,51425,51175,50923,
50669,50413,50155,49895,49634,49370,49105,48838,
48569,48298,48026,47751,47475,47197,46917,46636,
46352,46067,45780,45492,45202,44910,44616,44321,
44024,43725,43425,43123,42820,42514,42208,41899,
41590,41278,40965,40650,40334,40017,39698,39377,
39055,38731,38406,38080,37752,37423,37092,36760,
36426,36092,35755,35418,35079,34739,34397,34054,
33710,33365,33018,32670,32321,31971,31619,31267,
30913,30558,30202,29844,29486,29126,28766,28404,
28041,27677,27312,26946,26579,26211,25842,25473,
25102,24730,24357,23983,23609,23233,22857,22480,
22102,21723,21343,20963,20582,20200,19817,19433,
19049,18664,18278,17892,17505,17117,16729,16340,
15950,15560,15169,14778,14386,13993,13600,13207,
12813,12418,12023,11628,11232,10836,10439,10042,
9645,9247,8849,8450,8052,7652,7253,6853,
6454,6053,5653,5252,4852,4451,4049,3648,
3247,2845,2443,2042,1640,1238,836,434
}; 

int32_t fp_tan(int32_t theta) { 
    return fp_div(fp_sin(theta), fp_cos(theta));
}

int32_t fp_sin(int32_t theta) { 
    return -fp_cos(theta + FP_PI_OVER_TWO);
}

//Quadratic interpolation.
int32_t fp_cos(int32_t theta) {
    uint8_t n;
    int8_t negative=0;
    int32_t x_n=0, x_np1=0, x_np2=0;
    int32_t y_n, y_np1, y_np2;
    int32_t dd_n, dd_np1, second_dd, result;
    
    //Move theta into [0, pi/2] w/ appropriate sign.
    theta = ABS(theta) % FP_TWO_PI;

    if(theta > FP_PI) 
        theta = FP_TWO_PI - theta;
    
    if(theta > FP_PI_OVER_TWO) {
        theta = FP_PI - theta;
        negative = 1;
    }

    //Find the nearest table values. FIXME
    n = theta / TABLE_STEP;
    while( n < TABLE_LENGTH - 1 && pgm_read_dword(&linspace[n])<theta){
        n++;
    }
    
    //theta is between x_{n-1} and x_{n}
    
    if(n == TABLE_LENGTH - 1) { 
        //Perform linear interpolation, since we're close to zero anyway.
        x_n = pgm_read_dword(&linspace[TABLE_LENGTH - 1]);
        y_n = pgm_read_dword(&fp_cos_table[TABLE_LENGTH - 1]);

        result = fp_mult(fp_div(FP_PI_OVER_TWO - x_n, 0 - y_n), theta - x_n) + y_n;
        return negative ? -result : result;
    }

    if(n == TABLE_LENGTH) { 
        
        return 0;
    }
    
    //Address the general case. Quadratic interpolation.
    //Load in the necessary values.
    x_n = pgm_read_dword(&linspace[n]);
    x_np1 = pgm_read_dword(&linspace[n+1]);
    x_np2  = pgm_read_dword(&linspace[n + 2]);
    
    y_n = pgm_read_dword(&fp_cos_table[n]);
    y_np1 = pgm_read_dword(&fp_cos_table[n + 1]);
    y_np2 = pgm_read_dword(&fp_cos_table[n + 2]);

    //Calculate first divided differences.
    dd_n = fp_div(y_np1 - y_n, x_np1 - x_n);
    dd_np1 = fp_div(y_np2 - y_np1, x_np2 - x_np1);

    //Calculate the second divided difference.
    second_dd = fp_div(dd_np1 - dd_n, x_np2 - x_n);
    
    result = fp_mult(fp_mult(second_dd, theta - x_n), theta - x_np1)  
            + fp_mult(dd_n, theta - x_n) + y_n;

    return negative ? -result : result;
}

//FIXME I didn't write these functions very carefully...
int32_t fp_mult(int32_t a, int32_t b) { 
    return (int32_t) (((int64_t)a) * ((int64_t)b)) >>  16;
}

int32_t fp_div(int32_t a, int32_t b) { 
    return (int32_t) ((int64_t)a << 16) / (int64_t)b;
}



