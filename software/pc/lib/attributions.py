# -*- coding: utf-8 -*-

import serial

def attribuer():
    peripheriques = [[0,"asservissement",9600,"serieCapt"],[1,"capteurs",57600],[2,"balise",9600],[4,"actionneurs",9600]]
    chemins = ["","","","","",""]

    for periph in peripheriques:
        i=0
        instancie = False
        while i<20 and not instancie :
            try :
                serieCapt = serial.Serial("/dev/ttyUSB"+str(i), periph[2], timeout=0.1)
                serieCapt.write("\n\r")
                #print "/dev/ttyUSB"+str(i)+" est occupé, ping..."
                sent=False
                for pat in ["\n\r","\r\n","\n","\r"]:
                    serieCapt.write("?"+pat)
                    rep = str(serieCapt.readline())
                    if rep.replace("\n","").replace("\r","").replace("\0","") == str(periph[0]):
                        print periph[1]+" OK sur ttyUSB" + str(i)
                        print periph[0]
                        chemins[int(periph[0])] = "/dev/ttyUSB" + str(i)
                        instancie = True
                        sent=True
                        break
                if sent:
                    break
                else:
                    i+=1
            except :
                i+=1
    print chemins
    return chemins