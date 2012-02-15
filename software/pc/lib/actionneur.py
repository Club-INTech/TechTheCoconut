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
        #actionneur = serie.Serie(peripherique, 'actionneur '+nom, debit, timeout)
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
