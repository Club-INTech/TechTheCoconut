# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import serial
import serie
import log

log = log.Log()


class Actionneur(serie.Serie):
    """
    Classe permettant de gérer un actionneur
    """
    # Le périphérique, le débit, le timeout et le nom sont les mêmes pour tous les actionneurs
    def __init__(self, nom):
        """
        :param nom: nom du moteur concerné. Utiliser les lettres h (haut) b (bas) g (gauche) et d (droite). Exemple : hd ou bg. (On choisit gauche et droite dans le repère du rorbot)
        :type nom: string
        """
        if not hasattr(Actionneur, 'initialise') or not Actionneur.initialise:
            Actionneur.initialise = True
            serie.Serie.__init__(self, "/dev/ttyUSB10", nom, 9600, 3)
        self.nom = nom
        self.angle = 0
        
    def deplacer(self, angle, vitesse = None):
        """
        Envoyer un ordre à l'actionneur
        :param angle: angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :type angle: int
        :param vitesse: (facultatif) vitesse de la rotation
        :type vitesse: float
        :return: booleen pour demander une réponse ou non
        :rtype: string
        """

        if angle < 170 and angle > 0:
            actionneur.ecrire(self.nom + '\n ' + str(angle) +'\n ' + str(vitesse))
            serie.Serie.lire()
            self.angle = self.file_attente.get(lu)
        
    def getAngle(self):
        """
        Envoie une requête pour obtenir la position de chaque bras.
        """
        serie.Serie.ecrire(nom + '\n '+ '0' + '0')
        serie.Serie.lire()
        self.angle = self.file_attente.get(lu)
