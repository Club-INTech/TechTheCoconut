# -*- coding: utf-8 -*-

import serial
import serie
import log

log=log.Log(constantes['Logs']['logs'], constantes['Logs']['logs_level'], constantes['Logs']['logs_format'], constantes['Logs']['stderr'], constantes['Logs']['stderr_level'], constantes['Logs']['stderr_format'], constantes['Logs']['dossier'])


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
        if angle > 170:
            log.logger.info("La valeur demandé " + str(angle) + " est trop grande, on ramène cette valeur à 170°")
            angle = 170
        elif angle < 0:
            log.logger.info("La valeur demandé " + str(angle) + " est trop petite, on ramène cette valeur à 0°")
            angle = 0
        self.ecrire('nom : ' + self.nom + '\nangle : ' + str(angle) + '\nreponse : ' + str(reponse) + '\nvitesse : ' + str(vitesse))
        
        