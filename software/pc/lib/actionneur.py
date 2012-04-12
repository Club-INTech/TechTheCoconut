# -*- coding: utf-8 -*-

import serie
import log
import peripherique
import __builtin__

# Ajout de constantes de develop si on ne passe pas par la console INTech
if not hasattr(__builtin__, "constantes"):
    import profils.develop.constantes
    __builtin__.constantes = profils.develop.constantes.constantes

log = log.Log(__name__)

# Conversion du chiffre décimal a en chaîne de caract. de 0 et de 1, de longueur nbBits
def bin(a, nbBits) :
    s = ''
    t = {'0' : '000', '1' : '001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110', '7':'111'}
    for c in oct(a)[1:] :
        s += t[c]
    l = len(s.lstrip('0'))
    result = '0'*(nbBits - l)
    return result+s.lstrip('0')

class Actionneur(serie.Serie):
    """
    Classe permettant de gérer un actionneur
    
    :param nom: nom du moteur concerné. Utiliser les lettres h (haut) b (bas) g (gauche) et d (droite). Exemple : hd ou bg. (On choisit gauche et droite dans le repère du rorbot)
    :type nom: string
    
    :param vitesse: Vitesse de déplacement de l'actionneur
    :type vitesse: int (entre 0 et 500) DEFAUT : 500
    
    :param position: Position du moteur par rapport au robot vu de derrière
    :type position: string du type "hg", "hd", "bg" ou "bd".
    
    :param id: id de l'actionneur (de 0 à 3 normalement)
    :type id: int
    
    """
    # Le périphérique, le débit, le timeout et le nom sont les mêmes pour tous les actionneurs
    def __init__(self, position, id, vitesse = 500):
        self.angle      = 0
        self.vitesse    = vitesse
        self.position   = position
        self.id         = id
        
        
        self.demarrer()
        
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
        if position != "ALL" and position != self.position :
            if angle >= constantes["Actionneurs"]["angleMax"] :
                angle = constantes["Actionneurs"]["angleMax"]
            elif angle <= constantes["Actionneurs"]["angleMin"] :
                angle = constantes["Actionneurs"]["angleMin"]
            
            self.serieInstance.write("GOTO" + "\n\r")
            self.serieInstance.write(str(int(self.id)) + "\n\r")
            self.serieInstance.write(str(int(angle))   + "\n\r")
        
        
    def changerVitesse(self, nouvelleVitesse) :
        """
        Changer la vitesse de rotation de TOUS les actionneurs branchés
        
        :param nouvelleVitesse: Nouvelle vitesse des actionneurs
        :type nouvelleVitesse: int (entre 0 et 1000)
        """
        
        if vitesse >= 1000 :
            vitesse = 1000
        elif vitesse <= 0 :
            vitesse = 0
        
        self.serieInstance.write("CH_VITESSE" + "\n\r")
        self.serieInstance.write(str(int(nouvelleVitesse)) + "\n\r")
        
    def getAngle(self):
        """
        Envoie une requête pour obtenir la position de chaque bras.
        NOTE Ne marcheras sans doute jamais. :'(
        """
        #self.serieCaptInstance.write(self.nom + '\n '+ '0' + '\n '  + '0')
        ##serie.Serie.lire()
        #self.angle = self.file_attente.get(lu)

    def reset(self):
        """
        Réinitialise l'actionneur
        """
        self.deplacer(90)
        
    def stop(self):
        """
        Arrête l'actionneur en urgence
        """
        self.serieInstance.write(self.nom + '\n '+ '1' + '\n '  + '0')#TODO modifier selon convention
        #self.getAngle()
        serie.Serie.stop()
        