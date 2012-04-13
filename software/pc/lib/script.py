# -*- coding: utf-8 -*-

import log
import sys
import __builtin__
import time
import outils_math.point
import lib.log
import os
import math
import actionneur

log = lib.log.Log(__name__)

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
        largeur_robot = 200
        largeur_table = 3000
        
        self.asser.serieInstance.ecrire("ctm\n50.0\n")
        self.asser.serieInstance.ecrire("crm\n100.0\n")
        
        self.asser.avancer(-300.0)
        #self.asser.serieInstance.ecrire("cr0\n")
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.avancer(-200.0)
        if couleur == 'R':
            self.asser.robotInstance.position.x = -largeur_table/2+largeur_robot/2
            self.asser.serieInstance.ecrire("cx\n" + str(float(-largeur_table/2+largeur_robot/2)) + "\n")
            self.asser.robotInstance.orientation = 0.0
            self.asser.serieInstance.ecrire("co\n" + str(float(0.0)) + "\n")
        else:
            self.asser.robotInstance.position.x = largeur_table/2-largeur_robot/2
            self.asser.serieInstance.ecrire("cx\n" + str(float(largeur_table/2-largeur_robot/2)) + "\n")
            self.asser.robotInstance.orientation = math.pi
            self.asser.serieInstance.ecrire("co\n" + str(float(math.pi)) + "\n")
        self.asser.setUnsetAsser('rotation', 1)
        self.asser.avancer(300.0)
        self.asser.tourner(math.pi/2)
        self.asser.avancer(-300.0)
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.avancer(-300)
        self.asser.robotInstance.position.y = largeur_robot/2
        self.asser.serieInstance.ecrire("cy\n" + str(float(largeur_robot/2)) + "\n")
        self.asser.robotInstance.orientation = math.pi/2
        self.asser.serieInstance.ecrire("co\n" + str(float(math.pi/2)) + "\n")
        self.asser.setUnsetAsser('rotation', 1)
        self.asser.avancer(150.0)
        self.asser.serieInstance.ecrire("crm\n120.0\n")
        if couleur == 'R':
            self.asser.tourner(0.0)
        else:
            self.asser.tourner(math.pi)
        self.asser.serieInstance.ecrire("ctm\n120.0\n")
        self.asser.setUnsetAsser('rotation', 0)
        self.asser.setUnsetAsser('translation', 0)
        """
        
    def homologation(self):
        
        couleur = 'V'
        
        self.asserInstance.avancer(300)
        self.asserInstance.tourner(1.5)
        self.asserInstance.avancer(500)
        self.asserInstance.tourner(0)
        self.asserInstance.avancer(300)
        self.asserInstance.avancer(-300)
        self.asserInstance.tourner(1.5)
        self.asserInstance.avancer(650)
        self.asserInstance.tourner(-1.5)
        self.asserInstance.avancer(-480)
        self.serialInstance.write("ctm\n120.0\n")
        self.asserInstance.avancer(-500.0)
        self.serialInstance.write("ctm\n250.0\n")
        
        self.asserInstance.avancer(1500)
        if couleur == 'R':
            self.asserInstance.tourner(0.0)
        else :
            self.asserInstance.tourner(math.pi)
        self.asserInstance.avancer(-500.0)
        
        """
        #stocke le lingot et enfonce un poussoir
        self.asserInstance.avancer(600.0)
        self.asserInstance.tourner(math.pi/2)
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
        pas = 0
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
                    if (pas > 4):
                        pas = 0
                        self.serialInstance.write("d\n-1500.0\n")
                        
                    print "constantes rotation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        self.serialInstance.write("d\n300.0\n")
                        pas+=1
                    else:
                        try:
                            val = str(float(raw_input()))
                            self.serialInstance.write("cr"+cte.replace("\r","").replace("\n","")+"\n"+val+"\n")
                            self.serialInstance.write("d\n300.0\n")
                            pas+=1
                        except:
                            pass
                
            elif choix == "t":
                while True :
                    if (pas > 4):
                        pas = 0
                        self.serialInstance.write("d\n-1500.0\n")
                    
                    print "constantes translation : p,d,i. q pour quitter."
                    cte = str(raw_input())
                    if cte == "q":
                        break
                    elif cte == "a":
                        self.serialInstance.write("d\n300.0\n")
                        pas+=1
                    else:
                        try :
                            val = str(float(raw_input()))
                            self.serialInstance.write("ct"+cte.replace("\r","").replace("\n","")+"\n"+val+"\n")
                            self.serialInstance.write("d\n300.0\n")
                            pas+=1
                        except :
                            pass
        
    def lire(self):
        """
        Permet de lire un message de ltestPosition'asservissement autre que celui lu par le thread d'acquisition.
        """
        while not self.robotInstance.new_message:
            time.sleep(0.01)
        self.robotInstance.new_message = False
        return self.robotInstance.message
        
        
    def scriptPipeauNewStrategie(self):
        """
        try :
            #script
            asserInstance.gestionAvancer(300)
            asserInstance.gestionAvancer(300,"forcer")
            return "scriptOK"
        except :
            return "BAD_TRIP"
        """
            
    def testFonctions(self):
        
        raw_input()
        serieActionneurs.changer_angle(130)
        raw_input()
        serieActionneurs.changer_angle(90)
        raw_input()
        self.asserInstance.avancer(200)
        raw_input()
        changerVitesse("translation",1)
        self.asserInstance.avancer(-200)
        raw_input()
        changerVitesse("translation",2)
        self.asserInstance.avancer(200)
        raw_input()
        self.asserInstance.tourner(1.57)
        raw_input()
        self.asserInstance.goTo(outils_math.point.Point(300, 300))
        raw_input()
        
    def ramasserTotem(self):
        angle_max = True
        serieActionneurs.changer_angle(160)
        while True :
            print "a : avance, r : reculer, t : bouger angle, tt : spécifier angle, o : orientation"
            choix = raw_input("~Sopal\'INT~ ")
            if choix == "q":
                break
            elif choix == "a":
                self.asserInstance.avancer(100)
            elif choix == "r":
                self.asserInstance.avancer(-200)
            elif choix == "t":
                if angle_max :
                    serieActionneurs.changer_angle(135)
                else :
                    serieActionneurs.changer_angle(150)
                angle_max = not angle_max
            
            elif choix == "tt":
                angl = raw_input("angle ? ")
                serieActionneurs.changer_angle(int(angl))
            elif choix == "o":
                orient = raw_input("orientation ? ")
                self.asserInstance.tourner(float(orient))
                
                
    def scriptTestStruct0(self):
        try:
            #1ère action effectuée
            print "ca marche ! "
            #le script est validé
            return True
        except:
            return False
            
    
    def scriptTestStruct1(self):
        try:
            #1ère action effectuée
            print "yeeeees"
            #2ème action lève une exception
            print 4/0
            #3ème action ne sera pas effectuée
            print "yoyoyo"
            #le script ne sera pas validé
            return True
        except:
            return False