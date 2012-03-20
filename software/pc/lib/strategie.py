# -*- coding: utf-8 -*-

import decision
import carte
import robot
import timer, time
import threading

import log
log = log.Log(__name__)

class Strategie(decision.Decision, threading.Thread):
    """
    Classe permettant de construire une stratégie
    
    :param strategie: Type de stratégie à adopter :
                        - 1 : Stratégie en carton.
                        - 2 : Stratégie un peu mieux.
                        - 3 : Stratégie sopalin.
    :type strategie:  int

    """
    def __init__(self, strategie=1):

        
        self.strategie = strategie
        self.timer = timer.Timer() 
        
        # Résolution d'un bug de timer infini.
        if not hasattr(Strategie, "prendreDecisions") :

            log.logger.info("Lancement de la stratégie numéro " + str(strategie))
            
            # Gestion de l'arrêt au bout de 90 secondes :
            Strategie.prendreDecisions = True
            
            # Lancement du timer.
            self.timer.lancer()
        
            # Lancer le thread de prise de décision
            threading.Thread.__init__(self, name="prendreDecision", target=self.prendreDecision)
            self.start()
        
    def arreterPrendreDecisions(self) :
        """
        Appeller cette méthode lorsque l'on souhaite arrêter de prendre des décisions
        Cette méthode est appellée depuis le timer.        
        """
        
        Strategie.prendreDecisions = False
        log.logger.info("Arrêt de la prise de décisions")
        
    def prendreDecision(self): 
        """
        Retourne la décision prise par le robot. Pour les conventions, voir pc/lib/decision.py
        """
        
        #------------------------------------#
        #-- STRATEGIE NUMERO 1 : En carton --#
        #------------------------------------#
        if self.strategie == 1 :
            # Tant qu'on peut prendre des décisions
            while Strategie.prendreDecisions :
                # Avant une seconde : on va raffler la partie 'haute' de notre Totem
                if self.timer.getTime() <= 1 :
                    log.logger.info("TEST STRATEGIE, Rafle")
                    time.sleep(1.5)
                    
                # etc.
                elif self.timer.getTime() <= 10 :
                    log.logger.info("TEST STRATEGIE, Rafle")
                    time.sleep(10.5)
                    
                elif self.timer.getTime() <= 20 :
                    log.logger.info("TEST STRATEGIE, end")
                    time.sleep(5)                    
            
        
        elif self.strategie == 2:
            pass
        
        elif self.strategie == 3 :
            pass
        