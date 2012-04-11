# -*- coding:utf-8 -*-
import serial
import time


serieCapt = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

id_hg = 1
id_hd = 2
id_bg = 0
id_bd = 3

"""
PROTOCOLE DE COMMUNICATION PC <-> AVR POUR LES AX12 
---------------------------------------------------

    ENVOI D'UN OCTET (8 bits)
        ex : 01101001
        
    PREMIER BIT : ASSERVISSEMENT EN ROTATION ?
         -> si 1er bit = 0 ALORS ASSERVISSEMENT EN ROTATION
                Puis :
                    2 bits suivants : codage de l'id de l'AX12
                    5 bits suivants : codage de l'angle
                    
                    EXEMPLE :
                            0 10 10110
                            |  |   |______________________  
                            |  |_________                |
                            |            |               |
                         rotation      id = 2       angle consigne
                         
        -> SINON : 
                2 bits suivants : codage de l'ordre à donner :
                    si 00 : changement de la vitesse des AX12 branchés
                            -> codage de la vitesse sur les bits suivants
                    si 01 : changement de l'id
                            -> codage du nouvel id sur les bits suivants.
                            
                    si 10 : changement du baud rate d'écoute des AX12 branchés
                            -> codage du nouveau baud rate :
                                    00000 : BR de 1.000.000
                                    00001 : BR de   200.000
                                    00010 : BR de   115.200
                                    00011 : BR de    57.600
                                    00100 : BR de     9.600
                                    
"""
# Conversion du chiffre décimal a en chaîne de caract. de 0 et de 1, de longueur nbBits
def bin(a, nbBits) :
    s = ''
    t = {'0' : '000', '1' : '001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110', '7':'111'}
    for c in oct(a)[1:] :
        s += t[c]
    l = len(s.lstrip('0'))
    result = '0'*(nbBits - l)
    return result+s.lstrip('0')

def changer_serie(numero) :
    serieCapt = serial.Serial('/dev/ttyUSB' + str(numero), 9600, timeout = 1)
    
def initialiserBras() :
    serieCapt.write(chr(int('00001111', 2)))
    serieCapt.write(chr(int('00101111', 2)))
    serieCapt.write(chr(int('01001111', 2)))
    serieCapt.write(chr(int('01101111', 2)))

def testerBras() :
    i=0
    for i in range(127) :
        serieCapt.write(chr(i))
        time.sleep(0.5)
    
def fermerBras():
    changer_angle(0)

def ouvrirBras() :
    changer_angle(160)
    
def changer_angle(angle, nom = "ALL") :
    # ANGLE COMPRIS ENTRE 0 ET 150
    if angle <= 125 and angle >= 0 :
        angle /= 180.
        angle *= 31
        angle = int(angle)
        
        if nom == "hg" or nom == "ALL" :
            serieCapt.write(chr(int('0' + bin(id_hg, 2) + bin(31 - angle, 5), 2)))
        if nom == "hd" or nom =="ALL":
            serieCapt.write(chr(int('0' + bin(id_hd, 2) + bin(angle, 5), 2)))
        if nom == "bd" or nom =="ALL":
            serieCapt.write(chr(int('0' + bin(id_bd, 2) + bin(31 - angle, 5), 2)))
        if nom == "bg" or nom =="ALL":
            serieCapt.write(chr(int('0' + bin(id_bg, 2) + bin(angle, 5), 2)))
    

# VITESSE DOIT ETRE COMPRIS ENTRE 0 et 500
def changer_vitesse(vitesse) :
    vitesse = vitesse/500.
    vitesse *= 31
    vitesse = int(vitesse)
    serieCapt.write(chr(int('1' + '00' + bin(vitesse, 5), 2)))
    
def test_vitesse() :
    for i in range(0,10) :
        changer_vitesse(i*50)
        time.sleep(1)
        if i%2 == 0 :
            ouvrirBras()
        else :
            fermerBras()
            
def changer_id(nouvel_id) :
    serieCapt.write(chr(int('1' + '01' + '000' + bin(nouvel_id, 2), 2)))

    
def BIG_TEST() :
    time.sleep(1)
    
    initialiserBras()
    time.sleep(1)
    changer_angle(160)
    time.sleep(1)
    changer_angle(0)
    time.sleep(1)
    changer_angle(45)
    time.sleep(1)
    changer_angle(120)
    time.sleep(1)
    changer_angle(45, "bg")
    time.sleep(0.3)
    changer_angle(45, "bd")
    time.sleep(0.3)
    changer_angle(45, "hg")
    changer_angle(45, "hd")
    time.sleep(0.3)
    changer_angle(100)
    time.sleep(0.2)
    changer_angle(120)
    time.sleep(0.3)
    changer_angle(140, "bg")
    changer_angle(140, "bd")

    changer_angle(160, "hg")
    changer_angle(160, "hd")
    time.sleep(0.5)
    changer_angle(45, "hd")
    changer_angle(45, "hg")
    changer_vitesse(100)
    changer_angle(20, "bd")
    changer_angle(20, "bg")
    changer_vitesse(500)
    time.sleep(0.5)
    changer_angle(160, "hg")
    changer_angle(160, "hd")
    time.sleep(0.5)
    changer_angle(45, "hd")
    changer_angle(45, "hg")
    time.sleep(0.5)
    changer_angle(160, "hg")
    changer_angle(160, "hd")
    time.sleep(0.5)
    changer_angle(45, "hd")
    changer_angle(45, "hg")
    time.sleep(0.5)
    changer_angle(160, "hg")
    changer_angle(160, "hd")
    time.sleep(0.5)
    changer_angle(45, "hd")
    changer_angle(45, "hg")
    time.sleep(0.5)
    changer_angle(160, "hg")
    changer_angle(160, "hd")
    time.sleep(0.5)
    changer_angle(45, "hd")
    changer_angle(45, "hg")
    time.sleep(0.5)
    
    changer_angle(40, "bg")
    changer_angle(40, "hg")
    changer_angle(160, "hd")
    changer_angle(160, "bd")
    time.sleep(0.5)
    changer_vitesse(150)
    changer_angle(40, "bd")
    changer_angle(40, "hd")
    changer_angle(160, "hg")
    changer_angle(160, "bg")
    time.sleep(1.5)
    changer_vitesse(500)
    changer_angle(40, "bg")
    changer_angle(40, "hg")
    changer_angle(160, "hd")
    changer_angle(160, "bd")
    time.sleep(0.5)
    changer_vitesse(150)
    changer_angle(40, "bd")
    changer_angle(40, "hd")
    changer_angle(160, "hg")
    changer_angle(160, "bg")
    time.sleep(1.5)
    changer_vitesse(400)
    changer_angle(40, "bg")
    changer_angle(160, "bd")
    time.sleep(1)
    changer_angle(160, "hd")
    changer_angle(40, "hg")
    changer_angle(160, "bg")
    changer_angle(40, "bd")
    time.sleep(0.7)
    changer_angle(90)
    time.sleep(1)
    changer_vitesse(500)
    
    changer_angle(80, "bg")
    changer_angle(80, "bd")
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    time.sleep(0.5)
    changer_angle(70, "hg")
    changer_angle(70, "hd")
    changer_angle(110, "bg")
    changer_angle(110, "bd")
    time.sleep(0.5)
    changer_angle(60, "bg")
    changer_angle(60, "bd")
    changer_angle(120, "hg")
    changer_angle(120, "hd")
    time.sleep(1)
    changer_angle(70, "hg")
    changer_angle(70, "hd")
    changer_angle(110, "bg")
    changer_angle(110, "bd")
    time.sleep(0.5)
    changer_angle(80, "bg")
    changer_angle(80, "bd")
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    time.sleep(0.5)
    changer_angle(90)
    time.sleep(1)
    
    #####################################
    
    changer_angle(80, "hg")
    time.sleep(0.3)
    changer_angle(100, "hg")
    time.sleep(0.3)
    changer_angle(80, "hg")
    time.sleep(0.3)
    changer_angle(100, "hg")
    time.sleep(0.3)
    
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    time.sleep(0.3)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    time.sleep(0.3)
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    time.sleep(0.3)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    time.sleep(0.3)
    
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    time.sleep(0.3)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    time.sleep(0.3)
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    time.sleep(0.3)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    time.sleep(0.3)
    
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    changer_angle(80, "bg")
    time.sleep(0.3)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    changer_angle(100, "bg")
    time.sleep(0.3)
    
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    changer_angle(80, "bg")
    time.sleep(0.15)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    changer_angle(100, "bg")
    time.sleep(0.15)
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    changer_angle(80, "bg")
    time.sleep(0.15)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    changer_angle(100, "bg")
    time.sleep(0.15)
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    changer_angle(80, "bg")
    time.sleep(0.15)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    changer_angle(100, "bg")
    time.sleep(0.15)
    changer_angle(80, "hg")
    changer_angle(80, "hd")
    changer_angle(80, "bd")
    changer_angle(80, "bg")
    time.sleep(0.15)
    changer_angle(100, "hg")
    changer_angle(100, "hd")
    changer_angle(100, "bd")
    changer_angle(100, "bg")
    time.sleep(0.15)
    
    changer_angle(160)
    
    