# -*- coding: utf-8 -*-

import serie
import log
import peripherique
import __builtin__

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
            self.serieInstance = __builtin__.instance.serieCaptInstance
        
    def deplacer(self, angle):
        """
        Envoyer un ordre à l'actionneur
        
        :param angle: angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :type angle: int (entre 0 et 180)

        """

        if angle >= 0 and angle <= 180 :
            angle /= 180.
            angle *= 31             # On se rapporte à un nombre codé sur 5 bits (2^5 = 32)
            angle = int(angle)
            
            # Si le moteur est monté à l'envers ou est à droite (et vice-versa)
            if (self.position[0] == 'hd' or self.position == 'bg') :
                angle = 31-angle
            
            self.serieCaptInstance.write(chr('0' + bin(self.id, 2) + bin(angle, 5), 2))
            
        else :
            log.logger.error("L'angle cible de l'actionneur doit être compris entre 0 et 500")
        
    def changerVitesse(self, nouvelleVitesse) :
        """
        Changer la vitesse de rotation de TOUS les actionneurs branchés
        
        :param nouvelleVitesse: Nouvelle vitesse des actionneurs
        :type nouvelleVitesse: int (entre 0 et 500)
        """
        if nouvelleVitesse >= 0 and nouvelleVitesse <= 500 :
            nouvelleVitesse = nouvelleVitesse/500.
            nouvelleVitesse *= 31                   # Codage sur 5 bits
            nouvelleVitesse = int(nouvelleVitesse)
            self.serieCaptInstance.write(chr(int('1' + '00' + bin(nouvelleVitesse, 5), 2)))
            log.logger.info("La vitesse des actionneurs a été changée")
            
        else :
            log.logger.error("La nouvelle vitesse de l'actionneur doit être comprise entre 0 et 500")
        
    def getAngle(self):
        """
        Envoie une requête pour obtenir la position de chaque bras.
        NOTE Ne marcheras sans doute jamais. :'(
        """
        self.serieCaptInstance.write(self.nom + '\n '+ '0' + '\n '  + '0')
        #serie.Serie.lire()
        self.angle = self.file_attente.get(lu)
        
    def change_id(self, nouvel_id) :
        """
        Permet de changer l'ID de tous les actionneurs branchés
        WARNING Cette méthode change TOUS les IDs de TOUS les actionneurs branchés.
        
        :param nouvel_id: Nouvel ID des actionneurs branchés
        :type nouvel_id: int (entre 0 et 3)
        """
        if nouvel_id >= 0 and nouvel_id <= 3 :
            self.serieCaptInstance.write(chr(int('1' + '01' + '000' + bin(int(nouvel_id), 2), 2)))
        
        else :
            log.logger.error("Le nouvel id des actionneurs doit être compris entre 0 et 3")

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
        