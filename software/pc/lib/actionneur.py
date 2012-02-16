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
        peripherique : Nom de l'usb
        nom : nom du moteur concerné. Utiliser les lettres h (haut) b (bas) g (gauche) et d (droite). Exemple : hd ou bg. (On choisit gauche et droite dans le repère du rorbot)
        debit : debit de bode à fixer
        timeout : temps avant abandon
        """
        self.nom = nom
        
        
        
    def deplacer(self, angle, vitesse = None):
        """
        Envoyer un ordre à l'actionneur
        :angle : angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :vitesse : vitesse de la rotation
        :reponse : booleen pour demander une réponse ou non
        """

        if angle < 170 and angle > 0:
            actionneur.ecrire(self.nom + '\n ' + angle +'\n ' + vitesse)
            return actionneur.lire()
        
