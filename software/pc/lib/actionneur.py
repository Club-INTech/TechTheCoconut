# -*- coding: utf-8 -*-

import serie
import log
import peripherique
import __builtin__

import time

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
            self.serieInstance = __builtin__.instance.serieActionneurInstance
        
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
                
        # Envoi des infos
        if position == "ALL" or "hg" in position:
            self.goto(self.ids["hg"], 180+3-angle)
        if position == "ALL" or "hd" in position:
            self.goto(self.ids["hd"], angle)
        if position == "ALL" or "bg" in position:
            self.goto(self.ids["bg"], angle+5)
        if position == "ALL" or "bd" in position:
            self.goto(self.ids["bd"], 180+3-angle)


        
        
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
        
        self.serieInstance.write("CH_VITESSE" + "\n\r")
        self.serieInstance.write(str(int(nouvelleVitesse)) + "\n\r")
        
     
    def stop(self):
        """
        Arrête l'actionneur en urgence
        """
        pass
        
    #------------------------------------------------#
    #       METHODES BAS NIVEAU                      #
    #------------------------------------------------#  
    
    def goto(self, id, angle) :
        # On considère que angle est dans les bonnes valeurs.
        self.serieInstance.write("GOTO" + "\n\r")
        time.sleep(0.01)
        self.serieInstance.write(str(int(id)) + "\n\r")
        time.sleep(0.01)
        self.serieInstance.write(str(int(angle))   + "\n\r")
        time.sleep(0.01)
        
