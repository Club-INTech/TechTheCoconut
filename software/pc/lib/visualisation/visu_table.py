# -*- coding: utf-8 -*-
import pygame, time, sys, os

#:TODO: Import et utilisation des logs

class Visu_table:
    """
    Classe permettant de visualiser la table de jeu avec les zones, les éléments de jeu, les robots, ...
    """
    
    #Définition des constantes de la classe
    couleur = { 'black':[0,0,0], 
	      'white':[255,255,255],
	      'green':[0,255,0],
	      'red':[255,0,0],
	      'blue':[0,0,255] }
    #Nota: Utiliser des Setters/Getters pour les propriétés suivantes ?
    tailleTablePx = [600,400]
    caption = "Visualisation Table - INTech 2012"
    srcImageTable = os.path.join(os.path.dirname(__file__), "../../donnees/images/table_3000_2000.png")
    fps = 1
    
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
	
    
    def majTable(self):
	#"Efface" les précédents items
        self.screen.blit(self.imageTable, [0,0])
        
        #:TODO: Récupérer les infos des objets et de la carte
        #:TODO: Replacer toutes ces données "sur l'écran"
        
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

#Instanctation de la classe (pour démo)
vTable = Visu_table()
vTable.mainLoop()
vTable.quit()