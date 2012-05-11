# -*- coding: utf-8 -*-

import pygame, time, sys, os, math, threading, lib.log,random
import outils_math.point as point
import __builtin__

# Ajout de ../.. au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

log = lib.log.Log(__name__)

#:TODO: Import et utilisation des logs

class Visu_table(threading.Thread):
    """
    Classe permettant de visualiser la table de jeu avec les zones, les éléments de jeu, les robots utilisant un thread (ie non bloquante)\n
    Pour la démarrer utiliser la méthode start()\n
    Pour l'arrêter utiliser la méthode stop()\n
    Une seule instance simultanée de cette classe est possible (conflit de thread sinon)
    """
    
    #Définition des constantes de la classe
    couleur = { 'NOIR':[0,0,0], 
		'BLANC':[255,255,255],
		'orange':[255,127,0],
		'marron':[168,86,6],
		'vert':[147,239,8],
		'rouge':[234,57,59],
		'violet':[138,48,225],
		'gris':[213,215,217],
		'bleuMarine':[0,0,127]}
    srcImageTable = os.path.join(os.path.dirname(__file__), "../donnees/images/table_3000_2000.png")
    fps = 2
    scale = 0.3
    
    def __init__(self,instances):
        """
        Constructeur

        :param debug: Affiche les paramètres de dessin des différents objets \n
        Pour la retro-compatibilité, normalement non utilisé. Utilise log.logger.debug à la place
        :type debug: boolean
        """
        

        self.nomThread = "visu_table"
        self.tailleTablePx = [math.trunc(3000*self.scale), math.trunc(2000*self.scale)]
        pygame.init()

        # Crée "l'écran" et définie la résolution
        self.screen = pygame.display.set_mode(self.tailleTablePx)

        pygame.display.set_caption( "Visualisation Table - INTech 2012")

        #charge l'image en mémoire et ajuste la dimension
        imageTable = pygame.image.load(Visu_table.srcImageTable).convert()
        self.imageTable = pygame.transform.scale(imageTable, self.tailleTablePx )

        #self.robotInstance = __builtin__.instance.robotInstance
        
        
        # Gère la vitesse de mise à jour de l'écran
        self.clock=pygame.time.Clock()

        # Limite le rafraichissement
        self.clock.tick(Visu_table.fps)

        self.instances = instances
        #self.chemin = []
        try:
            threading.Thread.__init__(self, name=self.nomThread, target=self.start)
            log.logger.info("Création de la visualisation de la table (thread nommé "+self.nomThread+")...")
        except:
            self.quit()
        
        self.infos = { 'pathfinding' : []
                        ,  'positionBaliseKalman' : [point.Point(0,0)]
                        ,  'positionBaliseBrut' : [point.Point(0,0)]
                        , 'vitesseRobotAdverse' : point.Point(0,0) }

    def ajouter_pos(self, nomListe, pos):
        positions = self.infos[nomListe]
        positions.append(pos*self.scale)
        if(len(positions) > 1):
            positions.pop(0)
    
    def modifierVitesseAdversaire(self,vitesse):
        self.infos['vitesseRobotAdverse'] = vitesse*self.scale
       
    def refresh(self):
        self.screen.blit(self.imageTable, [0,0])
        balise = self.instances.baliseInstance;
        ajouter_pos(balise.getPosition())
        modifierVitesseAdversaire(balise.getVitesse())
        positions = self.infos['positionRobotAdverse']
        vitesse = self.infos['vitesseRobotAdverse']
        #pygame.draw.lines( pygame.display.get_surface(), Visu_table.couleur['NOIR'], False,[[10,10]]);
        for pos in positions:
            pygame.draw.circle(pygame.display.get_surface(), self.couleur['rouge'],pos.to_list(),3)
        current = positions[len(positions)-1]
        futur = current + vitesse
        #print current
        #print futur
        pygame.draw.line(pygame.display.get_surface(), Visu_table.couleur['NOIR'], current.to_list(), futur.to_list(),3);
        position_robot = self.instances.asserInstance.getPosition()
        pygame.draw.rect(self.screen, Visu_table.couleur['BLANC'], (position_robot.x,position_robot.y,0.1*self.scale*constantes["Coconut"]["largeur"],0.1*self.scale*constantes["Coconut"]["longueur"]), 2)
        #pygame.draw.lines( pygame.display.get_surface(), Visu_table.couleur['bleuMarine'], False, []);
        pygame.display.flip()
        
    def quit(self):
        log.logger.info("Fermeture du thread "+self.nomThread+" en cours...")
        self.Terminated = True
        pygame.quit ()  
        self._Thread__stop()
        
    def run(self):
        self.Terminated=False	
        while self.Terminated is False:
            #On parcours la liste des évènements depuis le dernier appel à get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            
            self.refresh()
            #for i in range(10):
            #self.ajouter_pos_adversaire([int(random.uniform(0, 3000)),int(random.uniform(0, 2000))])
            #self.modifierVitesseAdversaire([int(random.uniform(-100, 100)),int(random.uniform(-350, 350))])
            #Evite la surchage du processeur
            time.sleep(1/float(self.fps))
            
            #self.majTable()