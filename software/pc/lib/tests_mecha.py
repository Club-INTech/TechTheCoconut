# -*- coding: utf-8 -*-

import sys, os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lolilol
import log
log = log.Log(__name__)

class Tests_mecha():
    """
    Classe permettant de tester les différents mouvements et le niveau de la batterie avant de démarrer l'homologation ou les matchs
    """
    def __init__(self):
        # Lancement des tests
        if constantes["Tests_mecha"]["batterie_test"]:
            self.batterie = self.test_batterie()
        if constantes["Tests_mecha"]["actionneurs_test"]:
            self.test_actionneurs()
        if constantes["Tests_mecha"]["deplacement_test"]:
            self.test_deplacement()
        if constantes["Tests_mecha"]["recalage_test"]:
            self.test_recalage()
        if constantes["Tests_mecha"]["capteurs_test"]:
            self.test_capteurs()
    
    def test_batterie(self):
        """
        Teste l'état de la batterie par rapport aux contraintes des profils
        
        :return: Test réussi ? True si réussi, False si échec
        :rtype: bool
        """
        lolilol.son('bruitages/jackpot.mp3')
        log.logger.info("Test des batteries ...")
        p = os.popen('acpi')
        string = p.readline().replace('\n', '')
        
        # Battery 0: Discharging, 24%, 00:28:54 remaining\n
        if re.search("Discharging", string):
            pourcentage = int(re.findall('[0-9]+%', string)[0].replace('%', ''))
            temps_restant = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}', string)[0].split(":")
            log.logger.debug("Batterie à "+str(pourcentage)+"% ("+temps_restant[0]+":"+temps_restant[1]+":"+temps_restant[2]+")")
            if pourcentage <= constantes["Tests_mecha"]["batterie_contraintes"]["pourcentage_min"] \
            or (int(temps_restant[0]) == 0 and int(temps_restant[1]) <= constantes["Tests_mecha"]["batterie_contraintes"]["minutes_min"]):
                log.logger.critical("Test des batteries ERREUR, batterie à "+str(pourcentage)+"% ("+temps_restant[0]+":"+temps_restant[1]+":"+temps_restant[2]+")")
                # Envoi d'un message à tous les gens connectés
                f = file('/tmp/acpi', 'w')
                f.write(string)
                f.close()
                os.popen('wall < /tmp/acpi 2> /dev/null')
                return False
            log.logger.warn("Test des batteries OK")
            return True
        else:
            log.logger.warn("Test des batteries OK")
            return True

    def test_actionneurs(self):
        """
        Teste l'état des actionneurs en les faisant fonctionner
        
        :return: Test réussi ? True si réussi, False si échec
        :rtype: bool
        """
        lolilol.son('bruitages/jackpot.mp3')
        log.logger.info("Test des actionneurs ...")
        #TODO Coder la méthode
        if False: #TODO à modifier
            log.logger.critical("Test des actionneurs ERREUR")
            return False
        log.logger.warn("Test des actionneurs OK")
        return True
    
    def test_deplacement(self):
        """
        Teste l'état du déplacement en faisant bouger le robot avec goto, avancer et tourner
        
        :return: Test réussi ? True si réussi, False si échec
        :rtype: bool
        """
        lolilol.son('bruitages/jackpot.mp3')
        log.logger.info("Test du déplacement ...")
        #TODO Coder la méthode
        if False: #TODO à modifier
            log.logger.critical("Test du déplacement ERREUR")
            return False
        log.logger.warn("Test du déplacement OK")
        return True

    def test_recalage(self):
        """
        Teste l'état du recalage en se recalant et en regardant si les coordonnées actuelles du robot ne sont pas folles
        
        :return: Test réussi ? True si réussi, False si échec
        :rtype: bool
        """
        lolilol.son('bruitages/jackpot.mp3')
        log.logger.info("Test du recalage ...")
        #TODO Coder la méthode
        if False: #TODO à modifier
            log.logger.critical("Test du recalage ERREUR")
            return False
        log.logger.warn("Test du recalage OK")
        return True

    def test_capteurs(self):
        """
        Teste l'état du capteur en vérifiant que les valeurs récupérées ne sont pas folles
        
        :return: Test réussi ? True si réussi, False si échec
        :rtype: bool
        """
        lolilol.son('bruitages/jackpot.mp3')
        log.logger.info("Test des capteurs ...")
        #TODO Coder la méthode
        if False: #TODO à modifier
            log.logger.critical("Test des capteurs ERREUR")
            return False
        log.logger.warn("Test des capteurs OK")
        return True