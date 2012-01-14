# -*- coding: utf-8 -*-

class Carte:
    """
    Classe permettant de gérer l'aire de jeu
    """
    def __init__(self):
        carte.lingots = []
        carte.disques = []
        carte.totems  = []
        carte.poussoirs=[]
        carte.cartesAuxTresor = []
        carte.palmiers= []
        carte.reglettesEnBois = []
        carte.zones   = []
        
    
    def goto(self, depart, arrivee):
        pass
    
    def ajouter_disque(self, disque):
        carte.disques.append(disque)
    
    def enlever_disque(self, pos, orientation):
        pass
    
    def ajouter_lingot(self, lingot):
        carte.lingots.append(lingot)
    
    def enlever_lingot(self, pos, orientation):
        pass
    
    def ajouter_totem(self, totem) :
        carte.totems.append(totem)
    
    def ajouter_regletteEnBois(self, regletteEnBois) :
        carte.reglettesEnBois.append(regletteEnBois)
    
    def ajouter_palmier(self, palmier) :
        carte.palmiers.append(palmier)
    
    def ajouter_poussoir(self, poussoir) :
        carte.poussoirs.append(poussoir)
    
    def enfoncer_poussoir(self, id):
        carte.poussoirs[id].setEtatOK()
    
    def ajouter_carteAuTresor(self, carteAuTresor) :
        carte.cartesAuxTresor.append(carteAuTresor)
    
    def arracher_carte_tresor(self, id):
        carte.cartesAuxTresor[id].setEtatOK()