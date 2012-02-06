# -*- coding: utf-8 -*-

import serial
import serie
import log

#log=log.Log(constantes['Logs']['logs'], constantes['Logs']['logs_level'], constantes['Logs']['logs_format'], constantes['Logs']['stderr'], constantes['Logs']['stderr_level'], constantes['Logs']['stderr_format'], constantes['Logs']['dossier'])


class Actionneur:
    """
    Classe permettant de gérer un actionneur
    """
    def __init__(self, peripherique, nom, debit, timeout):
        actionneur = Serie(peripherique, 'actionneur '+nom, debit, timeout)
        self.nom = nom
        
        
        
    def deplacer(self, angle, vitesse = None, reponse = None):
        """
        Envoyer un ordre à l'actionneur
        :angle : angle à atteindre (angle mesuré entre la face avant du robot et le bras)
        :vitesse : vitesse de la rotation
        :reponse : booleen pour demander une réponse ou non
        """
        if angle < 170 and angle > 0:
            actionneur.ecrire('nom : '+self.nom, '\nangle : ' + angle + '\nreponse : ' + reponse + '\nvitesse : ' + vitesse)
        
        