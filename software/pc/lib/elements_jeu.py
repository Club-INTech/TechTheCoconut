# -*- coding: utf-8 -*-

class ElementARamener :
    """
    :param position: position de l'objet à ramener
    :type position: Point
    
    :param orientation: orientation de l'objet à ramener
    :type orientation: float
    
    :param 
    """
    
    def __init__(self, position, orientation) :
        self.position = position
        self.orientation = orientation
        self.type = "SURLETERRAIN"        # Cette variable peut être égale à SURLETERRAIN, PROTEGEE
        
        
class Disque:
    
    
    """
    Classe de créer l'élément de jeu disque
    """
    def __init__(self, position):
      """
      :param position: Position du disque
      :type position: Point
      """
      self.position = position # position est de type Point
      self.rayon = 5 #TODO changer la valeur numérique

class Lingot:
    """
    Classe de créer l'élément de jeu lingot
    """
    def __init__(self, position, orientation):
      """
      :param position: Position du disque
      :type position: Point
      """
        self.position = position
        self.orientation = orientation  # Angle que fait le lingot avec le bas de la table, en radians
        
class Totem:
    """
    Classe de créer l'élément de jeu totem
    """
    def __init__(self, position):
      """
      :param position: Position du disque
      :type position: Point
      """
        self.position = position
        self.couleur = "ROUGE" # cet attribut correspond au joueur à qui appartient le totem
        #			 TODO gérer l'assignation de cet attibut
        self.longueur = 5 #TODO changer la valeur numérique
        self.largeur = self.longueur #cette variable est inutile mais au moins on peut l'utiliser
        
        self.hauteur = 5 #TODO changer la valeur numérique

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
      
class Point :
  """
  Classe pour la position des éléments  
  """
  def __int__(self, positionX, positionY):
    """
    :param positionX: abscisse du point, en mm
    :type positionY: float
    
    :param positionY: ordonnée du point, en mm
    :type positionY: float
    """
    self.x = positionX
    self.y = positionY
    
  def distance(self, point2) :
    from math import sqrt
    return sqrt((point2.x - self.x)*(point2.x - self.x) + (point2.y - self.y)*(point2.y - self.y))