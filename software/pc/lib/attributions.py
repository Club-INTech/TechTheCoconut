# -*- coding: utf-8 -*-

import os
import serial
import log
log = log.Log(__name__)

def attribuer():
    #on retourne une liste des chemins trouvés
    chemins = ["","","","","",""]
    
    #liste des périphériques recherchés
    peripheriques = [[0,"asservissement",9600],[3,"capteurs_actionneurs",9600],[2,"balise",9600]]#[1,"capteurs",57600],[4,"actionneurs",9600]]
    
    
    #listage des périphériques trouvés
    sources = os.popen('ls -1 /dev/ttyUSB* 2> /dev/null').readlines()
    sources.extend(os.popen('ls -1 /dev/ttyACM* 2> /dev/null').readlines())
    for k in range(len(sources)):
        sources[k] = sources[k].replace("\n","")
    
    for periph in peripheriques:
        for source in sources:
            serieCapt = serial.Serial(source, periph[2], timeout=0.3)
            #clean serie
            serieCapt.write("\n\r")
            serieCapt.write("?\r")
            serieCapt.readline()
            serieCapt.write("?\r")
            serieCapt.readline()
            
            serieCapt.write("?\r")
            rep = str(serieCapt.readline())
            if rep.replace("\n","").replace("\r","").replace("\0","") == str(periph[0]):
                print periph[1]+"\tOK sur " + source
                chemins[int(periph[0])] = source
                sources.remove(source)
                break
    log.logger.info(str(chemins))
    return chemins