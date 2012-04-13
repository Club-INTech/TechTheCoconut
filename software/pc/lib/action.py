# -*- coding: utf-8 -*-

import serie
import log
import peripherique
import __builtin__

# Ajout de constantes de develop si on ne passe pas par la console INTech
if not hasattr(__builtin__, "constantes"):
    import profils.develop.constantes
    __builtin__.constantes = profils.develop.constantes.constantes

log = log.Log(__name__)

class Action :
    
    def __init__(self) :
        pass

    def rafflerTotem(self, ennemi = False, nord = False, versLaCalle = True) :
        """
        (Thibaut)
        
        Le robot se déplace de façon à raffler un totem
        
        :param ennemi: A mettre à True si on veut raffler le totem ennemi
        :type ennemi: Bool
        
        :param nord: Partie Nord ou Sud du Totem qu'on veut raffler
        :type nord: Bool
        
        :param versLaCalle: A changer si on veut Parcourir le totem de D à G ou l'inverse
        :type versLaCalle: Bool        
        
        """
        pass
        

    def enfoncerPoussoir(self, idPoussoir) :
        """
        (Thibaut)
        
        Le robot se déplace pour enfoncer le poussoir d'indice idPoussoir
        
        :param idPoussoir: Indice du poussoir, 0 = près de chez nous, 1 = loin de chez nous
        :type idPoussoir: int
        """
        pass