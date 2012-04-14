# -*- coding: utf-8 -*-

import os
import sys
import time
import threading

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.serie

class TestSerie():
    """
    Classe permettant de tester la liaison serie
    """

    def test_init(self):
        """
        Teste l'initialisation et l'arrêt de la liaison
        """
        s = lib.serie.Serie("/dev/ttyUSB10", "ttyUSB10", 9600, 1)
        assert s.active

        s = lib.serie.Serie("/dev/ttyUSB20", "ttyUSB10", 9600, 5)
        assert s.active

        s = lib.serie.Serie("/dev/ttyUSB10", "ttyUSB10", 9600, 1, "PARITY_EVEN")
        assert not s.active
        
        s = lib.serie.Serie("/dev/ttyUSB20", "ttyUSB20", 56521, 3)
        assert not s.active
        
    def test_ecrire(self):
        """
        Teste l'écriture sur une liaison série
        """
        s = lib.serie.Serie("/dev/ttyUSB10", "ttyUSB10", 9600, 1)
        caracteres = s.ecrire("Hello World!")
        assert caracteres == len("Hello World!")+2
    
    def test_lire_ecrire(self):
        """
        Teste la lecture/écriture sur une liaison série
        """
        s1 = lib.serie.Serie("/dev/ttyUSB10", "écriture", 9600, 1)
        s2 = lib.serie.Serie("/dev/ttyUSB20", "lecture", 9600, 1)
        s2.start()
        s1.ecrire("Hello World!")
        # On attend que le message arrive
        time.sleep(2)
        assert "Hello World!" == s2.file_attente.get()
        print s2.file_attente.empty()
        s2.stop()