# -*- coding: utf-8 -*-

import decision
import carte
import robot
import timer

class Strategie(decision.Decision, timer.Timer):
    """
    Classe permettant de construire une stratégie
    
    :param strategie: Type de stratégie à adopter :
                        - 1 : Stratégie en carton.
                        - 2 : Stratégie un peu mieux.
                        - 3 : Stratégie sopalin.
    :type strategie:  int

    """
    def __init__(self, strategie):
        self.strategie = strategie
        timer.Timer.__init__(self)
        
    def prendreDecision(self): 
        """
        Retourne la décision prise par le robot. Pour les conventions, voir /lib/decision.py
        """
        
        if self.strategie == 1 :
            pass
        
        elif self.strategie == 2:
            pass
        
        elif self.strategie == 3 :
            pass
        