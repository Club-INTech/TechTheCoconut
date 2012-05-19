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

from random import randint



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
        self.couleur = __builtin__.constantes["couleur"]

        
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
            self.serieAsserInstance = __builtin__.instance.serieAsserInstance
            self.asserInstance = __builtin__.instance.asserInstance
            self.simu = False
        except :
            self.asserInstance = __builtin__.instance.asserInstanceDuree
            log.logger.error("Impossible d'importer l'asservissement")
            self.simu = True
        
        try :
            self.actionInstance = __builtin__.instance.actionInstance
        except :
            log.logger.error("Impossible d'importer les actionneurs")
            
        
            
    def lancer(self) :
            
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
        # Tableau : [score espéré, Point de départ , Temps du script,  [nvlle prio si succès, nvlle prio si échec], <METTREÀZERO> ]
        
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
            self.actions =  {"rafflerTotem00" : [13,Point(0,660), 18, [-1, 5], 0],
                             "rafflerTotem01" : [9,Point(0,1500), 18, [-1, 5], 0],
                             "rafflerTotem10" : [6,Point(-920+ 70, 450+180), 40, [-1, 4], 0],
                             
                             "enfoncerPoussoir0" : [5,Point(751.344262295,1445.0), 11,[-1, 3], 0],
                             "enfoncerPoussoir1" : [5,Point(-360, 1510.), 10, [-1, 3], 0],
                             
                             "bourrerCale"       : [0,Point(900, 1000), 10,  [0, 3], 0]
                            }
                            
        elif self.strategie == 2 :
            #self.actions =  {"rafflerTotem00" : [9, [3, 7]],
                             #"rafflerTotem01" : [9, [3, 7]],
                             #"rafflerTotem10" : [6, [1, 4]],
                             
                             #"enfoncerPoussoir0" : [5, [0, 3]],
                             #"enfoncerPoussoir1" : [5, [0, 3]],
                             
                             #"bourrerCale"       : [4, [1, 3]]
                            #}
            
            self.preActions =   [[[1,2], 'preAction_1_2']]       
                                      
        elif self.strategie == 3 :
            pass
        
    # Retourne la position sur la table, qui dépend de la couleur
    def getPositionSymetrisee(self) :
        pos = self.asserInstance.getPosition()
        if self.couleur == "v" :
            return Point(pos.x, pos.y)
        return Point(-pos.x, pos.y)
        
    # Cette fonction est appellée dans une boucle infinie et permet de choisir 
    # l'action la meilleure à réaliser.
    def choisirAction(self) :
        
        poids = []
        temps = []
        
        for action in self.actions.keys() :
            actionAtester = self.actions[action]
            positionRobot = self.getPositionSymetrisee()
            
            positionObjectif = actionAtester[1]
            
            try :
                temps_action = actionAtester[2] + self.asserInstance.getTimeTo(positionRobot, positionObjectif)
            except :
                log.logger.debug("Impossible de lancer getTimeTo")
                temps_action = actionAtester[2] + math.sqrt((positionRobot.x - positionObjectif.x)**2 + (positionRobot.y - positionObjectif.y)**2)/400
            
            # Éliminé si il ne reste pas assez de temps.
            if temps_action >= self.timerStrat.getTimeRemaining() :
                poids_action = -1
                
            else :
                poids_action = float(actionAtester[0])/temps_action
                
            temps.append([action,temps_action])
            poids.append([action,poids_action])
            
        log.logger.info("TEMPS : " + str(temps))
        log.logger.debug("POIDS : " + str(poids))
            
        # On cherche le max des actions
        maxID = -1
        max = 0
        for i in xrange(len(temps)) :
            if poids[i][1] > max :
                max = poids[i][1]
                maxID = i
        
        # Si il ne reste plus rien à faire :
        if maxID == -1 :
            log.logger.debug("Plus aucun script à lancer.")
            try :
                self.scriptInstance.gestionScripts(self.scriptInstance.viderCaleEnnemi)
                return
            except :
                log.logger.error("Impossible de vider la cale de l'ennemi")
                time.sleep(2)
                return
                
        meilleureAction = poids[maxID][0]
        
        print ("Position : " + str(positionRobot))
        
        # Lancement d'une preAction sur le passage de la zone courante à la zone d'action :
        #self.choisirPreAction(self.zoneRobot, self.actions[meilleureAction][2])
        
        # Lancement de la meilleure action :
        try :
            exec("success = self.scriptInstance.gestionScripts(self.scriptInstance." + meilleureAction + ")")
            log.logger.debug("Lancement du script " + meilleureAction + ".")
        except :   
            log.logger.critical("Impossible de lancer " + str(meilleureAction) + " !")
            success = randint(0,3)
            print success
            time.sleep(temps[maxID][1])
            
        if success and self.simu :
            self.asserInstance.setPosition(self.actions[meilleureAction][1])
            
        # Augmentation du nombre d'essai de cette action
        self.actions[meilleureAction][4] += 1
        
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
            
            # Incrémentation du poids du farmage de cale
            if "rafflerTotem" in nomAction :
                try :
                    self.actions["bourrerCale"][0] += 5
                except :
                    pass
        else :
            # Changement du poids des actions
            self.actions[nomAction][0] = self.actions[nomAction][3][1]
            if self.actions[nomAction][4] >= 3 :
                self.actions[nomAction][0] = -1
        
    #TEST
    def strateg_scripts(self):
        if self.scriptInstance.scriptTestStruct0():
            self.scriptInstance.scriptTestStruct1()
        
def t() :
    s = Strategie()
    s.lancer()
