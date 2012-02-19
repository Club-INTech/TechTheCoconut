# -*- coding: utf-8 -*-

# screen /dev/ttyUSB0 57600

import marshal
import time
from serie_simple import *

#BAUDRATE : 9600, 57600

serie1=SerieSimple("/dev/ttyUSB1",9600,5)
serie0=SerieSimple("/dev/ttyUSB0",9600,5)

#ctes=["0.0","0.0","0.0","0.0","0.0","0.0"]
#marshal.dump(ctes, open("constantes_asserv", 'wb'))


global dest
dest = "rien"

def envoyer(arg):
    global dest
    try:
            serie0.ecrire(arg)
    except:
        pass
    try:
            serie1.ecrire(arg)
    except:
        pass
    
    #enregistrement des constantes étalonnées
    
    ctes=marshal.load(open("constantes_asserv","rb"))
    
    if dest == "ctp":
        ctes[0]=arg
    elif dest == "ctd":
        ctes[1]=arg
    elif dest == "cti":
        ctes[2]=arg
    elif dest == "crp":
        ctes[3]=arg
    elif dest == "crd":
        ctes[4]=arg
    elif dest == "cri":
        ctes[5]=arg
        
    dest = arg    
    marshal.dump(ctes, open("constantes_asserv", 'wb'))

def initialise():
    ctes=marshal.load(open("constantes_asserv","rb"))
    envoyer("ctp")
    envoyer(ctes[0])
    envoyer("ctd")
    envoyer(ctes[1])
    envoyer("cti")
    envoyer(ctes[2])
    envoyer("crp")
    envoyer(ctes[3])
    envoyer("crd")
    envoyer(ctes[4])
    envoyer("cri")
    envoyer(ctes[5])
    
initialise()
while True :
    print "modifier ?"
    print "constantes de rotation.............r"
    print "constantes de translation..........t"
    print "une seule constante................c"
    print "entrer constantes indépendemment...i"
    print "afficher les constantes actuelles..a"
    print "sortez moi d'ici !.................q"
    choix = raw_input()
    if choix == "q":
        try:
            serie0.stop()
        except:
            pass
        try:
                serie1.stop()
        except:
            pass
        break
    elif choix == "r":
        print "constantes de rotation :"
        
        print "kp ?"
        buff=raw_input()
        envoyer("crp")
        envoyer(str(float(buff)))
        print "kd ?"
        buff=raw_input()
        envoyer("crd")
        envoyer(str(float(buff)))
        print "ki ?"
        buff=raw_input()
        envoyer("cri")
        envoyer(str(float(buff)))
        
    elif choix == "t":
        print "constantes de translation :"
        
        print "kp ?"
        buff=raw_input()
        envoyer("ctp")
        envoyer(str(float(buff)))
        print "kd ?"
        buff=raw_input()
        envoyer("ctd")
        envoyer(str(float(buff)))
        print "ki ?"
        buff=raw_input()
        envoyer("cti")
        envoyer(str(float(buff)))
        
    elif choix == "c":
        print "quelle constante modifier ?"
        print "de rotation.....r"
        print "de translation..t"
        choixC = raw_input()
        print "i ? p ? d ?"
        const = raw_input()
        print "entrez q pour quitter"
        while True :
            buf = raw_input()
            if buf =="q":
                break
            envoyer("c"+choixC+const)
            envoyer(str(float(buf)))
    elif choix == "i":
        print "quelle constante modifier ?"
        print "de rotation.....r"
        print "de translation..t"
        choixC = raw_input()
        print "entrez q pour quitter"
        print "exemple : p 0.0"
        print "exemple : i 3"
        while True :
            buf = raw_input()
            if buf =="q":
                break
            envoyer("c"+choixC+buf[0])
            envoyer(str(float(buf[2:])))
    
    elif choix == "a":
        ctes=marshal.load(open("constantes_asserv","rb"))
        print "translation : kp="+ctes[0]+" kd="+ctes[1]+" ki="+ctes[2]
        print "rotation    : kp="+ctes[3]+" kd="+ctes[4]+" ki="+ctes[5]
        