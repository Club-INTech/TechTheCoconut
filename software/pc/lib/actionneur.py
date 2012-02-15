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
        
        
        
    def deplacer(self, angle, vitesse = None, reponse = None):
        """
        Envoyer un ordre à l'actionneur
        :angle : angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :vitesse : vitesse de la rotation
        :reponse : booleen pour demander une réponse ou non
        """
<<<<<<< HEAD
        if angle > 170:
            log.logger.info("La valeur demandé " + str(angle) + " est trop grande, on ramène cette valeur à 170°")
            angle = 170
        elif angle < 0:
            log.logger.info("La valeur demandé " + str(angle) + " est trop petite, on ramène cette valeur à 0°")
            angle = 0
        self.ecrire('nom : ' + self.nom + '\nangle : ' + str(angle) + '\nreponse : ' + str(reponse) + '\nvitesse : ' + str(vitesse))
        
        
=======
        if angle < 170 and angle > 0:
            actionneur.ecrire('nom : '+self.nom, '\nangle : ' + angle + '\nreponse : ' + reponse + '\nvitesse : ' + vitesse)
>>>>>>> 9d90902cf80b60e00bc59a58bb7aa7693a2c4cf7
