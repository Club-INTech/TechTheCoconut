# -*- coding: utf-8 -*-

import decision
import carte
import robot

class Strategie(decision.Decision):
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
        
    def prendreDecision(self): 
        """
        Retourne la décision prise par le robot. Pour les conventions, voir /lib/decision.py
        """
        
        pass