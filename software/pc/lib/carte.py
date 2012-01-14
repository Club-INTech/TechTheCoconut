# -*- coding: utf-8 -*-

class Carte:
    """
    Classe permettant de gérer l'aire de jeu
    """
    def __init__(self):
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
        Carte.disques.append(disque)
    
    def enlever_disque(self, pos, orientation):
        pass
    
    def ajouter_lingot(self, lingot):
        Carte.lingots.append(lingot)
    
    def enlever_lingot(self, pos, orientation):
        pass
    
    def ajouter_totem(self, totem) :
        Carte.totems.append(totem)
    
    def ajouter_regletteEnBois(self, regletteEnBois) :
        Carte.reglettesEnBois.append(regletteEnBois)
    
    def ajouter_palmier(self, palmier) :
        Carte.palmiers.append(palmier)
    
    def ajouter_poussoir(self, poussoir) :
        Carte.poussoirs.append(poussoir)
    
    def enfoncer_poussoir(self, id):
        Carte.poussoirs[id].setEtatOK()
    
    def ajouter_carteAuTresor(self, carteAuTresor) :
        Carte.cartesAuxTresor.append(carteAuTresor)
    
    def arracher_carte_tresor(self, id):
        Carte.cartesAuxTresor[id].setEtatOK()