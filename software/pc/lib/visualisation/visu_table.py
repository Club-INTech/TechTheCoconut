# -*- coding: utf-8 -*-
import pygame, time, sys, os, math
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
	      'palmier':[147,239,8],
	      'poussoirTrue':[234,57,59], # Eux
	      'poussoirFalse':[138,48,225],# Nous
	      'carteTresorTrue':[127,127,127],
	      'carteTresorFalse':[127,127,127],
	      'CALE':[127,127,127],
	      'CALEPROTEGEE':[127,127,127],
	      'BUREAUCAPITAINE':[127,127,127],
	      'AIREDEJEU':[127,127,127]}
    srcImageTable = os.path.join(os.path.dirname(__file__), "../../donnees/images/table_3000_2000.png")
    debug = True
    displayMap = False
	      
    #Nota: Utiliser des Setters/Getters pour les propriétés suivantes ?
    scale = 0.3
    caption = "Visualisation Table - INTech 2012"
    fps = 1
    
    def __init__(self):
	
	self.tailleTablePx = [math.trunc(3000*self.scale), math.trunc(2000*self.scale)]
	
        pygame.init()
  
	# Crée "l'écran" et définie la résolution
	self.screen = pygame.display.set_mode(self.tailleTablePx)
	
	pygame.display.set_caption(Visu_table.caption)

	#charge l'image en mémoire et ajuste la dimension
	imageTable = pygame.image.load(Visu_table.srcImageTable).convert()
	self.imageTable = pygame.transform.scale(imageTable, self.tailleTablePx )
	
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
			  
	if Visu_table.debug:
	    print "draw Lingot"
	
    def drawDisque(self, disque):
	"""
	Dessine le disque sur l'écran
	
	:param disque: Le disque à dessiner
	:type disque: Disque
	"""
	x = self.tailleTablePx[0]/2 + math.trunc(self.scale*disque.position.x)
	y = self.tailleTablePx[1] - math.trunc(self.scale*disque.position.y)
	r = math.trunc( self.scale*disque.rayon)
	
	pygame.draw.circle( pygame.display.get_surface(), Visu_table.couleur[disque.couleur], (x,y), r)
	
	if Visu_table.debug:
	    print "draw Disque (r="+str(r)+";x="+str(x)+";y="+str(y)+")"
	    print "Table[x="+str(self.tailleTablePx[0])+";y="+str(self.tailleTablePx[1])+"]"
	    print "x = "+str(self.tailleTablePx[0]/2)+" + "+str(math.trunc(self.scale*disque.position.x))+" = "+str(x)+" (detail: "+str(self.scale)+"*"+str(disque.position.x)+")"
	    print "y = "+str(self.tailleTablePx[1])+" - "+str(math.trunc(self.scale*disque.position.y))+" = "+str(y)+" (detail: "+str(self.scale)+"*"+str(disque.position.y)+")"
			  
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
			  
	if Visu_table.debug:
	    print "draw Totem"
			  
    def drawPalmier(self, palmier):
	"""
	Dessine le palmier sur l'écran
	
	:param palmier: Le palmier à dessiner
	:type palmier: Palmier
	"""
	x = self.tailleTablePx[0]/2 + math.trunc(self.scale*palmier.position.x)
	y = self.tailleTablePx[1] - math.trunc(self.scale*palmier.position.y)
	r = math.trunc( self.scale*palmier.rayon)
	
	pygame.draw.circle( pygame.display.get_surface(), Visu_table.couleur["palmier"], (x,y), r)
	
	if Visu_table.debug:
	    print "draw Palmier (r="+str(r)+";x="+str(x)+";y="+str(y)+")"
	    print "Table[x="+str(self.tailleTablePx[0])+";y="+str(self.tailleTablePx[1])+"]"
	    print "x = "+str(self.tailleTablePx[0]/2)+" + "+str(math.trunc(self.scale*palmier.position.x))+" = "+str(x)+" (detail: "+str(self.scale)+"*"+str(palmier.position.x)+")"
	    print "y = "+str(self.tailleTablePx[1])+" - "+str(math.trunc(self.scale*palmier.position.y))+" = "+str(y)+" (detail: "+str(self.scale)+"*"+str(palmier.position.y)+")"
    
    def drawPoussoir(self, poussoir):
	"""
	Dessine le poussoir sur l'écran
	
	:param poussoir: Le poussoir à dessiner
	:type poussoir: Poussoir
	"""
	
	x = self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale * poussoir.position.x )
	y = self.tailleTablePx[1] - math.trunc( Visu_table.scale * poussoir.position.y )
	
	if poussoir.etat: #si enfoncé
	    l = 4
	else:
	    l = 9
	
	# if poussoir.etat: appartient à l'ennemi
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['poussoir'+str(poussoir.ennemi)],
			  pygame.Rect(x, y, 7, l))
	
	if Visu_table.debug:
	    print "draw Poussoir (etat="+str(poussoir.etat)+")" \
		  " abs[x="+str(x)+"/"+str(self.tailleTablePx[0])+" | y="+str(y)+"/"+str(self.tailleTablePx[1])+"]"+ \
		  " rel[x="+str(math.trunc( Visu_table.scale * poussoir.position.x ))+" | y="+str(math.trunc( Visu_table.scale * poussoir.position.y ))+"]"
			  
    def drawCarteTresor(self, carteTresor):
	"""
	Dessine la carte au trésor  sur l'écran
	
	:param carteTresor: La carte au trésor à dessiner
	:type carteTresor: CarteAuTresor
	"""
	obj = pygame.Rect(carteTresor.position.x, carteTresor.position.y, 20, 30)
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur['carteTresor'+str(carteTresor.etat)],
			  obj)
			  
	if Visu_table.debug:
	    print "draw Tresor"
			  
    def drawZone(self, zone):
	"""
	Dessine la zone sur l'écran
	
	:param zone: La zone à dessiner
	:type zone: Zone
	"""
	
	pygame.draw.polygon( pygame.display.get_surface(),
			  Visu_table.couleur[zone.nomZone],
			  [(zone.angleSG.x,zone.angleSG.y), (zone.angleIG.x,zone.angleIG.y), (zone.angleID.x,zone.angleID.y), (zone.angleSD.x,zone.angleSD.y)])
			  
	if Visu_table.debug:
	    print "draw Zone"

    def majTable(self):
	print "majTable"
	#"Efface" les précédents items
	if Visu_table.displayMap:
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
