# -*- coding: utf-8 -*-

import outils_math.point as point

import carte
import robot
import timer, time
import math

import log
log = log.Log(__name__)

import __builtin__
import script


carte = carte.Carte()

class Strategie():
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
        self.timerStrat = timer.Timer()
        self.actions = []
        
        # Remplir le tableau actions d'actions à faire (Thibaut)
        self.initialiserActionsAFaire()
        
        # Résolution d'un bug de timer infini.
        if not hasattr(Strategie, "prendreDecisions") :
            log.logger.info("Lancement de la stratégie numéro " + str(strategie))
            
        #------------------------------#
        #-- Définition des instances --#
        #------------------------------#
            
        try :
            self.robotInstance = __builtin__.instance.robotInstance
        except :
            log.logger.error("stratégie : ne peut importer instance.robotInstance")
            
        try :
            self.scriptInstance = __builtin__.instance.scriptInstance
        except :
            log.logger.error("stratégie : ne peut importer instance.scriptInstance")
            
        """
        try :
            self.baliseInstance = __builtin__.instance.baliseInstance  # NOTE Convention ? (Thibaut)            
        except :
            log.logger.error("stratégie : ne peut importer instance.baliseInstance")
        """
            
    def lancer(self) :
            # Gestion de l'arrêt au bout de 90 secondes :
            Strategie.prendreDecisions = True
            
            # Lancement du timer.
            self.timerStrat.lancer()
        
            # Lancer la de prise de décision
            self.prendreDecision()
        
        
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
        
            
        #------------------------------------#
        #-- STRATEGIE NUMERO 1 : En carton --#
        #------------------------------------#
        
        if self.strategie == 1 :
            # Position de départ.
            #self.depart = self.robotInstance.position()     
            
            # Tant qu'on peut prendre des décisions
            while Strategie.prendreDecisions :
                
                # Si on arrive là, c'est que le script d'origine est terminé.
                # On appelle choisirAction tant que self.actions n'est pas vide
                while self.actions != [] :
                    self.choisirAction()
                
                if self.timerStrat.time() <= 70 :
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
        
        
    def initialiserActionsAFaire(self) :
        """
        Thibaut.
        
        TYPE D'ACTIONS : [NOM_DE_L_ACTION, +paramètresOptionnels, PRIORITÉ DE L'ACTION]
            NOM_DE_L_ACTION :   "FARMERTOTEM"   +param1 : ennemi, +param2: Nord
                                "ENFONCERPOUSSOIR"                +param : id poussoir
                                "CHOPEROBJET"  (lingot ou disque) +param : Point
                                "FAIRECHIERENNEMI"                +param : AUCUN
                                
                                
            PRIORITÉ DE L'ACTION : A coter de 1 à 5. La stratégie l'utilisera en cas de conflits.
        """
        log.logger.info("Initialisation des actions à faire")
        self.actions.append(["FARMERTOTEM", 0, 0,   10  ])
        self.actions.append(["FARMERTOTEM", 0, 1,   10  ])
        self.actions.append(["FARMERTOTEM", 1, 0,   10  ])
        self.actions.append(["FARMERTOTEM", 1, 1,   10  ])
        
        self.actions.append(["ENFONCERPOUSSOIR", 1, 5])
        self.actions.append(["ENFONCERPOUSSOIR", 2, 5])
        
        #self.actions.append(["CHOPEROBJET", carte.disques[0].position, 2])   # disque 1
        #self.actions.append(["CHOPEROBJET", carte.disques[1].position, 2])   # disque 2
        #self.actions.append(["CHOPEROBJET", carte.disques[21].position, 3])  # disques du bas
        #self.actions.append(["CHOPEROBJET", carte.lingots[1].position, 1])
        
        self.actions.append(["FAIRECHIERENNEMI", 1])    #
        self.actions.append(["TOURDETABLE", 1])         #
        self.actions.append(["DEFENDRE", 1])            #
    
    def choisirAction(self) :
        """
        CETTE FONCTION PERMET A LA STRATEGIE DE CHOISIR QUELLE ACTION CHOISIR
        """
        
        # TODO associer la distance courante à celle de la balise.
        distance = 1
        
        # Poids du coefficient Nombre de Points / Durée
        k1 = 1
        
        # Poids du coefficient "Adversaire proche de l'objectif" :
        k2 = 1
        
        poids = []
        # Attribution des scores via les coefficients.   (k1*NbrPoints + k2*Prochitude de l'adv)
        for i in range(len(self.actions)) :
            poids.append(k1*self.actions[i][-1] + k2*distance)
            
        # On cherche ceux qui font des points positifs (sinon, c'est qu'on est dans un cas
        # déjà fait. Ex : On a déjà farmé le totem.)
        max = 0
        maxID = -1
        
        # On cherche l'action qui fait le meilleur score 
        for i in range(len(self.actions)) :
            if poids[i] > max :
                max = poids[i]
                maxID = i
                
        # Si maxID == -1 c'est que il ne reste rien à faire.
        # TODO Qu'est-ce qu'on fait dans ce cas là ?!
        if maxID < -1 :
            log.logger.info("ZUT ALORS ! Plus d'actions à faire")
            return
        
        
        # Sinon, on prend l'action
        try :
            if self.actions[maxID][0] == "FARMERTOTEM" :
                exec ("self.scriptInstance.gestionScript(self.scriptInstance.rafflerTotem"+str(self.actions[maxID][1])+str(self.actions[maxID][2])+")")
                self.changerPriorite("FARMERTOTEM", [self.actions[maxID][1], self.actions[maxID][2]], -1)
                
            elif self.actions[maxID][0] == "ENFONCERPOUSSOIR" :
                exec ("self.scriptInstance.gestionScript(enfoncerPoussoir"+str(self.actions[maxID][1])+")")
                self.changerPriorite("ENFONCERPOUSSOIR", [self.actions[maxID][1]], -1)
                
            elif self.actions[maxID][0] == "FAIRECHIERENNEMI" :
                self.scriptInstance.faireChierEnnemi()
                self.changerPriorite("FAIRECHIERENNEMI", [], self.actions[maxID][-1]-0.01)
                
            elif self.actions[maxID][0] == "TOURDETABLE":
                self.scriptInstance.tourDeTable()
                self.changerPriorite("TOURDETABLE", [], self.actions[maxID][-1]-0.01)
                
            elif self.actions[maxID][0] == "DEFENDRE":
                self.scriptInstance.defendreBase()
                self.changerPriorite("DEFENDRE", [], self.actions[maxID][-1]-0.01)
        except :
            log.logger.error("La stratégie ne peut pas lancer d'actions")
        
        
    def changerPriorite(self, nomAction, params, nouvellePriorite) :
        """
        
        Change la priorité d'une action dans le tableau self.actions
        
        
        :param nomAction: NOM_DE_L_ACTION
        :type nomAction: string
        
        :param params: Tableau contenant les paramètres optionels
        :type params: tableau de trucs
        
        :param nouvellePriorite: Nouvelle priorité pour l'action
        :type nouvellePriorite: int (entre 0 et 5)
        """
        for i in range(len(self.actions)) :
            if self.actions[i][0] == nomAction :
                found = 1
                for j in range(len(params)) :
                    if self.actions[i][j+1] != params[j] :
                        
                        found = 0
                        break
                if found :
                    self.actions[i][1+len(params)] = nouvellePriorite
                    return 1
                    
    #TEST
    def strateg_scripts(self):
        if self.scriptInstance.scriptTestStruct0():
            self.scriptInstance.scriptTestStruct1()
        