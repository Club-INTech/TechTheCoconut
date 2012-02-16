# -*- coding: utf-8 -*-

import serial
import serie
import log

log = log.Log()


class Actionneur(serie.Serie):
    """
    Classe permettant de gérer un actionneur
    """
    def __init__(self, peripherique, nom, debit, timeout):
        """
        :param peripherique: Nom de l'usb
        :type peripherique: string
        :param nom: nom du moteur concerné. Utiliser les lettres h (haut) b (bas) g (gauche) et d (droite). Exemple : hd ou bg. (On choisit gauche et droite dans le repère du rorbot)
        :type nom: string
        :param debit: debit de bode à fixer
        :type debit: int
        :param timeout: temps avant abandon
        :type timeout: int
        """
        serie.Serie.def __init__(peripherique, nom, debit, timeout)
        self.nom = nom
        self.angle = 0;
        
        
        
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
        
    def getAngle(self, nom):
        """
        Envoie une requête pour obtenir la position de chaque bras.
        """
        serie.Serie.ecrire(nom + '\n '+ '0' + '0')
        serie.Serie.lire()
        return self.file_attente.get(lu)
