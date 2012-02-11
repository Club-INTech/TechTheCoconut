# -*- coding: utf-8 -*-

import log as mod_log


class Carte:
    """
    Classe permettant de gérer l'aire de jeu
    """
    def __init__(self):
        self.log = mod_log.Log()
        self.log.logger.info("Création de la table en cours...\n")
        # On initialise seuleument si les listes n'existent pas déjà
        if not hasattr(Carte, 'lingots'):
            Carte.lingots = []
        if not hasattr(Carte, 'disques'):
            Carte.disques = []
        if not hasattr(Carte, 'totems'):
            Carte.totems  = []
        if not hasattr(Carte, 'poussoirs'):
            Carte.poussoirs=[]
        if not hasattr(Carte, 'cartesAuxTresor'):
            Carte.cartesAuxTresor = []
        if not hasattr(Carte, 'palmiers'):
            Carte.palmiers= []
        if not hasattr(Carte, 'reglettesEnBois'):
            Carte.reglettesEnBois = []
        if not hasattr(Carte, 'zones'):
            Carte.zones   = []
        
    
    def goto(self, depart, arrivee):
        pass
    
    def ajouter_disque(self, disque):
        self.log.logger.info("Ajout d'un disque dans l'objet Carte\n")
        Carte.disques.append(disque)
    
    def enlever_disque(self, pos, orientation):
        pass
    
    def ajouter_lingot(self, lingot):
        self.log.logger.info("Ajout d'un lingot dans l'objet Carte\n")
        Carte.lingots.append(lingot)
    
    def enlever_lingot(self, pos, orientation):
        pass
    
    def ajouter_totem(self, totem) :
        self.log.logger.info("Ajout d'un totem dans l'objet Carte\n")
        Carte.totems.append(totem)
    
    def ajouter_regletteEnBois(self, regletteEnBois) :
        self.log.logger.info("Ajout d'une reglette en bois dans l'objet Carte\n")
        Carte.reglettesEnBois.append(regletteEnBois)
    
    def ajouter_palmier(self, palmier) :
        self.log.logger.info("Ajout d'un palmier dans l'objet Carte\n")
        Carte.palmiers.append(palmier)
    
    def ajouter_poussoir(self, poussoir) :
        self.log.logger.info("Ajout d'un bouton poussoir dans l'objet Carte\n")
        Carte.poussoirs.append(poussoir)
    
    def enfoncer_poussoir(self, id):
        Carte.poussoirs[id].setEtatOK()
    
    def ajouter_carteAuTresor(self, carteAuTresor) :
        self.log.logger.info("Ajout d'une carte au trésor dans l'objet Carte\n")
        Carte.cartesAuxTresor.append(carteAuTresor)
    
    def arracher_carte_tresor(self, id):
        Carte.cartesAuxTresor[id].setEtatOK()
        
    def ajouter_zone(self, zone) :
        self.log.logger.info("Ajout d'une zone dans l'objet Carte \n")
        Carte.zones.append(zone)
