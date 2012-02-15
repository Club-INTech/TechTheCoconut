# -*- coding: utf-8 -*-

import pygame, time, sys, os, math, threading, lib.log

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

log = lib.log.Log()

class Visu_serie(threading.Thread):
  
    #Définition des constantes de la classe
	      
    tailleEcran = [640,480]
    caption = "Visualisation Liaison Série - INTech 2012"
    fps = 1
    
    """
    Classe permettant de visualiser les messages passant par la liaison série utilisant un thread (ie non bloquante)\n
    Pour la démarrer utiliser la méthode start()\n
    Pour l'arrêter utiliser la méthode stop()\n
    """    
    def __init__(self,nom):
	"""
	Constructeur
	
	:param nom: Défini le nom du Thread
	:type nom: string
	"""
	self.nom = nom
	
        pygame.init()
  
	# Crée "l'écran" et définie la résolution
	self.screen = pygame.display.set_mode(Visu_serie.tailleEcran)
	pygame.display.set_caption(Visu_serie.caption)
	
	# Gère la vitesse de mise à jour de l'écran
	self.clock=pygame.time.Clock()
	self.clock.tick(Visu_serie.fps)
	
	# pick a font you have and set its size
	myfont = pygame.font.SysFont("Comic Sans MS", 30)
	# apply it to text on a label
	label = myfont.render("Python and Pygame are Fun!", 1, [138,48,225])
	# put the label object on the screen at point x=100, y=100
	self.screen.blit(label, (100, 100))
	
	try:
	    threading.Thread.__init__(self, name=nom)
	    log.logger.info("Création de la visualisation de la liaison Série (thread nommé "+nom+")...")
	except:
	    self.stop()

    def quit(self):
	log.logger.info("Fermeture du thread "+self.nom+" en cours...")
	self.Terminated = True
	pygame.quit ()  
	self._Thread__stop()

    def run(self):
	self.Terminated=False
	
	while self.Terminated is False:
	    #On parcours la liste des évènements depuis le dernier appel à get()
	    for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    self.Terminated=True
	    
	    #Evite la surchage du processeur
	    time.sleep(1/self.fps)
	    pygame.display.update()
	
	
	self.quit()
