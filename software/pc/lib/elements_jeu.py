# -*- coding: utf-8 -*-



# Classe Point
#import math.point

# Ajout de ../ au path python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Log
import log
#log = log.Log()

"""
Ce fichier crée les classes des différents objets présents sur le terrain, obstacles et zone.

:TODO: Utiliser les constantes définies dans ../profils/prod/constante.py




"""


class ElementARamener :
    """
    Cette classe permet de créer tous les objets à ramener au camp (i.e. Diques et Lingots)
    :note: Les classes Disque et Lingot sont mieux appropriées pour la création d'objets
    
    :param position: position de l'objet à ramener
    :type position: Point
    
    :param orientation: orientation de l'objet à ramener
    :type orientation: float
    
    :param etat: Type actuel de l'objet : A Ramener, Protégée ou Chez l'adversaire
    :type etat: string 'SURLETERRAIN' | 'PROTEGEE' | 'CHEZLADVERSAIRE'
    :TODO: Est-ce une bonne manière de faire ?
    """
    
    def __init__(self, position, orientation) :
        #log.logger.info("Création d'un objet ElementARamener en cours...\n")
        self.position = position
        self.orientation = orientation
        self.etat = "SURLETERRAIN"        # Cette variable peut être égale à SURLETERRAIN, PROTEGEE, CHEZLADVERSAIRE
        
        
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
    :type position: Point   (voir lib/math/point.py)
    
    :param orientation: orientation de l'objet quête annexe
    :type orientation: float
    
    :param etat: Etat de l'objet quête annexe (à False si la quête n'est pas remplie, à True sinon)
    :type etat: boolean
    
    :param enemy: Appartenance de l'objet (à True si il est à nous, à False sinon)
    :type enemy: boolean
    
    """
    
    def __init__(self, position, orientation, etat) :
        self.position = position
        self.orientation = orientation
        self.etat = etat
        self.enemy = enemy
        
        
class Disque(ElementARamener):
    """
    Classe permettant de créer l'élément de jeu disque
    
    :param position: Position du disque
    :type position: Point
    
    :param orientation: Orientation du disque
    :type orientation: float
    
    :param rayon: Rayon du disque, en mm
    :type rayon: float
    
    
    """
    def __init__(self, position, orientation):
        #log.logger.info("Création d'un objet disque en cours...\n")
        ElementARamener.__init__(self, position, orientation)
        self.rayon = 90 #:TODO: changer la valeur numérique
        
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
    
    :param position: Position du disque
    :type position: Point
    
    :param orientation: Orientation du disque
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
    
    :param enemy: [OPTIONEL] Est à 1 si le totem appartient à l'ennemi, à 0 sinon
    :type enemy: boolean
    """
    
    def __init__(self, position, enemy = False):
        #log.logger.info("Création d'un objet Totem en cours...\n")
        ElementInfranchissable.__init__(self, position, 0)
        self.enemy = enemy    #:TODO: Gérer l'assignation de cet élement en fonction de la position et de notre camp
        
        self.longueur = 5 #:TODO: changer la valeur numérique
        self.largeur = self.longueur #cette variable est inutile mais au moins on peut l'utiliser
        
        self.hauteur = 5 #:TODO: changer la valeur numérique
        

class RegletteEnBois(ElementInfranchissable) :
    """
    Classe permettant de créer l'élément de jeu pour les règlettes en bois
    
    :param position: Position de la règlette
    :type position: Point
    
    :param orientation: Orientation de la règlette
    :type orientation: float
    
    :param largeur: Largeur de la règlette, en mm
    :type largeur: float
    
    :param longueur: Longueur de la règlette, en mm
    :type longueur: float
    """
    def __init__(self, position, orientation) :
        #log.logger.info("Création d'un objet RegletteEnBois en cours...\n")
        ElementInfranchissable.__init__(self, position, orientation)
        self.largeur = 20               #:TODO: changer la valeur numérique
        self.longueur = 200             #:TODO: changer la valeur numérique
        
class Poussoir(ElementQueteAnnexe):
    """
    Classe permettant de créer l'élément de jeu poussoir
    
    :param position: Position du poussoir
    :type position: Point
    
    :param orientation: Orientation du poussoir (toujours égale à Pi/2)
    :type orientation: float
    
    :param etat: Etat du poussoir (True si enfoncé, False sinon)
    :type etat: boolean
    
    """
    def __init__(self, position):
        """
        :TODO: Gerer l'assignation de la variable 'enemy' en fonction de la position du poussoir et de notre couleur
        """
        
        #log.logger.info("Création d'un objet Poussoir en cours...\n")
        enemy = True  ##
        ElementQueteAnnexe.__init__(self, position, 3.1415/2, False, enemy)
        
    def setEtatOK(self, etat = True) :
        """
        Fonction permettant d'actualiser l'état du poussoir
        
        :param etat: [OPTIONEL] Mettre False si le bouton se désactive (cas rare)
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
    
    :param etat: Etat de la carte au trésor (True si dévoilée, False sinon)
    :type etat: boolean
    """
    def __init__(self, position):
        """
        :TODO: Gerer l'assignation de la variable 'enemy' en fonction de la position du poussoir et de notre couleur
        """
        #log.logger.info("Création d'un objet Carte_tresor en cours...\n")
        enemy = True
        ElementQueteAnnexe.__init__(self, position, -3.1415/2, False, enemy)

class Zone:
    """
    Classe permettant de créer l'élément de jeu Zone
    
    :param nomZone: Nom de la zone (La casse n'a pas d'importance)
    :type nomZone: string 'CALE'|'CALEPROTEGEE'|'BUREAUCAPITAINE'|'AIREDEJEU'
    
    :param angleSG: Position de l'angle supérieur gauche de la zone
    :type angleSG: Point
    
    :param angleID: Position de l'angle inférieur droit de la zone
    :type angleID: Point
    
    :param enemy: [OPTIONEL] Est à 1 si le totem appartient à l'ennemi, à 0 sinon
    :type enemy: boolean
    
    :param protectionCale: Est à 1 si le cadre protégeant le dessous de la cale est fermé, à 0 sinon.
    :type protectionCale: boolean
    """
    def __init__(self, nomZone, angleSG, angleID, enemy=0):
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
            

    