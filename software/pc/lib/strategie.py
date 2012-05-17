# -*- coding: utf-8 -*-

from outils_math.point import Point

import carte
import robot
import timer, time
import math

import log
log = log.Log(__name__)

import __builtin__
import script
import instance



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
    def __init__(self):

        
        self.strategie = constantes['Strategie']
        self.timerStrat = timer.Timer()
        self.actions = {}
        self.preActions     = []
        self.zoneRobot = 1

        
        # Remplir le tableau actions d'actions à faire (Thibaut)
        self.initialiserActionsAFaire()
        
        # Résolution d'un bug de timer infini.
        if not hasattr(Strategie, "prendreDecisions") :
            log.logger.info("Lancement de la stratégie numéro " + str(self.strategie))
            
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
            
        try :
            self.baliseInstance = __builtin__.instance.baliseInstance  # NOTE Convention ? (Thibaut)            
        except :
            log.logger.error("stratégie : ne peut importer instance.baliseInstance")
        
        try :
            self.asserInstance = __builtin__.instance.asserInstance
        except :
            log.logger.error("Impossible d'importer l'asservissement")
        
        try :
            self.actionInstance = __builtin__.instance.actionInstance
        except :
            log.logger.error("Impossible d'importer les actionneurs")
            
        
            
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
                while 42 :
                    self.choisirAction()
                
        #--------------------------------------#
        #-- STRATEGIE NUMERO 2: Un peu mieux --#
        #--------------------------------------#
        
        elif self.strategie == 2:
            while 42 :
                self.choisirAction()
        
        elif self.strategie == 3 :
            pass
        
        log.logger.info("ARRET DEFINITIF STRATEGIE")
        
        
    def initialiserActionsAFaire(self) :
        """
        TYPE D'ACTIONS : [NOM_DE_L_ACTION, +paramètresOptionnels, PRIORITÉ DE L'ACTION]
            NOM_DE_L_ACTION :   "FARMERTOTEM"   +param1 : ennemi, +param2: Nord
                                "ENFONCERPOUSSOIR"                +param : id poussoir
                                "FAIRECHIERENNEMI"
                                "TOURDETABLE"                     +param1 : brasOuverts
                                "DEFENDRE"
                                
                                
            PRIORITÉ DE L'ACTION : Nombre de points rapportés si l'action réussi.
        """
        
        # Nombre de paramètres par actions
        self.actions_nbrParametres = {"FARMERTOTEM":2, "ENFONCERPOUSSOIR":1, "FAIRECHIERENNEMI":0, "TOURDETABLE":1, "DEFENDRE":0,
                                      "BOURRERCALLE":0}
        
        log.logger.debug("Initialisation des actions à faire")
        # Selon le profil de statégie choisi, on peut mettre des priorités différentes pour chaques actions.
        # Tableau : [score espéré, temps d'éxécution, [zone(s) dans lequel se trouve le départ de l'obj], [nvlle prio si succès, nvlle prio si échec]]
        
        #           _________________________________
        #           |               |               |
        #           |      3        |       2       |
        #           |_______________|_______________|           /!\ Ces zones sont vues
        #           |               |               |               depuis un joueur violet
        #           |       4       |        1      |
        #           |_______________|_______________|
        #
        #
        if self.strategie == 1 :
            self.actions =  {"rafflerTotem00" : [9, 25, 1, [3, 7]],
                             "rafflerTotem01" : [9, 27, 2, [3, 7]],
                             "rafflerTotem10" : [6, 30 , 4, [1, 4]],
                             
                             "enfoncerPoussoir0" : [5, 7,2, [0, 3]],
                             "enfoncerPoussoir1" : [5, 7,3, [0, 3]],
                             
                             "bourrerCale"       : [4, 10, 1, [1, 3]]
                            }
                            
            self.preActions =   [[[1,2], 'preAction_1_2']]

            
            #self.preActions.append([0, "preAction_totem01_1", "self.asserInstance.getPosition().y < 670"])
            #self.preActions.append([0, "preAction_totem01_2", "self.asserInstance.getPosition().x > 400"])
            
            
            
            
        elif self.strategie == 2 :
            self.actions =  {"rafflerTotem00" : [9, 25, 1, [3, 7]],
                             "rafflerTotem01" : [9, 27, 2, [3, 7]],
                             "rafflerTotem10" : [6, 30 , 4, [1, 4]],
                             
                             "enfoncerPoussoir0" : [5, 7,2, [0, 3]],
                             "enfoncerPoussoir1" : [5, 7,3, [0, 3]],
                             
                             "bourrerCale"       : [4, 10, 1, [1, 3]]
                            }
            
            self.preActions =   [[[1,2], 'preAction_1_2']]       
                                      
        elif self.strategie == 3 :
            pass
        
    
    # Cette fonction est appellée dans une boucle infinie et permet de choisir 
    # l'action la meilleure à réaliser.
    def choisirAction(self) :
        poids = []
        temps = []
        try :
            self.zoneRobot = asserInstance.getZone()
        except :
            log.logger.error("Impossible de lancer asser.getZone()")

        debug = True


        for action in self.actions.keys() :
            actionAtester = self.actions[action]
            zoneObjectif  = actionAtester[2]
            difference = self.getDifferenceZone(self.zoneRobot, zoneObjectif)
            
            temps_action = float(actionAtester[1]+(1+difference)*5)
            poids_action = actionAtester[0]/temps_action
            
            temps.append([action,temps_action])
            poids.append([action,poids_action])
        
        if debug :
            log.logger.debug("TEMPS :: " + str(temps))
            log.logger.debug("POIDS :: " + str(poids))
            
        # On cherche le max des actions
        maxID = -1
        max = 0
        for i in xrange(len(temps)) :
            if poids[i][1] > max :
                max = poids[i][1]
                maxID = i
                
        meilleureAction = poids[maxID][0]
        
        # Lancement d'une preAction sur le passage de la zone courante à la zone d'action :
        self.choisirPreAction(self.zoneRobot, self.actions[meilleureAction][2])
        
        # Lancement de la meilleure action :
        try :
            exec("success = self.scriptInstance.gestionScripts(self.scriptInstance." + meilleureAction + ")")
        except :
            log.logger.critical("Impossible de lancer " + str(meilleureAction) + " !")
            success = True
            self.zoneRobot = self.actions[meilleureAction][2]
            time.sleep(5)
            
        # Changement des scores des actions
        self.changerScore(meilleureAction, success)
        
        
    # Retourne le nombre de zones à franchir pour passer d'une à l'autre.
    def getDifferenceZone(self, zone1, zone2) :
        if zone1 == zone2 :
            return 0
        if abs(zone1-zone2) == 2 :
            return 2            
        return 1
        
    # Lance une preAction lors du passage de la zone 1 à la zone 2
    def choisirPreAction(self, zone1, zone2) :
        for i in xrange(len(self.preActions)) :
            print zone1, zone2
            if self.preActions[i][0] == [zone1, zone2] :
                try :
                    exec("self.scriptInstance.gestionScripts(self.scriptInstance." + self.preActions[i][1] + ")")
                    return
                except :
                    log.logger.error("Impossible de lancer la préaction " + self.preActions[i][1] + " !")
                    time.sleep(2)

    # Changement de priorité d'une entrée du tableau self.actions
    def changerScore(self, nomAction, success) :
        if success : 
            self.actions[nomAction][0] = self.actions[nomAction][3][0]
        else :
            self.actions[nomAction][0] = self.actions[nomAction][3][1]

    #TEST
    def strateg_scripts(self):
        if self.scriptInstance.scriptTestStruct0():
            self.scriptInstance.scriptTestStruct1()
        
def t() :
    s = Strategie()
    s.lancer()
