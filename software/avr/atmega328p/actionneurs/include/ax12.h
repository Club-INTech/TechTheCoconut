// /*
//   ax12.h - arbotiX Library for AX-12 Servos
//   Copyright (c) 2008,2009 Michael E. Ferguson.  All right reserved.
//   Modificada el 15/11/09 por Pablo Gindel.
// */
// 
// #ifndef ax12_h
// #define ax12_h
// 
// #include <stdint.h>
// 
// #define AX12_MAX_SERVOS             18
// #define AX12_BUFFER_SIZE            32
// 
// /** EEPROM AREA **/
// #define AX_MODEL_NUMBER_L           0
// #define AX_MODEL_NUMBER_H           1
// #define AX_VERSION                  2
// #define AX_ID                       3
// #define AX_BAUD_RATE                4
// #define AX_RETURN_DELAY_TIME        5
// #define AX_CW_ANGLE_LIMIT_L         6
// #define AX_CW_ANGLE_LIMIT_H         7
// #define AX_CCW_ANGLE_LIMIT_L        8
// #define AX_CCW_ANGLE_LIMIT_H        9
// #define AX_SYSTEM_DATA2             10
// #define AX_LIMIT_TEMPERATURE        11
// #define AX_DOWN_LIMIT_VOLTAGE       12
// #define AX_UP_LIMIT_VOLTAGE         13
// #define AX_MAX_TORQUE_L             14
// #define AX_MAX_TORQUE_H             15
// #define AX_RETURN_LEVEL             16
// #define AX_ALARM_LED                17
// #define AX_ALARM_SHUTDOWN           18
// #define AX_OPERATING_MODE           19
// #define AX_DOWN_CALIBRATION_L       20
// #define AX_DOWN_CALIBRATION_H       21
// #define AX_UP_CALIBRATION_L         22
// #define AX_UP_CALIBRATION_H         23
// 
// /** RAM AREA **/
// #define AX_TORQUE_ENABLE            24
// #define AX_LED                      25
// #define AX_CW_COMPLIANCE_MARGIN     26
// #define AX_CCW_COMPLIANCE_MARGIN    27
// #define AX_CW_COMPLIANCE_SLOPE      28
// #define AX_CCW_COMPLIANCE_SLOPE     29
// #define AX_GOAL_POSITION_L          30
// #define AX_GOAL_POSITION_H          31
// #define AX_GOAL_SPEED_L             32
// #define AX_GOAL_SPEED_H             33
// #define AX_TORQUE_LIMIT_L           34
// #define AX_TORQUE_LIMIT_H           35
// #define AX_PRESENT_POSITION_L       36
// #define AX_PRESENT_POSITION_H       37
// #define AX_PRESENT_SPEED_L          38
// #define AX_PRESENT_SPEED_H          39
// #define AX_PRESENT_LOAD_L           40
// #define AX_PRESENT_LOAD_H           41
// #define AX_PRESENT_VOLTAGE          42
// #define AX_PRESENT_TEMPERATURE      43
// #define AX_REGISTERED_INSTRUCTION   44
// #define AX_PAUSE_TIME               45
// #define AX_MOVING                   46
// #define AX_LOCK                     47
// #define AX_PUNCH_L                  48
// #define AX_PUNCH_H                  49
// 
// /** Status Return Levels **/
// #define AX_RETURN_NONE              0
// #define AX_RETURN_READ              1
// #define AX_RETURN_ALL               2
// 
// /** Instruction Set **/
// #define AX_PING                     1
// #define AX_READ_DATA                2
// #define AX_WRITE_DATA               3
// #define AX_REG_WRITE                4
// #define AX_ACTION                   5
// #define AX_RESET                    6
// #define AX_SYNC_WRITE               131
// 
// typedef unsigned char byte;
// 
// void ax12Init(long baud);
// 
// byte ping (byte id);
// byte reset (byte id);
// byte readData (byte id, byte regstart, byte reglength);
// byte writeData (byte id, byte regstart, byte reglength, int value);
// 
// extern int status_id;
// extern int status_error;
// extern int status_data;
// 
// 
// // extern volatile uint16_t ax_cons1;
// // extern volatile uint16_t ax_cons2;
// 
// /*
//  *  Fonctions pour les AX12
//  *    ID : ID du servo
//  *    angleCW : angle max antitrigo
//  *    angleCCW : angle max trigo
//  *    angle : consigne en angle
//  *    vitesse : vitesse de rotation
//  */
// void AX12Init (uint8_t ID, uint16_t angleCW, uint16_t angleCCW, uint16_t vitesse);
// void AX12GoTo (uint8_t ID, uint16_t angle);
// 
// 
// #endif
