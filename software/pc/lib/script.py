# -*- coding: utf-8 -*-

import log
import sys
import __builtin__
import time
import outils_math.point
import lib.log

#log =lib.log.Log(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

class Script:
    
    def __init__(self):
        if hasattr(__builtin__.instance, 'asserInstance'):
            self.asserInstance = __builtin__.instance.asserInstance
        else:
            log.logger.error("l'instance de instance.asserInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'capteurInstance'):
            self.capteurInstance = __builtin__.instance.capteurInstance
        else:
            log.logger.error("l'instance de instance.capteurInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("l'instance de instance.robotInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'serieAsserInstance'):
            self.serialInstance = __builtin__.instance.serieAsserInstance
        else:
            log.logger.error("l'instance de instance.serieAsserInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'serieCaptInstance'):
            self.CaptSerialInstance = __builtin__.instance.serieCaptInstance
        else:
            log.logger.error("l'instance de instance.serieCaptInstance n'est pas chargée")
    
    def recalage(self):
        """
        Fonction permettant de recaller le robot dans un coin de la table
        """
        
        self.asserInstance.recalage()
        
        
        """
        couleur = profils.develop.constantes.constantes["couleur"]
        self.asser.avancer(-100.0)
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.avancer(-100.0)
        if couleur == 'R':
            self.asser.robotInstance.position.x = 1460
            self.asser.serieInstance.ecrire("c\nx\n" + str(float(1460)))
        else:
            self.asser.robotInstance.position.x = -1460
            self.asser.serieInstance.ecrire("c\nx\n" + str(float(-1460)))
        self.asser.setUnsetAsser('rotation', 1)
        self.asser.avancer(200.0)
        self.asser.tourner(3*math.pi/2)
        self.asser.avancer(-150.0)
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.avancer(-150)
        self.asser.robotInstance.position.y = 60
        self.asser.serieInstance.ecrire("c\ny\n" + str(float(60)))
        self.asser.setUnsetAsser('rotation', 1)
        self.asser.avancer(200.0)
        if couleur == 'R':
            self.asser.tourner(3*math.pi/2)
        else:
            self.asser.tourner(0)
        self.asser.avancer(-300.0)
        """
        
    def testPosition(self):
        self.recalage()
        raw_input()
        self.asserInstance.avancer(600)
        raw_input()
        self.asserInstance.tourner(1.57)
        raw_input()
        self.asserInstance.goTo(outils_math.point.Point(100, 1500))
        raw_input()
        self.asserInstance.goTo(outils_math.point.Point(800, 250))
        raw_input()
        self.asserInstance.tourner(3.1415)
        raw_input()
        self.asserInstance.avancer(-400)
        
    def etalonnageAsserv(self):
        
        while True :
            print "modifier ?"
            print "constantes de rotation.............r"
            print "constantes de translation..........t"
            print "sortez moi d'ici !.................q"
            choix = raw_input()
            if choix == "q":
                break
            elif choix == "r":
                while True :
                    print "constantes rotation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    else:
                        val = str(float(raw_input()))
                        self.serialInstance.write("cr"+cte.replace("\r","").replace("\n","")+"\n"+val+"\n")
                
            elif choix == "t":
                while True :
                    print "constantes translation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    else:
                        val = str(float(raw_input()))
                        self.serialInstance.write("ct"+cte.replace("\r","").replace("\n","")+"\n"+val+"\n")
        
        
    def lire(self):
        """
        Permet de lire un message de ltestPosition'asservissement autre que celui lu par le thread d'acquisition.
        """
        while not self.robotInstance.new_message:
            time.sleep(0.01)
        self.robotInstance.new_message = False
        return self.robotInstance.message