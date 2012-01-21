# -*- coding: utf-8 -*-

"""
Ce fichier crée les classes des différents objets présents sur le terrain, obstacles et zone.

:TODO: Utiliser les constantes de profil
"""


# Classe Point
#import outils_math.point

# Ajout de ../ au path python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import math
import __builtin__

# Log
import log
log = log.Log()


# Ajout de constantes de develop si on ne passe pas par la console INTech
if not hasattr(__builtin__, "constantes"):
    import profils.develop.constantes
    __builtin__.constantes = profils.develop.constantes.constantes

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
    
    :param hauteur: Hauteur du disque en mm (nul si au sol)
    :type hauteur: int
    
    :param enemy: Est à True si le disque est en terrain ennemi au début du jeu
    :type enemy: bool
    
    
    """
    def __init__(self, position, orientation, couleur, hauteur, enemy):
        #log.logger.info("Création d'un objet disque en cours...\n")
        ElementARamener.__init__(self, position, orientation)
        self.rayon = constantes['Objets_Table']['rayon_disque']
        self.couleur = couleur
        self.hauteur = hauteur
        self.enemy = enemy
        
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
    
    :param hauteur: Hauteur du lingot en mm (au début du jeu)
    :type hauteur: int
    
    :param enemy: Est à True si le lingot est en terrain ennemi au début du jeu
    :type enemy: bool
    
    """
    def __init__(self, position, orientation, hauteur, enemy):
        #log.logger.info("Création d'un objet Lingot en cours...\n")
        ElementARamener.__init__(self, position, orientation)
        self.hauteur = hauteur
        self.enemy = enemy
        self.largeur = constantes['Objets_Table']['largeur_lingot']
        self.longueur = constantes['Objets_Table']['longueur_disque']
    
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
    
    :param rectangle: Rectangle de collision, utilisé principalement pour la recherche de chemin
    :type rectangle: Rectangle (voir lib/outils_math/rectangle.py)
    
    """
    
    def __init__(self, position, ennemi):
        #log.logger.info("Création d'un objet Totem en cours...\n")
        ElementInfranchissable.__init__(self, position, 0)
        self.ennemi = ennemi    #:TODO: Gérer l'assignation de cet élement en fonction de la position et de notre camp
        
        self.longueur = constantes['Objets_Table']['longueur_totem']
        self.largeur = constantes['Objets_Table']['largeur_totem']
        self.hauteur = constantes['Objets_Table']['hauteur_totem']
        
        self.rectangle = Rectangle.rectangle(position.x, position.y, 0, self.longueur, self.largeur)
        
class Palmier(ElementInfranchissable) :
    
    """
    
    :param position: Position du palmier
    :type position: Point
    
    :param rayon: Rayon du palmier (en mm)
    :type rayon: int
    
    :param rectangle: Rectangle de collision, utilisé principalement pour la recherche de chemin
    :type rectangle: Rectangle (voir lib/outils_math/rectangle.py)
    
    """
    
    def __init__(self, position) :
        ElementInfranchissable.__init__(self, position, 0)
        self.rayon = constantes['Objets_Table']['rayon_palmier']
        self.rectangle = Rectangle.rectangle(position.x, position.y, 0, 2*self.rayon, 2*self.rayon)
        

class RegletteEnBois(ElementInfranchissable) :
    """
    Classe permettant de créer l'élément de jeu pour les règlettes en bois
    
    :param position: Centre de la reglette en bois (intersection de ses diagonales)
    :type position: Point    (voir lib/outils_math/point.py)
    
    :param orientation: Angle (radians) que fait la reglette avec le haut de la table, selon la convention définie.
    :type orientation: float
    
    :param longueur: Longueur (en mm) de la reglette 
    :type longueur: int 
    
    :param largeur: Largeur (en mm) de la reglette CONSTANTE (voir profils/prod/constantes.py)
    :type largeur: int
    
    :param rectangle: Rectangle de collision, utilisé principalement pour la recherche de chemin
    :type rectangle: Rectangle (voir lib/outils_math/rectangle.py)
    
    """
    
    def __init__(self, position, orientation, longueur) :
        #log.logger.info("Création d'un objet RegletteEnBois en cours...\n")
        self.position = position
        self.orientation = orientation
        self.longueur = longueur
        self.largeur = constantes["Objets_Table"]['largeur_regletteEnBois']
        
        self.rectangle = Rectangle.rectangle(position.x, position.y, orientation, self.largeur, self.longueur)
    
    
        
        
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
        :TODO: Gerer l'assignation de la variable 'ennemi' en fonction de la position du poussoir et de notre couleur
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

class CarteAuTresor(ElementQueteAnnexe):
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
        :TODO: Gerer l'assignation de la variable 'ennemi' en fonction de la position du poussoir et de notre couleur
        Je ne pense pas que ça soit important (Anthony V.)
        """
        #log.logger.info("Création d'un objet Carte_tresor en cours...\n")
        ElementQueteAnnexe.__init__(self, position, -math.pi/2, ennemi, False)
        
        
    def setEtatOK(self, etat = True):
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
    
    :param angleSD: Position de l'angle sopérieur droit de la zone
    :type angleID: Point
    
    :param angleIG: Position de l'angle inférieur gauche de la zone
    :type angleSG: Point
    
    :param angleID: Position de l'angle inférieur droit de la zone
    :type angleID: Point
    
    :param ennemi: Est à True si le totem appartient à l'ennemi, à False sinon
    :type ennemi: boolean
    
    :param protectionCale: Est à True si le cadre protégeant le dessous de la cale est fermé, à False sinon.
    :type protectionCale: boolean
    
    :TODO: Prévoir une adaptation pour la zone trapézoïdale (bas de la cale)
    """
    def __init__(self, nomZone, angleSG, angleSD, angleIG, angleID, ennemi):
        nomZone = nomZone.upper()
        #log.logger.info("Création d'un objet Zone en cours...\n")
        if nomZone not in ["CALE", "CALEPROTEGEE", "BUREAUCAPITAINE", "AIREDEJEU"] :
            #log.logger.warning("Attention : nom de la Zone non valide\n")
            print("Attention")
        
        self.nomZone = nomZone
        self.angleSG = angleSG
        self.angleSD = angleSD
        self.angleIG = angleIG
        self.angleID = angleID
        self.ennemi = ennemi
        
        if nomZone == "CALEPROTEGEE" :
            #log.logger.info("Création d'un objet CALEPROTEGEE en cours\n")
            self.nomZone = nomZone
            self.protectionCale = True