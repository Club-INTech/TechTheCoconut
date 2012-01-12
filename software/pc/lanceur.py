# -*- coding: utf-8 -*-

import os
import lib.log
import lib.conf
import __builtin__

first = True
while first or not profil.importation:
	first = False
	conf = raw_input('Indiquer la configuration a importer (prod, develop, developSimulUc) : \n')
	profil = lib.conf.Conf(conf)

# Chargement des constantes en variable globale
exec('import profils.'+conf+'.constantes')
exec('__builtin__.constantes = profils.'+conf+'.constantes.constantes')

# Initialisatoin des logs
log = lib.log.Log(constantes['Logs']['logs'], constantes['Logs']['logs_level'], constantes['Logs']['logs_format'], constantes['Logs']['stderr'], constantes['Logs']['stderr_level'], constantes['Logs']['stderr_format'], constantes['Logs']['dossier'])

log.logger.info('Profil de configuration chargé : ' + conf)

first = True
erreur = False
while first or erreur:
    mode = raw_input('Indiquer le mode de lancement (autonome, console) : \n')
    first = False
    try:
        log.logger.info("Chargement du fichier de lancement " + mode)
        exec('import bin.'+ mode)
    except:
        log.logger.warning("Le mode '" + mode + "' n'a pas pu etre charge")
        erreur = True