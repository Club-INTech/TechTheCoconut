# -*- coding: utf-8 -*-

import asservissement
import outils_math
import robot
from outils_math.point import Point
import script
import time
import serial
import instance
import __builtin__
import math
import threading
from threading import Lock
"""
x = raw_input("Donner les coordonnées en x puis y du point de départ\n")
y = raw_input()
depart = outils_math.point.Point(x,y)

x = raw_input("Donner les coordonnées en x puis y du point de arrivee\n")
y = raw_input()
arrivee = outils_math.point.Point(x,y)
"""
"""
capteurInstance = __builtin__.instance.capteurInstance
while 42:
    print capteurInstance.mesurer()
    time.sleep(0.1)
"""
import __builtin__
import instance

asser = __builtin__.instance.asserInstanceDuree
sc = __builtin__.instance.scriptInstance
#sc.gestionScripts(sc.recalage)
#sc.gestionScripts(sc.secour)


#depart = outils_math.point.Point(0.0,400)
##############################UTILISATION DE LA STRATEGIE####################################
#import strategie
#strategie = strategie.Strategie()
#strategie.lancer()
#############################################################################################


##############################UTILISATION D'UN SCRIPT########################################
#while True:
    #sc.gestionScripts(sc.test4,True)
    
##############################UTILISATION D'UN SCRIPT######################################## 


def console():
    asser.setOrientation(0)
    asser.setPosition(Point(float(0),float(400)))
    print ("tests de points inaccessibles....a")
    print ("tests de goto....................g")
    com = raw_input("?")
    if com == "g":
        while True:
            print "recherche de chemin"
            print "quitter............q"
            print "point de départ....d"
            print "point d'arrivée....a"
            print "placer adverse.....p"
            com = raw_input("?")
            if com == "q":
                break
            elif com == "d":
                xd = raw_input("x départ? ")
                yd = raw_input("y départ? ")
                asser.setPosition(Point(float(xd),float(yd)))
            elif com == "a":
                xa = raw_input("x arrivée? ")
                ya = raw_input("y arrivée? ")
                asser.goTo(Point(float(xa),float(ya)))
            elif com == "p":
                xp = raw_input("x robot adverse? ")
                yp = raw_input("y robot adverse? ")
                __builtin__.instance.ajouterRobotAdverse(Point(float(xp),float(yp)))
            print ""
    elif com == "a":
        while True:
            x = raw_input("x ? ")
            y = raw_input("y ? ")
            if( asser.estInaccessible(Point(float(x),float(y)))):
                print "inaccessible"
            else:
                print "accessible"
console()


#############################################################################################

#def test():
    #while 42 :
        #print "getPosition.........p"
        #print "getOrientation......o"
        #print "sortir..............q"
        #ordre = raw_input()
        #if ordre == "q":
            #break
        #elif ordre == "p":
            #while 69:
                #print "pos ?\n"
                #attend = raw_input()
                #if attend == "q":
                    #break
                #else:
                    #pos = asser.getPosition()
                    #print "("+str(int(pos.x))+", "+str(int(pos.y))+")\n"
        #elif ordre == "o":
            #while 1337:
                #print "orient ?\n"
                #attend = raw_input()
                #if attend == "q":
                    #break
                #else:
                    #print str(asser.getOrientation())+"\n"


#import robot
#import asservissement
#robotInstance=robot.Robot()
#asser = asservissement.Asservissement(robotInstance)

#scriptInstance = __builtin__.instance.scriptInstance


#arrivee = outils_math.point.Point(100,1500)
#print asser.dureeGoTo(depart, arrivee, 2)
#depart = outils_math.point.Point(0.0,841)
#arrivee = outils_math.point.Point(0,800)
#print asser.dureeGoTo(depart, arrivee, 1)
#depart = arrivee
#arrivee = outils_math.point.Point(0,100)
#print asser.dureeGoTo(depart, arrivee, 1)
#depart = arrivee
#arrivee = outils_math.point.Point(0,1000)
#print asser.dureeGoTo(depart, arrivee, 1)

######################################################################
#Test de mutex
#class Test:
    #def __init__(self):
        #self.huk = 0
        #mutex = __builtin__.instance.mutex

        #thread = threading.Thread(target = self.ecoute_thread)
        #thread.start()
        #threadd = threading.Thread(target = self.ecriture_thread)
        #threadd.start()
    
    #def ecoute_thread(self):
        #while 42:
            #print self.huk

    #def ecriture_thread(self):
        #while 42:
            #self.huk += 1
#######################################################################



#écriture du point de départ initial

#asser.serialInstance.write("\n")

#asser.serialInstance.write("cx\n" + str(float(depart.x)) + "\ncy\n"+str(float(depart.y)))
#robotInstance.setPosition
#scriptInstance.homologation()
#asser.avancer(500)
#asser.avancer(-500)


#while 42:
    #asser.avancer(200)
    #asser.avancer(-200)
    
#asser.avancer(500)
#asser.avancer(-500)
#asser.avancer(500)
#asser.avancer(-500)

#while 42:
    #asser.avancer(400)
    #asser.tourner(0)
    #asser.avancer(400)
    #asser.tourner(math.pi)
    #asser.avancer(400)
    #asser.tourner(0)
    #asser.avancer(400)
    #asser.tourner(math.pi)
    #asser.avancer(400)
    #asser.tourner(0)
    #asser.avancer(400)
    #asser.tourner(math.pi)
    #asser.avancer(400)
    #asser.tourner(0)
    #asser.avancer(400)
    #asser.tourner(math.pi)
    
"""
asser.avancer(300)
#time.sleep(0.5)
asser.tourner(1.5)
#time.sleep(0.5)
asser.avancer(500)
#time.sleep(0.5)
asser.tourner(0)
#time.sleep(0.5)
asser.avancer(300)
#time.sleep(0.5)
asser.avancer(-300)
#time.sleep(0.5)
asser.tourner(1.5)
#time.sleep(0.5)
asser.avancer(600)
#time.sleep(0.5)
asser.tourner(-1.5)
#time.sleep(0.5)
asser.avancer(-480)
#time.sleep(0.5)
asser.avancer(1500)
asser.tourner(math.pi)
asser.avancer(-300)
"""
"""
asser.serialInstance.write('\n')
asser.serialInstance.write('d\n' + str(float(-200))+'\n')
acquitement = False
while not acquitement:
    asser.serialInstance.write('acq\n')
    reponse = str(asser.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
    print 'reponse :'
    print reponse
    if reponse == "FIN_MVT":
        acquitement = True
print 'FINI'
"""
#angle = 0.0
#angle = (float(angle)*3.14)/180
#asser.calculRayon(angle)
    
#scriptInstance = script.Script(asser)
#scriptInstance.huit()
#while(True):
    #x, y = '', ''
    #while x=='':
        #x = raw_input("x arrivé ?")
    #while y=='':
        #y = raw_input("y arrivé ?")
    #arrivee = outils_math.point.Point(int(x),int(y))
    #asser.goTo(depart, arrivee)
    #asser.serialInstance.write("pos\n")
    #depart = (asser.serialInstance.readline()).replace("\n","").replace("\r","").replace("\0", "")
    #if depart[4]== "+":
        #depart = depart.split("+")
    #else:
        #depart = depart.split("-")
    #depart = outils_math.point.Point(depart[0],depart[1])
    