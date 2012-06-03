#ifndef DEF_AX12_HPP
#define DEF_AX12_HPP

// Librairie INTech
#include <libintech/serial/serial_0.hpp>

// Librairie Standard
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

// Librairie INTech.
#include <libintech/serial/serial_1.hpp>


#define AX_BROADCAST            0xFE



/** EEPROM AREA **/
#define AX_MODEL_NUMBER_L           0
#define AX_MODEL_NUMBER_H           1
#define AX_VERSION                  2
#define AX_ID                       3
#define AX_BAUD_RATE                4
#define AX_RETURN_DELAY_TIME        5
#define AX_CW_ANGLE_LIMIT_L         6
#define AX_CW_ANGLE_LIMIT_H         7
#define AX_CCW_ANGLE_LIMIT_L        8
#define AX_CCW_ANGLE_LIMIT_H        9
#define AX_SYSTEM_DATA2             10
#define AX_LIMIT_TEMPERATURE        11
#define AX_DOWN_LIMIT_VOLTAGE       12
#define AX_UP_LIMIT_VOLTAGE         13
#define AX_MAX_TORQUE_L             14
#define AX_MAX_TORQUE_H             15
#define AX_RETURN_LEVEL             16
#define AX_ALARM_LED                17
#define AX_ALARM_SHUTDOWN           18
#define AX_OPERATING_MODE           19
#define AX_DOWN_CALIBRATION_L       20
#define AX_DOWN_CALIBRATION_H       21
#define AX_UP_CALIBRATION_L         22
#define AX_UP_CALIBRATION_H         23

/** RAM AREA **/
#define AX_TORQUE_ENABLE            24
#define AX_LED                      25
#define AX_CW_COMPLIANCE_MARGIN     26
#define AX_CCW_COMPLIANCE_MARGIN    27
#define AX_CW_COMPLIANCE_SLOPE      28
#define AX_CCW_COMPLIANCE_SLOPE     29
#define AX_GOAL_POSITION_L          30
#define AX_GOAL_POSITION_H          31
#define AX_GOAL_SPEED_L             32
#define AX_GOAL_SPEED_H             33
#define AX_TORQUE_LIMIT_L           34
#define AX_TORQUE_LIMIT_H           35
#define AX_PRESENT_POSITION_L       36
#define AX_PRESENT_POSITION_H       37
#define AX_PRESENT_SPEED_L          38
#define AX_PRESENT_SPEED_H          39
#define AX_PRESENT_LOAD_L           40
#define AX_PRESENT_LOAD_H           41
#define AX_PRESENT_VOLTAGE          42
#define AX_PRESENT_TEMPERATURE      43
#define AX_REGISTERED_INSTRUCTION   44
#define AX_PAUSE_TIME               45
#define AX_MOVING                   46
#define AX_LOCK                     47
#define AX_PUNCH_L                  48
#define AX_PUNCH_H                  49

/** Instruction Set **/
#define AX_PING                     1
#define AX_READ_DATA                2
#define AX_WRITE_DATA               3
#define AX_REG_WRITE                4
#define AX_ACTION                   5
#define AX_RESET                    6
#define AX_SYNC_WRITE               131



    template< class Serial, uint32_t baud_rate >
class AX12
{
private :
    
    // Méthode pour envoyer un packet lisible par l'AX12
    void sendPacket (uint8_t id, uint8_t datalength, uint8_t instruction, uint8_t *data)
    {
        uint8_t checksum = 0;
        Serial::send_char(0xFF);
        Serial::send_char(0xFF);
        
        Serial::send_char(id);
        Serial::send_char(datalength + 2);
        Serial::send_char(instruction);
        
        checksum += id + datalength + 2 + instruction;

        uint8_t f;
        for (f=0; f<datalength; f++) {
        checksum += data[f];
        Serial::send_char(data[f]);
        }
        Serial::send_char(~checksum);
    }
    
public :
    /// Initialisation
    void init(uint16_t AX_angle_CW, uint16_t AX_angle_CCW, uint16_t AX_speed)
    {
        // Initialisation de la série
        Serial::init();
        Serial::change_baudrate(baud_rate);
        
        // Active l'asservissement du servo
        writeData (AX_BROADCAST, AX_TORQUE_ENABLE, 1, 1);
        // Définit les angles mini et maxi
        writeData (AX_BROADCAST, AX_CW_ANGLE_LIMIT_L, 2, AX_angle_CW);
        writeData (AX_BROADCAST, AX_CCW_ANGLE_LIMIT_L, 2, AX_angle_CCW);
        // Définit la vitesse de rotation
        writeData (AX_BROADCAST, AX_GOAL_SPEED_L, 2, AX_speed);
    }
    
    /// Reset de l'AX12
    void reset (uint8_t id) {
        uint8_t *data = 0;
        sendPacket (id, 0, AX_RESET, data);  
    }


    /// Ecriture d'une séquence de bits 
    void writeData (uint8_t id, uint8_t regstart, uint8_t reglength, uint16_t value) {
        uint8_t data [reglength+1];
        data [0] = regstart; data [1] = value&0xFF;
        if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
        sendPacket (id, reglength+1, AX_WRITE_DATA, data);
    }
    
    /// Tente de réanimer un AX12 mort.
    void reanimationMode(uint8_t id = 0xFE)
    {
        uint8_t debug_baudrate = 0;
        // On brute-force le baud rate des AX12, et on leur envoie pour chaque baud rate
        // d'écoute un signal de reset.
        while (debug_baudrate < 0xFF)
        {
            Serial::change_baudrate(2000000/(debug_baudrate + 1));
            reset(id);
            debug_baudrate++;
        }
        
        // Une fois que le signal de reset a été reçu, l'AX12 écoute à 1.000.000 bps.
        // Donc à ce baud rate, on reflash le baud rate d'écoute de l'AX12.
        Serial::change_baudrate(1000000);
        writeData(0xFE, AX_BAUD_RATE, 1, uint8_t(2000000/baud_rate - 1));
        
        Serial::change_baudrate(baud_rate);
        // Si l'id est différente du broadcast, alors on la reflash.
        if (id != 0xFE)
            initID(0x01, id);
    }
    
    /// Réinitialisation de l'ID de l'AX12
    void initID(uint8_t ancien_id, uint8_t nouvel_id)
    {
        writeData (ancien_id, AX_ID, 1, nouvel_id);
    }

    /// Goto
    void GoTo (uint8_t ID, uint16_t angle)
    {
        writeData (ID, AX_GOAL_POSITION_L, 2, angle);
    }

    /// Changement de l'angle min
    void changeAngleMIN(uint8_t ID, uint16_t angleCW)
    {
        writeData (ID, AX_CW_ANGLE_LIMIT_L, 2, angleCW);
    }

    /// Changement de l'angle max
    void changeAngleMAX(uint8_t ID, uint16_t angleCCW)
    {
        writeData (ID, AX_CCW_ANGLE_LIMIT_L, 2, angleCCW);
    }
    
    /// Changement de la vitesse de rotation
    void changeSpeed(uint8_t ID, uint16_t vitesse)
    {
        writeData (ID, AX_GOAL_SPEED_L, 2, vitesse);
    }

    /// Désasservissement d'un AX12 branché.
    void unasserv(uint8_t ID)
    {
        writeData (ID, AX_TORQUE_ENABLE, 1, 0);
    }

    
        
        

    
    
    
    
};
    


#endif