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
        
        self.endmsg = "\n\r"
        
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
        
        self.serieInstance.write("CH_VITESSE" + self.endmsg)
        self.serieInstance.write(str(int(nouvelleVitesse)) + self.endmsg)
        
    def test_demarrage(self, mode = "LONG") :
        """
        Test de démarrage des bras Ax12. Un paramètre optionnel est mis en place pour
        pouvoir régler la durée du test.
        
        :param mode: Type de test
        :type mode: String "LONG" | "SHORT". Défault : "LONG"
        
        """
        
        if mode = "LONG" :
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
            
        elif mode = "SHORT" :
            self.deplacer(80)
            time.sleep(1)
            self.deplacer(0)
            time.sleep(1)
            log.logger.debug("Test des bras : Fait")

        
    def flash_id(self, nouvelID) :
        """
        Flashage de l'id
        """
        self.serieInstance.write("FLASH_ID" + self.endmsg)
        self.serieInstance.write(str(int(nouvelID)) + self.endmsg)
        
        
    def stop(self):
        """
        Arrête l'actionneur en urgence
        """
        self.serieInstance.write("UNASSERV" + self.endmsg)
        
    #------------------------------------------------#
    #       METHODES BAS NIVEAU                      #
    #------------------------------------------------#  
    
    def goto(self, id, angle) :
        # On considère que angle est dans les bonnes valeurs.
        self.serieInstance.write("GOTO" + self.endmsg)
        time.sleep(0.01)
        self.serieInstance.write(str(int(id)) + self.endmsg)
        time.sleep(0.01)
        self.serieInstance.write(str(int(angle))   + self.endmsg)
        time.sleep(0.01)
        
