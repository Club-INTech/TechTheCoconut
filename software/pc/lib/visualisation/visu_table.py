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
		'marron':[168,86,6],
		'vert':[147,239,8],
		'rouge':[234,57,59],
		'violet':[138,48,225],
		'gris':[213,215,217],
		
		#:deprecated: retro-compatibilité
		'poussoirTrue':[234,57,59],	# Eux  ("Rouge")
		'poussoirFalse':[138,48,225],	# Nous ("Violet")
		'carteTresorTrue':[234,57,59],
		'carteTresorFalse':[138,48,225],
		'CALE':[127,127,127],
		'CALEPROTEGEE':[127,127,127],
		'BUREAUCAPITAINE':[127,127,127],
		'AIREDEJEU':[127,127,127]}
    srcImageTable = os.path.join(os.path.dirname(__file__), "../../donnees/images/table_3000_2000_vierge.png")
    displayMap = True
	      
    #Nota: Utiliser des Setters/Getters pour les propriétés suivantes ?
    scale = 0.3
    caption = "Visualisation Table - INTech 2012"
    fps = 1
    
    def __init__(self,debug=True):
	"""
	Constructeur
	
	:param debug: Affiche les paramètres de dessin des différents objets
	:type debug: boolean
	"""
	self.debug = debug
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
			  
	if self.debug:
	    print "Lingot"
	
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
	
	if self.debug:
	    print "Disque (r="+str(r)+";x="+str(x)+";y="+str(y)+") " \
		  "abs[x="+str(x)+"/"+str(self.tailleTablePx[0])+" | y="+str(y)+"/"+str(self.tailleTablePx[1])+"] " \
		  "rel[x="+str(math.trunc( Visu_table.scale * disque.position.x ))+" | y="+str(math.trunc( Visu_table.scale * disque.position.y ))+"]"
			  
    def drawTotem(self, totem):
	"""
	Dessine le totem sur l'écran
	
	:param totem: Le totem à dessiner
	:type totem: Totem
	"""
	x = self.tailleTablePx[0]/2 + math.trunc(self.scale*totem.position.x) - math.trunc( (self.scale*totem.largeur)/2 )
	y = self.tailleTablePx[1] - math.trunc(self.scale*totem.position.y) - math.trunc( (self.scale*totem.longueur)/2 )
	largeur = math.trunc( Visu_table.scale * totem.largeur )
	longueur = math.trunc( Visu_table.scale * totem.longueur )
	
	pygame.draw.rect(pygame.display.get_surface(),
			 Visu_table.couleur['marron'],
			 pygame.Rect(x, y, largeur, longueur))
			  
	if self.debug:
	    print "Totem(la="+str(largeur)+";lo="+str(longueur)+") abs[x="+str(x)+"/"+str(self.tailleTablePx[0])+" | " +  "y="+str(y)+"/"+str(self.tailleTablePx[1])+"] "+ \
		  "rel[x="+str(math.trunc( Visu_table.scale * totem.position.x ))+" | y="+str(math.trunc( Visu_table.scale * totem.position.y ))+"]"
			  
    def drawPalmier(self, palmier):
	"""
	Dessine le palmier sur l'écran
	
	:param palmier: Le palmier à dessiner
	:type palmier: Palmier
	"""
	x = self.tailleTablePx[0]/2 + math.trunc(self.scale*palmier.position.x)
	y = self.tailleTablePx[1] - math.trunc(self.scale*palmier.position.y)
	r = math.trunc( self.scale*palmier.rayon)
	
	pygame.draw.circle( pygame.display.get_surface(), Visu_table.couleur["vert"], (x,y), r)
	
	if self.debug:
	    print "Palmier (r="+str(r)+";x="+str(x)+";y="+str(y)+")" \
		  " abs[x="+str(x)+"/"+str(self.tailleTablePx[0])+" | y="+str(y)+"/"+str(self.tailleTablePx[1])+"]"+ \
		  " rel[x="+str(math.trunc( Visu_table.scale * palmier.position.x ))+" | y="+str(math.trunc( Visu_table.scale * palmier.position.y ))+"]"
    
    def drawPoussoir(self, poussoir):
	"""
	Dessine le poussoir sur l'écran
	
	:param poussoir: Le poussoir à dessiner
	:type poussoir: Poussoir
	"""
	
	x = self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale * poussoir.position.x )
	y = self.tailleTablePx[1] - math.trunc( Visu_table.scale * poussoir.position.y )
	couleur = (poussoir.ennemi  and 'rouge') or 'violet'
	
	if poussoir.etat: #si enfoncé
	    l = math.trunc( 12 * Visu_table.scale )
	else:
	    l = math.trunc( 27 * Visu_table.scale )
	
	# if poussoir.etat: appartient à l'ennemi
	pygame.draw.rect( pygame.display.get_surface(),
			  Visu_table.couleur[couleur],
			  pygame.Rect(x, y, 7, l))
	
	if self.debug:
	    print "Poussoir (etat="+str(poussoir.etat)+";ennemi="+str(poussoir.ennemi)+") "  \
		  "abs[x="+str(x)+"/"+str(self.tailleTablePx[0])+" | " +  "y="+str(y)+"/"+str(self.tailleTablePx[1])+"] "+ \
		  "rel[x="+str(math.trunc( Visu_table.scale * poussoir.position.x ))+" | y="+str(math.trunc( Visu_table.scale * poussoir.position.y ))+"]"
			  
    def drawCarteTresor(self, carteTresor):
	"""
	Dessine la carte au trésor  sur l'écran
	
	:param carteTresor: La carte au trésor à dessiner
	:type carteTresor: CarteAuTresor
	"""
	hauteur = math.trunc( 42 * Visu_table.scale )
	largeur = math.trunc( 192 * Visu_table.scale )
	
	x = self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale*carteTresor.position.x) - math.trunc( largeur/2 )
	y = self.tailleTablePx[1] - math.trunc( Visu_table.scale*carteTresor.position.y) - hauteur
	couleur = (carteTresor.ennemi  and 'rouge') or 'violet'
	
	if not carteTresor.etat:
	    pygame.draw.rect(pygame.display.get_surface(),
			     Visu_table.couleur[couleur],
			     pygame.Rect(x, y, largeur, hauteur) )
			  
	if self.debug:
	    if carteTresor.etat:
		print "CarteAuTresor(ennemi="+str(carteTresor.ennemi)+"): not displayed "
	    else:
		print "CarteAuTresor(ennemi="+str(carteTresor.ennemi)+"): " \
		  " abs[x="+str(x)+"/"+str(self.tailleTablePx[0])+" | y="+str(y)+"/"+str(self.tailleTablePx[1])+"]"+ \
		  " rel[x="+str(math.trunc( Visu_table.scale * carteTresor.position.x ))+" | y="+str(math.trunc( Visu_table.scale * carteTresor.position.y ))+"]"
			  
    def drawZone(self, zone):
	"""
	Dessine la zone sur l'écran
	:Note: Ajouter une info sur l'etat de la protection de la cale ?
	:TODO; Refaire la fonction de manière à rendre visible les informations utiles
	
	:param zone: La zone à dessiner
	:type zone: Zone
	"""
	sg = (self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale*zone.angleSG.x), self.tailleTablePx[1] - math.trunc( Visu_table.scale*zone.angleSG.y))
	ig = (self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale*zone.angleIG.x), self.tailleTablePx[1] - math.trunc( Visu_table.scale*zone.angleIG.y))
	id = (self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale*zone.angleID.x), self.tailleTablePx[1] - math.trunc( Visu_table.scale*zone.angleID.y))
	sd = (self.tailleTablePx[0]/2 + math.trunc( Visu_table.scale*zone.angleSD.x), self.tailleTablePx[1] - math.trunc( Visu_table.scale*zone.angleSD.y))
	
	if zone.nomZone == 'CALEPROTEGEE':
	    couleur = Visu_table.couleur['gris']
	elif zone.nomZone == 'CALE':
	    couleur = Visu_table.couleur['marron']
	elif zone.nomZone == 'BUREAUCAPITAINE':
	    couleur = Visu_table.couleur['violet']
	else: #AIREDEJEU
	    pass

	
	pygame.draw.polygon( pygame.display.get_surface(), couleur, [sg, ig, id, sd])
			  
	if self.debug:
	    print "Zone (nom="+zone.nomZone+";ennemi="+str(zone.ennemi)+"): " \
		  "abs[sg="+str(sg)+";ig="+str(ig)+";id="+str(id)+";sd=;"+str(sd)+"]"

    def majTable(self):
	print "majTable"
	#"Efface" les précédents items
	if Visu_table.displayMap:
	    self.screen.blit(self.imageTable, [0,0])
        
        for zone in self.carte.zones:
	    self.drawZone(zone)
            
        for palmier in self.carte.palmiers:
	    self.drawPalmier(palmier)
            
        for carteTresor in self.carte.cartesAuxTresor:
	    self.drawCarteTresor(carteTresor)
	
	for poussoir in self.carte.poussoirs:
	    self.drawPoussoir(poussoir)
            
        for totem in self.carte.totems:
	    self.drawTotem(totem)
	
	for lingot in self.carte.lingots:
	    self.drawLingot(lingot)
	
        for disque in self.carte.disques:
	    self.drawDisque(disque)
	    
        
	
	#Nota: Dessin des réglettes inutiles puisqu'elles ne devraient à priori pas bouger. 
	    
	"""
	    Position du robot 
	    @QuiDeDroit Ajout d'un attribut dans Carte() pour le representer ou utilisation de sa classe Robot() directement ?
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
