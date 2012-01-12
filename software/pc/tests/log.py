# -*- coding: utf-8 -*-

import os
import sys
import shutil
import datetime
import logging
import re

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.log

class TestLog(lib.log.Log):
	"""
	Classe permettant de tester la gestion des logs
	"""

	def	test_creer_dossier_inexistant(self):
		"""
		Teste la création d'un dossier inexistant initiallement
		"""
		assert self.creer_dossier("dossier_test")
		assert os.access("dossier_test", os.F_OK)
		os.rmdir("dossier_test")
		
	def test_creer_dossier_existant(self):
		"""
		Teste la création d'un dossier existant initiallement
		"""
		os.makedirs("dossier_test")
		assert not self.creer_dossier("dossier_test")
		assert os.access("dossier_test", os.F_OK)
		os.rmdir("dossier_test")
	
	def test_revision_disponible_dossier_vide(self):
		"""
		Teste la récupération de la prochaine révision d'un fichier de log pour un dossier vide
		"""
		os.makedirs("fake1")
		assert (0 == self.revision_disponible("fake1", str(datetime.date.today())))
		shutil.rmtree("fake1")

	def test_revision_disponible_dossier_non_vide(self):
		"""
		Teste la récupération de la prochaine révision d'un fichier de log pour un dossier non vide
		"""
		# Pour dossier non vide
		os.makedirs("fake1/"+str(datetime.date.today()))
		# touch
		with file("fake1/"+str(datetime.date.today())+"/0.log", 'a'):
			pass
		assert (1 == self.revision_disponible("fake1", str(datetime.date.today())))
		shutil.rmtree("fake1")
	
	def test_ecrire_entete(self):
		"""
		Teste l'écriture de l'entête au niveau INFO
		"""
		logging.basicConfig(filename='example.log',level=logging.DEBUG)
		self.logger = logging
		self.ecrire_entete()
		f = file('example.log', 'r')
		assert "INFO:root:Début des logs\n" == f.read()
		os.remove('example.log')

	def test_initialisation_scenario1(self):
		"""
		Teste un premier scénario de chargement l'initialisation complète du système de log
		(Tests de stdout non implémentés)
		"""
		os.makedirs("logs_test")
		log1 = lib.log.Log(True, "DEBUG", "%(asctime)s:%(name)s:%(levelname)s:%(threadName)s:l%(lineno)d:%(message)s", True, "INFO", "%(asctime)s:%(name)s:%(levelname)s:%(message)s", "logs_test")
		log1.logger.debug("Debug1")
		log1.logger.info("Info1")
		log1.logger.warning("Warning1")
		log2 = lib.log.Log(True, "DEBUG", "%(asctime)s:%(name)s:%(levelname)s:%(threadName)s:l%(lineno)d:%(message)s", True, "INFO", "%(asctime)s:%(name)s:%(levelname)s:%(message)s", "logs_test")
		log2.logger.debug("Debug2")
		log2.logger.info("Info2")
		log2.logger.critical("Critical2")
		
		assert os.path.exists("logs_test/"+str(datetime.date.today())+"/0.log")
		f = file("logs_test/"+str(datetime.date.today())+"/0.log", "r")
		lignes = f.readlines()
		
		regex_heure = "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}"
		regex_name = ":([a-z]+(\.)*)+"
		regex_severity = ":(DEBUG|INFO|WARNING|ERROR|CRITICAL)"
		
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:D\xc3\xa9but des logs\n", lignes[0])
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:Debug1\n", lignes[1])
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:Info1\n", lignes[2])
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:Warning1\n", lignes[3])
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:Debug2\n", lignes[4])
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:Info2\n", lignes[5])
		assert re.match(regex_heure+regex_name+regex_severity+":[a-zA-Z]+:l[0-9]+:Critical2\n", lignes[6])
		
		shutil.rmtree("logs_test")
		del lib.log.Log.initialise
		
	def test_initialisation_scenario2(self):
		"""
		Teste un deuxième scénario de chargement l'initialisation complète du système de log
		(Tests de stdout non implémentés)
		"""
		os.makedirs("logs_test2")
		log1 = lib.log.Log(True, "WARNING", "%(asctime)s:%(name)s:%(levelname)s:%(message)s", False, dossier="logs_test2")
		log1.logger.info("Info1")
		log1.logger.warning("Warning1")
		log1.logger.error("Error1")
		
		assert os.path.exists("logs_test2/"+str(datetime.date.today())+"/0.log")
		f = file("logs_test2/"+str(datetime.date.today())+"/0.log", "r")
		lignes = f.readlines()
		
		regex_heure = "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}"
		regex_name = ":([a-z]+(\.)*)+"
		regex_severity = ":(DEBUG|INFO|WARNING|ERROR|CRITICAL)"
		
		assert re.match(regex_heure+regex_name+regex_severity+":Warning1\n", lignes[0])
		assert re.match(regex_heure+regex_name+regex_severity+":Error1\n", lignes[1])
		
		shutil.rmtree("logs_test2")
		del lib.log.Log.initialise
		
	def test_initialisation_scenario3(self):
		"""
		Teste un troisième scénario de chargement l'initialisation complète du système de log
		(Tests de stdout non implémentés)
		"""
		log1 = lib.log.Log(logs=False, stderr=False, dossier="logs_test3")
		
		assert not os.path.exists("logs_test3")