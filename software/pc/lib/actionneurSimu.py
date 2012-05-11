# -*- coding: utf-8 -*-

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


class Actionneur_simu():
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
        if not hasattr(Actionneur_simu, 'initialise') or not Actionneur_simu.initialise:
            Actionneur_simu.initialise = True
            
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("[Actionneurs]  ne peut importer instance.robotInstance")
        
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
        
        if position == "ALL":
            log.logger.info("[Actionneurs] 4 bras à : " + str(angle))
        elif position == "G":
            log.logger.info("[Actionneurs] bras gauches à : " + str(angle))
        elif position == "D":
            log.logger.info("[Actionneurs] bras droits à : " + str(angle))
        else:
            if "hg" in position:
                log.logger.info("[Actionneurs] hg à : " + str(angle))
            if "hd" in position:
                log.logger.info("[Actionneurs] hd à : " + str(angle))
            if "bg" in position:
                log.logger.info("[Actionneurs] bg à : " + str(angle))
            if "bd" in position:
                log.logger.info("[Actionneurs] bd à : " + str(angle))
        
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
        
        log.logger.info("[Actionneurs] Changement de la vitesse à la nouvelle vitesse : " + str(vitesse))
        

        
    def flash_id(self, nouvelID) :
        """
        Flashage de l'id
        """
        log.logger.info("[Actionneurs] Flashage de l'ID à l'ID : " + str(nouvelID))
        
        
    def stop(self):
        """
        Arrête l'actionneur en urgence
        """
        log.logger.info("[Actionneurs] Arrêt des bras")
        
    #------------------------------------------------#
    #       METHODES BAS NIVEAU                      #
    #------------------------------------------------#  
    
    def goto(self, id, angle) :
        # On considère que angle est dans les bonnes valeurs.
        log.logger.info("[Actionneurs] Goto à l'angle :" + str(angle));
        
    def calculRayon(self, angle):
        """
        Modifie le rayon du cercle circonscrit au robot par rapport au centre d'origine (bras rabattus).
        Le calcul ne se fait que sur un bras (inférieur droit dans le repère du robot) puisque le tout est symétrique.
        
        :param angle: angle entre la face avant du robot et les bras en bas du robot. Unité :  radian
        :type angle: float
        """
        
        #récupération des constantes nécessaires:
        log.logger.info('[Actionneurs] Calcul du rayon et du centre du robot')
        
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
        
