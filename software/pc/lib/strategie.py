# -*- coding: utf-8 -*-

import outils_math.point as point

import decision
import carte
import robot
import timer, time
import threading
import math

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
        
        ############
        #TODO : à mettre dans constantes
        #vitesses en pwm pour les scripts
        self.VITESSE_PRUDENCE_EVITEMENT = 80
        self.VITESSE_NORMALE = 180
        self.VITESSE_INSISTER = 255
        
        self.rayonRobotsAdverses = 200.0
        
        ############
        
        # Résolution d'un bug de timer infini.
        if not hasattr(Strategie, "prendreDecisions") :

            log.logger.info("Lancement de la stratégie numéro " + str(strategie))
            
        #------------------------------#
        #-- Définition des instances --#
        #------------------------------#
        
        try :
            
            self.asserInstance = __builtin__.instance.asserInstance
            self.serieAsservInstance = __builtin__.instance.instanciationSerie
            self.capteurInstance = __builtin__.instance.capteurInstance
            self.actionInstance = __builtin__.instance.actionInstance
            self.robotInstance = __builtin__.instance.robotInstance
        except :
            log.logger.error("Impossible d'importer les instances globales d'asservissement, capteur, et actionneur")
            
    def gestionAvancer(self, distance, instruction = ""):
        
        """
        méthode de haut niveau pour translater le robot
        prend en paramètre la distance à parcourir en mm
        et en facultatif une instruction "auStopNeRienFaire"
        """
        
        posAvant = self.asserInstance.MAJposition()
        ret = self.asserInstance.avancer()
        
        if ret == "timeout" or (ret == "stoppe" and not instruction):
            ##1
            #reculer de ce qui a été avancé
            posApres = self.asserInstance.MAJposition()
            dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
            signe = distance/abs(distance)
            gestionAvancer(-signe*dist,"sansRecursion")
            #recommencer le déplacement
            gestionAvancer(distance,"sansRecursion")
        
        if ret == obstacle :
            ##2 
            #ajoute un robot adverse sur la table, pour la recherche de chemin
            orientation = self.asserInstance.MAJorientation()
            position = self.asserInstance.MAJposition()
            
            #300 : distance au robot adverse à la detection, 200 : rayon moyen du robot adverse
            adverse = outils_math.point.Point(position.x + (300+200)*math.cos(orientation),position.y + (300+200)*math.sin(orientation))
            __builtin__.instance.ajouterRobotAdverse(adverse)
            
            if instruction == "sansRecursion":
                ##4
                #mettre à jour l'attribut position du robot
                
                #stopper l'execution du script parent
                raise Exception
            else:
                pass
                """
                ##3
                #stopper le robot
                asserInstance.immobiliser()
                #attente que la voie se libère
                #début timer
                #gestion timer
                #gestion capteurs
                while ROBOT_DEVANT and TIMER < 4sec :
                    pass
                if not ROBOT_DEVANT:
                    #baisser pwm
                   asserInstance.changerPWM("translation", VITESSE_PRUDENCE_EVITEMENT)
                    
                    #finir le déplacement
                    posApres = self.asserInstance.MAJposition()
                    dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
                    signe = distance/abs(distance)
                    gestionAvancer(distance-signe*dist)
                    
                    #remettre pwm
                   asserInstance.changerPWM("translation", VITESSE_NORMALE)
                else:
                    #mettre à jour l'attribut position du robot
                    
                    #stopper l'execution du script parent
                    raise Exception
                """
                
        if ret == "stoppe" and instruction == "sansRecursion":
            ##4
            #mettre à jour l'attribut position du robot
            
            #stopper l'execution du script parent
            raise Exception
            
        if ret == "stoppe" and instruction == "forcer":
            ##5
            #augmenter pwm
            asserInstance.changerPWM("translation", VITESSE_INSISTER)
            
            #finir le déplacement
            posApres = self.asserInstance.MAJposition()
            dist = math.sqrt((posApres.x - posAvant.x) ** 2 + (posApres.y - posAvant.y) ** 2)
            signe = distance/abs(distance)
            gestionAvancer(distance-signe*dist)
                    
            #remettre pwm
            asserInstance.changerPWM("translation", VITESSE_NORMALE)
            
        
    
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
        
            
        #------------------------------------#
        #-- STRATEGIE NUMERO 1 : En carton --#
        #------------------------------------#
        
        if self.strategie == 1 :
            # Position de départ.
            self.depart = self.robotInstance.position()     #TODO A tester sur le vrai EeePC       
            
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
    
    # L'utiliser avec goTo(arrivee=trucmuche)
    def goTo(self, arrivee, depart = None):
        if depart == None:
            depart = self.depart
        return self.asserInstance.goTo(depart, arrivee)
        
    def enfoncerPoussoir(self, idPoussoir) :
        """
        Le robot se déplace pour enfoncer le poussoir d'indice idPoussoir
        
        :param idPoussoir: Indice du poussoir, 0 = près de chez nous, 1 = loin de chez nous
        :type idPoussoir: int
        """
        pass