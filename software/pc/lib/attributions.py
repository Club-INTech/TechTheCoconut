# -*- coding: utf-8 -*-

import serial
import log
log = log.Log(__name__)

def attribuer():
    peripheriques = [[0,"asservissement",9600],[1,"capteurs",57600],[2,"balise",9600],[4,"actionneurs",9600]]
    chemins = ["","","","","",""]

    for periph in peripheriques:
        i=0
        instancie = False
        while i<10 and not instancie :
            try :
                serieCapt = serial.Serial("/dev/ttyUSB"+str(i), periph[2], timeout=0.3)
                serieCapt.write("\n\r")
                #print "/dev/ttyUSB"+str(i)+" est occupé, ping..."
                sent=False
                serieCapt.write("?\r")
                rep = str(serieCapt.readline())
                if rep.replace("\n","").replace("\r","").replace("\0","") == str(periph[0]):
                    print periph[1]+"\tOK sur ttyUSB" + str(i)
                    chemins[int(periph[0])] = "/dev/ttyUSB" + str(i)
                    instancie = True
                    sent=True
                if sent:
                    break
                else:
                    i+=1
            except :
                i+=1
    log.logger.warn(str(chemins))
    return chemins