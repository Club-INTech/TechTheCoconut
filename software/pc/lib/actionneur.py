# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import serie
import log
import peripherique

log = log.Log()


class Actionneur(serie.Serie):
    """
    Classe permettant de gérer un actionneur
    
    :param nom: nom du moteur concerné. Utiliser les lettres h (haut) b (bas) g (gauche) et d (droite). Exemple : hd ou bg. (On choisit gauche et droite dans le repère du rorbot)
    :type nom: string
    """
    # Le périphérique, le débit, le timeout et le nom sont les mêmes pour tous les actionneurs
    def __init__(self, nom):
        if not hasattr(Actionneur, 'initialise') or not Actionneur.initialise:
            Actionneur.initialise = True
            chemin = peripherique.chemin_de_peripherique("actionneur")
            if chemin:
                serie.Serie.__init__(self, chemin, nom, 9600, 3)
            else:
                log.logger.error("L'actionneur "+nom+" n'est pas chargé")
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
        self.ecrire(self.nom + '\n '+ '0' + '\n '  + '0')
        serie.Serie.lire()
        self.angle = self.file_attente.get(lu)

    def reset(self):
        """
        Réinitialise l'actionneur
        """
        self.ecrire(self.nom + '\n' + '0')
        self.angle = 0
        
    def stop(self):
        """
        Arrête l'actionneur en urgence
        """
        self.ecrire(self.nom + '\n '+ '1' + '\n '  + '0')#TODO modifier selon convention
        self.getAngle()
        serie.Serie.stop()
        