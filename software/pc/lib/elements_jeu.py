# -*- coding: utf-8 -*-

class ElementARamener :
    """
    Cette classe contient tous les objets à ramener au camp (i.e. disques et lingots)
    
    :param position: position de l'objet à ramener
    :type position: Point
    
    :param orientation: orientation de l'objet à ramener
    :type orientation: float
    
    :param etat: Type actuel de l'objet : A Ramener, Protégée ou Chez l'adversaire
    :type etat: string (prends les valeurs de "SURLETERRAIN", "PROTEGEE" ou "CHEZLADVERSAIRE"
    :TODO: Est-ce une bonne manière de faire ?
    """
    
    def __init__(self, position, orientation) :
        self.position = position
        self.orientation = orientation
        self.etat = "SURLETERRAIN"        # Cette variable peut être égale à SURLETERRAIN, PROTEGEE, CHEZLADVERSAIRE
        
        
class ElementInfranchissable :
    """
    Cette classe contient tous les objets infranchissables (i.e. totem et règlettes en bois)
    
    :param position: position de l'objet à ramener
    :type position: Point
    
    :param orientation: orientation de l'objet à ramener
    :type orientation: float
    
    """
    
    def __init__(self, position, orientation) :
        self.position = position
        self.orientation = orientation
        
        
class Disque(ElementARamener):
    """
    Classe de créer l'élément de jeu disque
    :param position: Position du disque
    :type position: Point
    
    :param orientation: Orientation du disque
    :type orientation: float
    
    :param rayon: Rayon du disque, en mm
    :type rayon: float
    
    """
    def __init__(self, position):
        ElementARamener.__init__(position, orientation)
        self.rayon = 90 #:TODO: changer la valeur numérique

class Lingot(ElementARamener):
    """
    Classe gérant l'élement de jeu Lingot
    
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
        ElementARamener.__init__(position, orientation)
        self.largeur = 90       #:TODO: changer la valeur numérique
        self.longueur = 160     #:TODO: changer la valeur numérique
        
class Totem:
    """
    Classe gérant l'élement de jeu Totem
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
    
    :param couleur: Zone où le Totem réside ( "ROUGE" ou "VIOLET" )
    :type couleur: string
    """
    def __init__(self, position):
      """
      :param position: Position du disque
      :type position: Point
      """
        self.position = position
        self.couleur = "ROUGE"    #:TODO: Gérer l'assignation de cet élement en fonction de la position
        
        self.longueur = 5 #:TODO: changer la valeur numérique
        self.largeur = self.longueur #cette variable est inutile mais au moins on peut l'utiliser
        
        self.hauteur = 5 #:TODO: changer la valeur numérique

class RegletteEnBois :
    """
    Classe pour les règlettes en bois
    
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
        ElementInfranchissable.__init__(position, orientation)
        self.largeur = 20               #:TODO: changer la valeur numérique
        self.longueur = 200             #:TODO: changer la valeur numérique
        
class Poussoir:
    """
    Classe de créer l'élément de jeu poussoir
    """
    def __init__(self, position):
      """
      :param position: Position du disque
      :type position: Point
      """
        self.position = position

class Carte_tresor:
    """
    Classe de créer l'élément de jeu carte au trésor
    """
    def __init__(self):
        pass

class Zone:
    """
    Classe de créer l'élément de jeu zone
    
    :TODO: Différencier les différents types de zone (départ, cale, pont, ...) avec leurs propriétés
    """
    def __init__(self):
        pass


        
    
    