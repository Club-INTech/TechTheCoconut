# -*- coding: utf-8 -*-

import serie
import log
import __builtin__
import outils_math.point as point
import math
import time
import sys

sys.path.append('../')
import profils.develop.constantes

# Ajout de constantes de develop si on ne passe pas par la console INTech
if not hasattr(__builtin__, "constantes"):
    import profils.develop.constantes
    __builtin__.constantes = profils.develop.constantes.constantes

log = log.Log(__name__)


class Actionneur(serie.Serie):
    """
    Classe permettant de gérer un actionneur
    
    :param ids: Dico contenant l'id de l'AX12 en fct° de sa position
    
    """
    # Le périphérique, le débit, le timeout et le nom sont les mêmes pour tous les actionneurs
    def __init__(self):
        self.ids        = {"hg":1, "hd":2, "bg":0, "bd":3}
        self.demarrer()
        
    # Démarrage.
    def demarrer(self):
        if not hasattr(Actionneur, 'initialise') or not Actionneur.initialise:
            Actionneur.initialise = True
            self.serieActionneurInstance = __builtin__.instance.serieActionneurInstance
            
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("actionneur : ne peut importer instance.robotInstance")
        
    def deplacer(self, angle, position = "ALL"):
        """
        Envoyer un ordre à l'actionneur
        
        :param angle: angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :type angle: int (entre 0 et ANGLEMAXI)
        
        :param position: Position de l'actionneur à tourner (OPTIONEL)
        :type position: string "hg" | "hd" | "bg" | "bd". Défaut : ALL

        """
        
        # Pas d'overflow, pas de trucs dégueux
        if angle >= constantes["Actionneurs"]["angleMax"] :
            angle = constantes["Actionneurs"]["angleMax"]
        elif angle <= constantes["Actionneurs"]["angleMin"] :
            angle = constantes["Actionneurs"]["angleMin"]
        
        #calcul du nouveau rayon du robot
        self.calculRayon(math.pi*angle/180)
                
        # Envoi des infos
        if position == "ALL" or "hg" in position:
            self.goto(self.ids["hg"], 180+3-angle)
        if position == "ALL" or "hd" in position:
            self.goto(self.ids["hd"], angle)
        if position == "ALL" or "bg" in position:
            self.goto(self.ids["bg"], angle+5)
        if position == "ALL" or "bd" in position:
            self.goto(self.ids["bd"], 180+9-angle)
        
        #print "##################\n"+str(self.robotInstance.rayon)+"\n#############\n"

        
    def changerVitesse(self, nouvelleVitesse) :
        """
        Changer la vitesse de rotation de TOUS les actionneurs branchés
        
        :param nouvelleVitesse: Nouvelle vitesse des actionneurs
        :type nouvelleVitesse: int (entre 0 et 1000)
        """
        
        if nouvelleVitesse >= 1000 :
            nouvelleVitesse = 1000
        elif nouvelleVitesse <= 0 :
            nouvelleVitesse = 0
        
        self.serieActionneurInstance.ecrire("CH_VITESSE")
        self.serieActionneurInstance.ecrire(str(int(nouvelleVitesse)))
        
    def test_demarrage(self, mode = "LONG") :
        """
        Test de démarrage des bras Ax12. Un paramètre optionnel est mis en place pour
        pouvoir régler la durée du test.
        
        :param mode: Type de test
        :type mode: String "LONG" | "SHORT". Défault : "LONG"
        
        """
        
        if mode == "LONG" :
            for i in range(4) :
                self.goto(i, 80)
                time.sleep(1)
            log.logger.debug("Test Actionneurs goto : Fait.")
            
            for i in ["hd", "hg", "bg", "bd"] :
                self.deplacer(50, i)
                time.sleep(1)
            log.logger.debug("Test Actionneurs déplacer : Fait")
            
            self.changerVitesse(100)
            self.deplacer(20)
            time.sleep(1)
            
            log.logger.debug("Test Actionneurs changerVitesse : Fait")
            self.changerVitesse(500)
            self.deplacer(0)
            
        elif mode == "SHORT" :
            self.deplacer(80)
            time.sleep(1)
            self.deplacer(0)
            time.sleep(1)
            log.logger.debug("Test des bras : Fait")

        
    def flash_id(self, nouvelID) :
        """
        Flashage de l'id
        """
        self.serieActionneurInstance.ecrire("FLASH_ID")
        self.serieActionneurInstance.ecrire(str(int(nouvelID)))
        
        
    def stop(self):
        """
        Arrête l'actionneur en urgence
        """
        self.serieActionneurInstance.ecrire("UNASSERV")
        
    #------------------------------------------------#
    #       METHODES BAS NIVEAU                      #
    #------------------------------------------------#  
    
    def goto(self, id, angle) :
        # On considère que angle est dans les bonnes valeurs.
        self.serieActionneurInstance.ecrire("GOTO")
        time.sleep(0.04)
        self.serieActionneurInstance.ecrire(str(int(id)))
        time.sleep(0.04)
        self.serieActionneurInstance.ecrire(str(int(angle)))
        time.sleep(0.04)
        
    def calculRayon(self, angle):
        """
        Modifie le rayon du cercle circonscrit au robot par rapport au centre d'origine (bras rabattus).
        Le calcul ne se fait que sur un bras (inférieur droit dans le repère du robot) puisque le tout est symétrique.
        
        :param angle: angle entre la face avant du robot et les bras en bas du robot. Unité :  radian
        :type angle: float
        """
        
        #récupération des constantes nécessaires:
        log.logger.info('Calcul du rayon et du centre du robot')
        
        #[]la longueur est sur x, largeur sur y
        longueur_bras = profils.develop.constantes.constantes["Coconut"]["longueurBras"]
        largeur_robot = profils.develop.constantes.constantes["Coconut"]["largeurRobot"]
        longueur_robot = profils.develop.constantes.constantes["Coconut"]["longueurRobot"]
        
        rayon_original = math.sqrt((longueur_robot/2) ** 2 + (largeur_robot/2) ** 2)
        proj_x = -longueur_bras*math.cos(float(angle))
        proj_y = longueur_bras*math.sin(float(angle))
        
        #point à l'extremité du bras droit
        sommet_bras = point.Point(longueur_robot/2 + proj_x, largeur_robot/2 + proj_y)
        rayon_avec_bras = math.sqrt((sommet_bras.x) ** 2 + (sommet_bras.y) ** 2)
        
        self.robotInstance.rayon = max(rayon_avec_bras,rayon_original)
        
    def test(self, temps = 0.3) :
        i = 0
        while 1 :
            self.deplacer((i%16)*10)
            time.sleep(temps)
            if i%16 == 0 :
                time.sleep(1)
            i += 1
        
    #------------------------------------------------#
    #       DANSE =D                                 #
    #------------------------------------------------#  
        
    def danse(self) :
        
        time.sleep(1)
        
        self.deplacer(90)
        time.sleep(1)
        self.deplacer(160)
        time.sleep(1)
        self.deplacer(0)
        time.sleep(1)
        self.deplacer(45)
        time.sleep(1)
        self.deplacer(120)
        time.sleep(1)
        self.deplacer(45, "bg")
        time.sleep(0.3)
        self.deplacer(45, "bd")
        time.sleep(0.3)
        self.deplacer(45, "hg")
        self.deplacer(45, "hd")
        time.sleep(0.3)
        self.deplacer(100)
        time.sleep(0.2)
        self.deplacer(120)
        time.sleep(0.3)
        self.deplacer(140, "bg")
        self.deplacer(140, "bd")

        self.deplacer(160, "hg")
        self.deplacer(160, "hd")
        time.sleep(0.5)
        self.deplacer(45, "hd")
        self.deplacer(45, "hg")
        self.changerVitesse(100)
        self.deplacer(20, "bd")
        self.deplacer(20, "bg")
        self.changerVitesse(500)
        time.sleep(0.5)
        self.deplacer(160, "hg")
        self.deplacer(160, "hd")
        time.sleep(0.5)
        self.deplacer(45, "hd")
        self.deplacer(45, "hg")
        time.sleep(0.5)
        self.deplacer(160, "hg")
        self.deplacer(160, "hd")
        time.sleep(0.5)
        self.deplacer(45, "hd")
        self.deplacer(45, "hg")
        time.sleep(0.5)
        self.deplacer(160, "hg")
        self.deplacer(160, "hd")
        time.sleep(0.5)
        self.deplacer(45, "hd")
        self.deplacer(45, "hg")
        time.sleep(0.5)
        self.deplacer(160, "hg")
        self.deplacer(160, "hd")
        time.sleep(0.5)
        self.deplacer(45, "hd")
        self.deplacer(45, "hg")
        time.sleep(0.5)
        
        self.deplacer(40, "bg")
        self.deplacer(40, "hg")
        self.deplacer(160, "hd")
        self.deplacer(160, "bd")
        time.sleep(0.5)
        self.changerVitesse(150)
        self.deplacer(40, "bd")
        self.deplacer(40, "hd")
        self.deplacer(160, "hg")
        self.deplacer(160, "bg")
        time.sleep(1.5)
        self.changerVitesse(500)
        self.deplacer(40, "bg")
        self.deplacer(40, "hg")
        self.deplacer(160, "hd")
        self.deplacer(160, "bd")
        time.sleep(0.5)
        self.changerVitesse(150)
        self.deplacer(40, "bd")
        self.deplacer(40, "hd")
        self.deplacer(160, "hg")
        self.deplacer(160, "bg")
        time.sleep(1.5)
        self.changerVitesse(400)
        self.deplacer(40, "bg")
        self.deplacer(160, "bd")
        time.sleep(1)
        self.deplacer(160, "hd")
        self.deplacer(40, "hg")
        self.deplacer(160, "bg")
        self.deplacer(40, "bd")
        time.sleep(0.7)
        self.deplacer(90)
        time.sleep(1)
        self.changerVitesse(500)
        
        self.deplacer(80, "bg")
        self.deplacer(80, "bd")
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        time.sleep(0.5)
        self.deplacer(70, "hg")
        self.deplacer(70, "hd")
        self.deplacer(110, "bg")
        self.deplacer(110, "bd")
        time.sleep(0.5)
        self.deplacer(60, "bg")
        self.deplacer(60, "bd")
        self.deplacer(120, "hg")
        self.deplacer(120, "hd")
        time.sleep(1)
        self.deplacer(70, "hg")
        self.deplacer(70, "hd")
        self.deplacer(110, "bg")
        self.deplacer(110, "bd")
        time.sleep(0.5)
        self.deplacer(80, "bg")
        self.deplacer(80, "bd")
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        time.sleep(0.5)
        self.deplacer(90)
        time.sleep(1)
        
        #####################################
        
        self.deplacer(80, "hg")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        time.sleep(0.3)
        self.deplacer(80, "hg")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        time.sleep(0.3)
        
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        time.sleep(0.3)
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        time.sleep(0.3)
        
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        time.sleep(0.3)
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        time.sleep(0.3)
        
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        self.deplacer(80, "bg")
        time.sleep(0.3)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        self.deplacer(100, "bg")
        time.sleep(0.3)
        
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        self.deplacer(80, "bg")
        time.sleep(0.15)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        self.deplacer(100, "bg")
        time.sleep(0.15)
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        self.deplacer(80, "bg")
        time.sleep(0.15)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        self.deplacer(100, "bg")
        time.sleep(0.15)
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        self.deplacer(80, "bg")
        time.sleep(0.15)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        self.deplacer(100, "bg")
        time.sleep(0.15)
        self.deplacer(80, "hg")
        self.deplacer(80, "hd")
        self.deplacer(80, "bd")
        self.deplacer(80, "bg")
        time.sleep(0.15)
        self.deplacer(100, "hg")
        self.deplacer(100, "hd")
        self.deplacer(100, "bd")
        self.deplacer(100, "bg")
        time.sleep(0.15)
        
        self.deplacer(160)

        
        

