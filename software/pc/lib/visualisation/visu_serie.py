# -*- coding: utf-8 -*-

# WARNING Non fini

import time, sys, os, threading, Tkinter, lib.log, datetime

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

log = lib.log.Log(__name__)

class Visu_serie(threading.Thread):
    def __init__(self, nom="visu_serie"):
        
        self.nom= nom
	try:
	    threading.Thread.__init__(self, name=nom)
	    log.logger.info("Création de la visualisation de la liaison Série (thread nommé "+nom+")...")
	except:
	    self.quit()
 
    def run(self, parent=None):

	self.window=GUIVisu_serie(parent)
	self.window.mainloop()

    def stop(self):
	log.logger.info("Fermeture du thread "+self.nom+" en cours...")
        self.window.destroy()

class GUIVisu_serie(Tkinter.Tk):
    
    """
    Classe permettant de visualiser les messages passant par la liaison série\n
    Le démarrage ce fait lors de l'instanciation\n
    Pour l'arrêter utiliser la méthode stop()\n
    """    
    def __init__(self, parent = None):
	"""
	Constructeur
	
	:param parent: Défini le parent de la fenetre
	:type nom: Tkinter.Tk
	"""
	
	Tkinter.Tk.__init__(self, parent)
	self.parent = parent
	self.initialize()
	
    def initialize(self):
	
	""" Options divers """
	
	self.grid_columnconfigure(0, weight=1)
	self.resizable( False, True)
	self.update()
	self.geometry("640x480")
	self.title("Visualisation Liaison Série - INTech 2012")
	self.grid()
	
	""" Variables texte """
	
	self.serieLogs = Tkinter.StringVar()
	date = datetime.datetime.today()
	self.serieLogs.set( date.strftime("Lancement de la visualisation à %H:%M:%S le %d/%m/%Y\n"))
	
	"""
	self.inputTxt = Tkinter.StringVar()
	self.inputTxt.set("Entrer ici votre commande")
	"""
	
	""" Widgets supérieur """
	
	self.lbText = Tkinter.Label(self, textvariable=self.serieLogs, fg="white", bg="black", anchor="w", justify="left", wraplength=640)
	self.lbText.grid(column=0, columnspan=3, row=0, sticky="EW")
	
	
	""" Widgets inferieur"""
	"""
	self.btnAdd = Tkinter.Button(self, text="Add")
	self.btnAdd.grid(  	column=2, row=1, sticky="W")
	
	self.txtEnter = Tkinter.Entry(self, textvariable=self.inputTxt)
	self.txtEnter.grid(	column=0, columnspan=2, row=1, sticky="EW")
	"""
	
    def addText(self, text):
	self.serieLogs.set(self.serieLogs.get() +"\n"+ text)