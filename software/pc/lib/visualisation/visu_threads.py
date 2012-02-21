# -*- coding: utf-8 -*-
import threading

class Visu_threads:
    """
    Classe permettant de visualiser les différents threads utilisés pour aider à les débuguer
    """
    def __init__(self):
        pass
    
    def rechercheThread(nomThread):
	"""
	Recherche un thread par son nom\n
	Retourne le thread si il existe, None sinon
	
	:param nomThread: le nom du thread a rechercher
	:type nomThread: string
	"""
	for t in threading.enumerate():
	    if nomThread == t.getName():
		return t
	return None
	
    rechercheThread = staticmethod(rechercheThread)