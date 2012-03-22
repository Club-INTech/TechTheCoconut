# -*- coding: utf-8 -*-

class Decision:
    """
    Classe permettant de prendre une décision stratégique
    
    
    Types de décisions :    
                            - ["NULL"] : Le robot ne fait rien
    
                            - ["VIDERTOTEM", ennemi, haut, versLaCalle] :
                                    Le robot vient vider un totem. "ennemi" et "haut" sont des variables booléenes
                                    La variable versLaCalle est booléenne, et détermine le sens de vidage du totem
                                    (de droite à gauche ou l'inverse).
                                    
                            - ["ENFONCERPOUSSOIR", numéro] :
                                    Le robot vient enfoncer le poussoir. "numéro" détermine quel poussoir enfoncer, 
                                    si numéro = 1, c'est le plus proche de notre camp, si numéro = 2, c'est le plus
                                    loin de chez nous.
                                    
                            - ["DECOUVRIRCARTE"] :
                                    Le robot vient découvrir la carte. Normalement pas utilisé.
                                    
                            - ["VISITERADVERSAIRE"] :
                                    Le robot vient raffler la calle du robot adverse.
                                    
                            - ["RENTRERALAMAISON"] :
                                    Le robot rentre dans sa calle.
                                    
                            - ["ALLERA", position] :
                                    Le robot va à la position donnée.
                                    
                            - ["ANGLEBRAS", angle] :
                                    Ouvre les bras (ou les ferme) selon la valeur donnée.
    """
    def __init__(self):
        self.decisionPrecedente = ["NULL"]
        self.decisionSuivante   = ["NULL"]