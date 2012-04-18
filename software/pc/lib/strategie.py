# -*- coding: utf-8 -*-

import outils_math.point as point

import carte
import robot
import timer, time
import threading
import math

import log
log = log.Log(__name__)

import __builtin__
import script


carte = carte.Carte()

class Strategie(threading.Thread):
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
        self.actions = []
        self.timerStrat = timer.Timer()
        
        
        
        # Remplir le tableau actions d'actions à faire (Thibaut)
        self.initialiserActionsAFaire()
        
        #--------------------------------
        #TODO : à mettre dans constantes
        
        self.rayonRobotsAdverses = 200.0
        
        #--------------------------------
        
        # Résolution d'un bug de timer infini.
        if not hasattr(Strategie, "prendreDecisions") :

            log.logger.info("Lancement de la stratégie numéro " + str(strategie))
            
        #------------------------------#
        #-- Définition des instances --#
        #------------------------------#
        
            
        try :
            self.asserInstance = __builtin__.instance.asserInstance
        except :
            log.logger.error("Impossible d'importer l'instances globale d'asservissement")
            
        try :
            self.capteurInstance = __builtin__.instance.capteurInstance
        except :
            log.logger.error("Impossible d'importer l'instances globale des capteurs")
        
        try :
            self.actionInstance = __builtin__.instance.actionInstance
        except :
            log.logger.error("Impossible d'importer l'instances globale des actionneurs")
            
        try :
            self.robotInstance = __builtin__.instance.robotInstance
        except :
            log.logger.error("Impossible d'importer l'instances globale du robot")
            
        try :
            self.scriptInstance = __builtin__.instance.scriptInstance
        except :
            log.logger.error("Impossible d'importer l'instances globale de scripts")
            
        try :
            self.baliseInstance = __builtin__.instance.baliseInstance  # NOTE Convention ? (Thibaut)            
        except :
            log.logger.error("Impossible d'importer la balise capteur")
            
            
    def gestionAvancer(self, distance, instruction = ""):
        """
        méthode de haut niveau pour translater le robot
        prend en paramètre la distance à parcourir en mm
        et en facultatif une instruction "auStopNeRienFaire" ou "forcer"
        """
        
        print "#avancer à "+str(distance)+", "+instruction
        
        posAvant = self.asserInstance.getPosition()
        retour = self.asserInstance.avancer(distance)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            ##1
            #stopper le robot
            self.asserInstance.immobiliser()
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
                
            else:
                #reculer de ce qui a été avancé
                posApres = self.asserInstance.getPosition()
                dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                if distance != 0: 
                    signe = distance/abs(distance)
                else:
                    signe = 1
                self.gestionAvancer(-signe*dist,"sansRecursion")
                #recommencer le déplacement
                self.gestionAvancer(distance,"sansRecursion")
        
        if retour == "obstacle" :
            ##2 
            #ajoute un robot adverse sur la table, pour la recherche de chemin
            orientation = self.asserInstance.getOrientation()
            position = self.asserInstance.getPosition()
            
            adverse = outils_math.point.Point(position.x + (self.asserInstance.maxCapt+self.rayonRobotsAdverses)*math.cos(orientation),position.y + (self.asserInstance.maxCapt+self.rayonRobotsAdverses)*math.sin(orientation))
            __builtin__.instance.ajouterRobotAdverse(adverse)
            
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
            else:
                
                ##3
                #stopper le robot
                self.asserInstance.immobiliser()
                #attente que la voie se libère
                ennemi_en_vue = True
                debut_timer = int(timerStrat.getTime())
                while ennemi_en_vue and (int(timerStrat.getTime()) - debut_timer) < 4 :
                    capteur = self.capteurInstance.mesurer()
                    if capteur < self.asserInstance.maxCapt:
                        print 'gestionAvancer : capteur !'
                    else :
                        print 'gestionAvancer : la voie est libre !'
                        ennemi_en_vue = False
                    
                if not ennemi_en_vue:
                    #baisser vitesse
                    self.asserInstance.changerVitesse("translation", 1)
                    
                    #finir le déplacement
                    posApres = self.asserInstance.getPosition()
                    dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                    if distance != 0:
                        signe = distance/abs(distance)
                    else:
                        signe = 1
                    self.gestionAvancer(distance-signe*dist)
                    
                    #remettre vitesse
                    self.asserInstance.changerVitesse("translation", 2)
                    
                else:
                    #mettre à jour l'attribut position du robot
                    
                    #stopper l'execution du script parent
                    raise Exception
                
        if retour == "stoppe" and instruction == "sansRecursion":
            ##4
            #mettre à jour l'attribut position du robot
            
            #stopper l'execution du script parent
            
            raise Exception
            
        if retour == "stoppe" and instruction == "forcer":
            ##5
            
            #augmenter vitesse
            self.asserInstance.changerVitesse("translation", 3)
            
            #finir le déplacement
            posApres = self.asserInstance.getPosition()
            dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
            if distance != 0:
                signe = distance/abs(distance)
            else:
                signe = 1
            self.gestionAvancer(distance-signe*dist)
            
            #remettre vitesse
            self.asserInstance.changerVitesse("translation", 2)
            
            
    def gestionTourner(self, angle, instruction = ""):
        
        """
        méthode de haut niveau pour tourner le robot
        prend en paramètre l'angle à parcourir en radians
        et en facultatif une instruction "auStopNeRienFaire" ou "forcer"
        """
        
        #l'angle spécifié dans les scripts est valable pour un robot violet.
        if __builtin__.constantes['couleur'] == "r":
            angle = math.pi - angle
        if angle > math.pi:
            angle = angle - 2*math.pi
        if angle < -math.pi:
            angle = angle + 2*math.pi
        
        print "#tourner à "+str(angle)+", "+instruction
        
        orientAvant = self.asserInstance.getOrientation()
        retour = self.asserInstance.tourner(angle)
        
        if retour == "timeout" or (retour == "stoppe" and not instruction):
            
            #stopper le robot
            self.asserInstance.immobiliser()
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
                
            else:
                ##1
                #tourner inversement à ce qui a été tourné
                self.gestionTourner(orientAvant,"sansRecursion")
                #recommencer le déplacement
                self.gestionTourner(angle,"sansRecursion")
        
        if retour == "stoppe" and instruction == "sansRecursion":
            ##4
            #mettre à jour l'attribut orientation du robot
            
            #stopper l'execution du script parent
            raise Exception
            
        if retour == "stoppe" and instruction == "forcer":
            ##5
            #augmenter vitesse
            self.asserInstance.changerVitesse("rotation", 3)
            #finir le déplacement
            self.gestionTourner(angle)
            #remettre vitesse
            self.asserInstance.changerVitesse("rotation", 2)
            
    def lancer(self) :
            # Gestion de l'arrêt au bout de 90 secondes :
            Strategie.prendreDecisions = True
            
            # Lancement du timer.
            self.timer.lancer()
        
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
                success = self.rafflerTotem()
                if success :
                    success = self.rafflerTotem(ennemi = True)
                    if success :
                        success = self.rafflerTotem(nord = True)
                        if success :
                            success = self.rafflerTotem(ennemi = True, nord = True)
                
                # Si on arrive là, c'est que le script d'origine est terminé.
                # On appelle choisirAction tant que self.actions n'est pas vide
                while self.actions != [] :
                    self.choisirAction()
                
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
        
        

    # L'utiliser avec goTo(arrivee=trucmuche)
    def goTo(self, arrivee, depart = None):
        if depart == None:
            depart = self.depart
        return self.asserInstance.goTo(depart, arrivee)
        
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
        self.actions.append(["FARMERTOTEM", 0, 1,   9.9 ])
        self.actions.append(["FARMERTOTEM", 1, 0,   9   ])
        self.actions.append(["FARMERTOTEM", 1, 1,   9   ])
        
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

        
        # TODO
        # TODO associer la distance courante à celle de la balise.
        # TODO
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
        # déjà fait. Ex : On a déjà farmé le totem.
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
                self.scriptInstance.rafflerTotem(self.actions[maxID][1], self.actions[maxID][2])
                self.changerPriorite("FARMERTOTEM", [self.actions[maxID][1], self.actions[maxID][2]], -1)
                
            elif self.actions[maxID][0] == "ENFONCERPOUSSOIR" :
                self.scriptInstance.enfoncerPoussoir(self.actions[maxID][1])
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
                    
    
    def strateg_scripts(self):
        if self.scriptInstance.scriptTestStruct0():
            self.scriptInstance.scriptTestStruct1()
        