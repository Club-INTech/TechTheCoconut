# -*- coding: utf-8 -*-

import outils_math.point as point

import decision
import carte
import robot
import timer, time
import threading

import log
log = log.Log(__name__)

import __builtin__

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
            

            
    def lancer(self) :
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
        self.Terminated = True
        log.logger.info("Arrêt de la prise de décisions")
        
    def prendreDecision(self): 
        """
        Retourne la décision prise par le robot. Pour les conventions, voir pc/lib/decision.py
        """
        
        #------------------------------#
        #-- Définition des instances --#
        #------------------------------#
        
        try :
            self.asservissement = __builtin__.instance.asserInstance
            self.capteur        = __builtin__.instance.capteurInstance
            self.actionneur     = __builtin__.instance.actionInstance
            self.robot          = __builtin__.instance.robotInstance
        except :
            log.logger.error("Impossible d'importer les instances globales d'asservissement, capteur, et actionneur")
            
        #------------------------------------#
        #-- STRATEGIE NUMERO 1 : En carton --#
        #------------------------------------#
        
        if self.strategie == 1 :
            # Position de départ.
            #depart = self.robot.position()     #TODO A tester sur le vrai EeePC       
            
            # Tant qu'on peut prendre des décisions
            while Strategie.prendreDecisions :
                success = self.rafflerTotem()
                if success :
                    success = self.rafflerTotem(ennemi = True)
                    if success :
                        success = self.rafflerTotem(nord = True)
                        if success :
                            success = self.rafflerTotem(ennemi = True, nord = True)
                
                
                if self.timer.time() <= 70 :
                    # Prise de décision selon ce qui n'a pas été prise
                    pass
                
                else :
                    # Faire un "tour de piste"
                    pass
                    
                
                   
                    

        #--------------------------------------#
        #-- STRATEGIE NUMERO 2: Un peu mieux --#
        #--------------------------------------#
        
        elif self.strategie == 2:
            pass
        
        elif self.strategie == 3 :
            pass
        
        log.logger.info("ARRET DEFINITIF STRATEGIE")
        
        
    def rafflerTotem(self, ennemi = False, nord = False, versLaCalle = True) :
        """
        Le robot se déplace de façon à raffler un totem
        
        :param ennemi: A mettre à True si on veut raffler le totem ennemi
        :type ennemi: Bool
        
        :param nord: Partie Nord ou Sud du Totem qu'on veut raffler
        :type nord: Bool
        
        :param versLaCalle: A changer si on veut Parcourir le totem de D à G ou l'inverse
        :type versLaCalle: Bool        
        
        """
        pass
    
    def goTo(self.depart, arrivee) :
        return self.asservissement.goTo(depart, arrivee)
        
    def enfoncerPoussoir(self, idPoussoir) :
        """
        Le robot se déplace pour enfoncer le poussoir d'indice idPoussoir
        
        :param idPoussoir: Indice du poussoir, 0 = près de chez nous, 1 = loin de chez nous
        :type idPoussoir: int
        """
        pass
    
    
    
    
    
        