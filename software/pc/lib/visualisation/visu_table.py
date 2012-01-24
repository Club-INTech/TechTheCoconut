# -*- coding: utf-8 -*-
import pygame, time, sys, os
from lib.carte import Carte

#:TODO: Import et utilisation des logs

class Visu_table:
    """
    Classe permettant de visualiser la table de jeu avec les zones, les éléments de jeu, les robots, ...
    """
    
    #Définition des constantes de la classe
    couleur = { 'NOIR':[0,0,0], 
	      'BLANC':[255,255,255],
	      'lingot':[0,255,0],
	      'totem':[255,0,0],
	      'palmier':[0,0,255] }
    #Nota: Utiliser des Setters/Getters pour les propriétés suivantes ?
    tailleTablePx = [600,400]
    caption = "Visualisation Table - INTech 2012"
    srcImageTable = os.path.join(os.path.dirname(__file__), "../../donnees/images/table_3000_2000.png")
    fps = 25
    
    def __init__(self):
	
        pygame.init()
  
	# Crée "l'écran" et définie la résolution
	self.screen = pygame.display.set_mode(Visu_table.tailleTablePx)
	
	pygame.display.set_caption(Visu_table.caption)

	#charge l'image en mémoire et ajuste la dimension
	imageTable = pygame.image.load(Visu_table.srcImageTable).convert()
	self.imageTable = pygame.transform.scale(imageTable, Visu_table.tailleTablePx )
	
	# Gère la vitesse de mise à jour de l'écran
	self.clock=pygame.time.Clock()

	# Limite le rafraichissement
	self.clock.tick(Visu_table.fps)
	
	self.carte = Carte()
	
    def drawLingot(self, lingot):
	"""
	Dessine le lingot sur l'écran
	
	:param lingot: Le lingot à dessiner
	:type lingot: Lingot
	"""
	obj = pygame.Rect(lingot.position.x, lingot.position.y, lingot.largeur, lingot.longueur)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['lingot'],
			  obj)
	
    def drawDisque(self, disque):
	"""
	Dessine le disque sur l'écran
	
	:param disque: Le disque à dessiner
	:type disque: Disque
	"""
	obj = pygame.Rect(disque.position.x, disque.position.y, disque.rayon, disque.rayon)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur[disque.couleur],
			  obj)
			  
    def drawTotem(self, totem):
	"""
	Dessine le totem sur l'écran
	
	:param totem: Le totem à dessiner
	:type totem: Totem
	"""
	obj = pygame.Rect(totem.position.x, totem.position.y, totem.largeur, totem.longueur)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['totem'],
			  obj)
			  
    def drawPalmier(self, palmier):
	"""
	Dessine le palmier sur l'écran
	
	:param palmier: Le palmier à dessiner
	:type palmier: Palmier
	"""
	obj = pygame.Rect(palmier.position.x, palmier.position.y, palmier.rayon, palmier.rayon)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['palmier'],
			  obj)
    
    def drawPoussoir(self, poussoir):
	"""
	Dessine le poussoir sur l'écran
	
	:param poussoir: Le poussoir à dessiner
	:type poussoir: Poussoir
	"""
	obj = pygame.Rect(poussoir.position.x, poussoir.position.y, 10, 10)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['poussoir'+poussoir.etat],
			  obj)
			  
    def drawCarteTresor(self, carteTresor):
	"""
	Dessine la carte au trésor  sur l'écran
	
	:param carteTresor: La carte au trésor à dessiner
	:type carteTresor: CarteAuTresor
	"""
	obj = pygame.Rect(carteTresor.position.x, carteTresor.position.y, 20, 30)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['carteTresor'+carteTresor.etat],
			  obj)
			  
    def drawZone(self, zone):
	"""
	Dessine la zone sur l'écran
	
	:param zone: La zone à dessiner
	:type zone: Zone
	"""
	
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur[zone.couleur],
			  [(zone.angleSG.x,zone.angleSG.y), (zone.angleIG.x,zone.angleIG.y), (zone.angleID.x,zone.angleID.y), (zone.angleSD.x,zone.angleSD.y)],
			  obj)

    def majTable(self):
	#"Efface" les précédents items
        self.screen.blit(self.imageTable, [0,0])
        
        for lingot in self.carte.lingots:
	    self.drawLingot(lingot)
	
        for disque in self.carte.disques:
	    self.drawDisque(disque)
	    
        for totem in self.carte.totems:
	    self.drawTotem(totem)
	    
        for poussoir in self.carte.poussoirs:
	    self.drawPoussoir(poussoir)
	    
        for carteTresor in self.carte.cartesAuxTresor:
	    self.drawCarteTresor(carteTresor)
	    
        for palmier in self.carte.palmiers:
	    self.drawPalmier(palmier)
        
        for zone in self.carte.zones:
	    self.drawZone(zone)
	
	#Nota: Dessin des réglettes inutiles puisqu'elles ne devraient à priori pas bouger. 
	    
	"""
	    Position du robot 
	    Ajout d'un attribut dans Carte() pour le representer ou utilisation de sa classe Robot() directement ?
	"""
	
	pygame.display.flip()

    def mainLoop(self):
	done=False
	
	while done==False:
	    #On parcours la liste des évènements depuis le dernier appel à get()
	    for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    done=True
	    
	    #Evite la surchage du processeur
	    time.sleep(1/self.fps)
	    
	    self.majTable()

    def quit(self):
	pygame.quit ()  
