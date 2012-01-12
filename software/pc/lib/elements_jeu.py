# -*- coding: utf-8 -*-



# Classe Point
import outils_math.point

# Ajout de ../ au path python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import math

# Log
import log
#log = log.Log()

"""
Ce fichier crée les classes des différents objets présents sur le terrain, obstacles et zone.

:TODO: Utiliser les constantes de profil
"""


class ElementARamener :
    """
    Cette classe permet de créer tous les objets à ramener au camp (i.e. Diques et Lingots)
    :note: Les classes Disque et Lingot sont mieux appropriées pour la création d'objets
    
    :param position: position de l'objet à ramener
    :type position: Point
    
    :param orientation: orientation de l'objet à ramener
    :type orientation: float
    
    :param etat: Type actuel de l'objet : A Ramener, En déplacement, Protégée ou Chez l'adversaire
    :type etat: string 'SURLETERRAIN' | 'ENDEPLACEMENT' | 'PROTEGEE' | 'CHEZLADVERSAIRE'
    """
    
    def __init__(self, position, orientation, etat = "SURLETERRAIN") :
        #log.logger.info("Création d'un objet ElementARamener en cours...\n")
        self.position = position
        self.orientation = orientation
        self.etat = etat
        
        
class ElementInfranchissable :
    """
    Cette classe permet de créer tous les objets infranchissables (i.e. totem et règlettes en bois)
    :note: Les classes RegletteEnBois et Totem sont mieux appropriées pour la création d'objets
    
    :param position: position de l'objet à ramener
    :type position: Point
    
    :param orientation: orientation de l'objet à ramener
    :type orientation: float
    
    """
    
    def __init__(self, position, orientation) :
        #log.logger.info("Création d'un objet ElementInfranchissable en cours...\n")
        self.position = position
        self.orientation = orientation
        
        
class ElementQueteAnnexe :
    """
    Cette classe permet de créer tous les objets de quête annexe (i.e. carte au trésor et bouton poussoir)
    
    :param position: position de l'objet de quête annexe
    :type position: Point   (voir lib/outils_math/point.py)
    
    :param orientation: orientation de l'objet quête annexe
    :type orientation: float
    
    :param etat: Etat de l'objet quête annexe (à False si la quête n'est pas remplie, à True sinon)
    :type etat: boolean
    
    :param ennemi: Appartenance de l'objet (à True si il est à nous, à False sinon)
    :type ennemi: boolean
    
    """
    
    def __init__(self, position, orientation, ennemi, etat = False) :
        self.position = position
        self.orientation = orientation
        self.etat = etat
        self.ennemi = ennemi
        
        
class Disque(ElementARamener):
    """
    Classe permettant de créer l'élément de jeu disque
    
    :param position: Position du disque
    :type position: Point
    
    :param orientation: Orientation du disque
    :type orientation: float
    
    :param rayon: Rayon du disque, en mm
    :type rayon: float
    
    :param couleur: Couleur du disque
    :type couleur: string  'NOIR' | 'BLANC'
    
    
    """
    def __init__(self, position, orientation, couleur):
        #log.logger.info("Création d'un objet disque en cours...\n")
        ElementARamener.__init__(self, position, orientation)
        self.rayon = 90 #:TODO: changer la valeur numérique
        self.couleur = couleur
        
    def actualiser(self, position, orientation = 0) :
        """
        Fonction permettant d'actualiser les attributs de l'élement Disque
        
        :param position: Nouvelle position du disque
        :type position: Point
        
        :param orientation: [OPTIONEL] Nouvelle orientation du disque
        :type orientation: float
        
        :TODO: actualiser l'élement self.etat (de la classe ElementARamener)
        """
        self.position = position  
        self.orientation = orientation

class Lingot(ElementARamener):
    """
    Classe permettant de créer l'élement de jeu Lingot
    
    :param position: Position du lingot
    :type position: Point
    
    :param orientation: Orientation du lingot
    :type orientation: float
    
    :param largeur: Largeur du lingot en mm
    :type largeur: int
    
    :param longueur: Longueur du lingot en mm
    :type longueur: int
    
    """
    def __init__(self, position, orientation):
        #log.logger.info("Création d'un objet Lingot en cours...\n")
        ElementARamener.__init__(self, position, orientation)
        self.largeur = 90       #:TODO: changer la valeur numérique
        self.longueur = 160     #:TODO: changer la valeur numérique
    
    def actualiser(self, position, orientation = 0) :
        """
        Fonction permettant d'actualiser les attributs de l'élement Lingot
        
        :param position: Nouvelle position du lingot
        :type position: Point
        
        :param orientation: [OPTIONEL] Nouvelle orientation du lingot
        :type orientation: float
        
        :TODO: Actualiser l'élement self.etat (de la classe ElementARamener)
        
        """
        self.position = position
        self.orientation = orientation
        
class Totem(ElementInfranchissable):
    """
    Classe permettant de créer l'élement de jeu Totem
    :param position: Position du disque
    :type position: Point
    
    :param orientation: Orientation du disque
    :type orientation: float
    
    :param largeur: Largeur du Totem en mm
    :type largeur: int
    
    :param longueur: Longueur du Totem en mm
    :type longueur: int
    
    :param hauteur: Hauteur du Totem en mm
    :type hauteur: int
    
    :param ennemi: [OPTIONEL] Est à True si le totem appartient à l'ennemi, à False sinon
    :type ennemi: boolean
    """
    
    def __init__(self, position, ennemi):
        #log.logger.info("Création d'un objet Totem en cours...\n")
        ElementInfranchissable.__init__(self, position, 0)
        self.ennemi = ennemi    #:TODO: Gérer l'assignation de cet élement en fonction de la position et de notre camp
        
        self.longueur = 5 #:TODO: changer la valeur numérique
        self.largeur = self.longueur #cette variable est inutile mais au moins on peut l'utiliser
        
        self.hauteur = 5 #:TODO: changer la valeur numérique
        

class RegletteEnBois(ElementInfranchissable) :
    """
    Classe permettant de créer l'élément de jeu pour les règlettes en bois
    
    :param angleID: Angle inférieur droit de la règlette.
    :type angleID: Point    (voir lib/outils_math/point.py)
    
    :param angleSG: Angle supérieur gauche de la règlette
    :type angleSG: Point    (voir lib/outils_math/point.py)
    """
    def __init__(self, angleSG, angleID) :
        #log.logger.info("Création d'un objet RegletteEnBois en cours...\n")
        self.angleID = angleID
        self.angleSG = angleSG
        
class Poussoir(ElementQueteAnnexe):
    """
    Classe permettant de créer l'élément de jeu poussoir
    
    :param position: Position du poussoir
    :type position: Point
    
    :param orientation: Orientation du poussoir (toujours égale à Pi/2)
    :type orientation: float
    
    :param ennemi: Est à True si le poussoir appartient à l'ennemi, à False sinon
    :type ennemi: boolean
    
    :param etat: [OPTIONEL] Etat du poussoir (True si enfoncé, False sinon)
    :type etat: boolean
    
    """
    def __init__(self, position, ennemi, etat = False):
        """
        :TODO: Gerer l'assignation de la variable 'enemy' en fonction de la position du poussoir et de notre couleur
        """
        
        #log.logger.info("Création d'un objet Poussoir en cours...\n")
        ElementQueteAnnexe.__init__(self, position, math.pi/2, ennemi, etat)
        
    def setEtatOK(self, etat = True) :
        """
        Fonction permettant d'actualiser l'état du poussoir
        
        :param etat: [OPTIONEL] Mettre False si le bouton se désactive (cas rare et potentiellement indétectable)
        :type etat: boolean
        
        """
        self.etat = etat

class Carte_tresor(ElementQueteAnnexe):
    """
    Classe permettant de créer l'élément de jeu carte au trésor
    
    :param position: Position de la carte au trésor
    :type position: Point
    
    :param orientation: Orientation de la carte au trésor (toujours égale à -Pi/2)
    :type orientation: float
    
    :param ennemi: Est à True si la carte au trésor appartient à l'ennemi, à False sinon
    :type ennemi: boolean
    
    :param etat: Etat de la carte au trésor (True si dévoilée, False sinon)
    :type etat: boolean
    """
    def __init__(self, position, ennemi, etat = False):
        """
        :TODO: Gerer l'assignation de la variable 'enemy' en fonction de la position du poussoir et de notre couleur
        Je ne pense pas que ça soit important (Anthony V.)
        """
        #log.logger.info("Création d'un objet Carte_tresor en cours...\n")
        ElementQueteAnnexe.__init__(self, position, -math.pi/2, ennemi, False)
        
        
    def setEtatOK(self, etat = TRUE):
        """
        Fonction permettant d'actualiser l'état de la carte au trésor
        
        :param etat: [OPTIONEL] Mettre False si la carte se recouvre (cas rare et potentiellement indétectable)
        :type etat: boolean
        
        """
        self.etat = etat
        

class Zone:
    """
    Classe permettant de créer l'élément de jeu Zone
    
    :param nomZone: Nom de la zone (La casse n'a pas d'importance)
    :type nomZone: string 'CALE'|'CALEPROTEGEE'|'BUREAUCAPITAINE'|'AIREDEJEU'
    
    :param angleSG: Position de l'angle supérieur gauche de la zone
    :type angleSG: Point
    
    :param angleID: Position de l'angle inférieur droit de la zone
    :type angleID: Point
    
    :param ennemi: Est à True si le totem appartient à l'ennemi, à False sinon
    :type ennemi: boolean
    
    :param protectionCale: Est à True si le cadre protégeant le dessous de la cale est fermé, à False sinon.
    :type protectionCale: boolean
    
    :TODO: Prévoir une adaptation pour la zone trapézoïdale (bas de la cale)
    """
    def __init__(self, nomZone, angleSG, angleID, ennemi):
        nomZone = nomZone.upper()
        #log.logger.info("Création d'un objet Zone en cours...\n")
        if nomZone not in ["CALE", "CALEPROTEGEE", "BUREAUCAPITAINE", "AIREDEJEU"] :
            #log.logger.warning("Attention : nom de la Zone non valide\n")
            print("Attention")
            pass
        
        self.nomZone = nomZone
        self.angleSG = angleSG
        self.angleID = angleID
        self.enemy = enemy
        
        if nomZone == "CALEPROTEGEE" :
            #log.logger.info("Création d'un objet CALEPROTEGEE en cours\n")
            self.nomZone = nomZone
            self.protectionCale = True