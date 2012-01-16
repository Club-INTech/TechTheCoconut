# -*- coding: utf-8 -*-

import log as mod_log
log = mod_log.Log()


class Carte:
    """
    Classe permettant de gérer l'aire de jeu
    """
    def __init__(self):
        log.logger.info("Création de la table en cours...\n")
        Carte.lingots = []
        Carte.disques = []
        Carte.totems  = []
        Carte.poussoirs=[]
        Carte.cartesAuxTresor = []
        Carte.palmiers= []
        Carte.reglettesEnBois = []
        Carte.zones   = []
        
    
    def goto(self, depart, arrivee):
        pass
    
    def ajouter_disque(self, disque):
        log.logger.info("Ajout d'un disque dans l'objet Carte\n")
        Carte.disques.append(disque)
    
    def enlever_disque(self, pos, orientation):
        pass
    
    def ajouter_lingot(self, lingot):
        log.logger.info("Ajout d'un lingot dans l'objet Carte\n")
        Carte.lingots.append(lingot)
    
    def enlever_lingot(self, pos, orientation):
        pass
    
    def ajouter_totem(self, totem) :
        log.logger.info("Ajout d'un totem dans l'objet Carte\n")
        Carte.totems.append(totem)
    
    def ajouter_regletteEnBois(self, regletteEnBois) :
        log.logger.info("Ajout d'une reglette en bois dans l'objet Carte\n")
        Carte.reglettesEnBois.append(regletteEnBois)
    
    def ajouter_palmier(self, palmier) :
        log.logger.info("Ajout d'un palmier dans l'objet Carte\n")
        Carte.palmiers.append(palmier)
    
    def ajouter_poussoir(self, poussoir) :
        log.logger.info("Ajout d'un bouton poussoir dans l'objet Carte\n")
        Carte.poussoirs.append(poussoir)
    
    def enfoncer_poussoir(self, id):
        Carte.poussoirs[id].setEtatOK()
    
    def ajouter_carteAuTresor(self, carteAuTresor) :
        log.logger.info("Ajout d'une carte au trésor dans l'objet Carte\n")
        Carte.cartesAuxTresor.append(carteAuTresor)
    
    def arracher_carte_tresor(self, id):
        Carte.cartesAuxTresor[id].setEtatOK()
        
    def ajouter_zone(self, zone) :
        log.logger.info("Ajout d'une zone dans l'objet Carte \n")
        Carte.zones.append(zone)
        # LIGNE 69 ! !! ! !! ! ! FUCK Y(e)ah !
        
        