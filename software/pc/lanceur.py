# -*- coding: utf-8 -*-

import lib.conf
import __builtin__

# Chargement de la couleur du robot
first = True
while first or couleur not in ['', 'r', 'v']:
    first = False
    couleur = raw_input('Couleur de notre robot rouge ou violet ([v], r) : ')
    if couleur == '' :
        couleur = 'v'

# Chargement du profil de configuration
first = True
while first or not profil.importation:
    first = False
    conf = raw_input('Indiquer la configuration a importer (prod, [develop], developSimulUc) : \n')

    # tronque la string conf pour éviter les bugs à l'import
    conf = conf.split('.')
    for i in conf:
        if i == 'prod':
            conf = 'prod'
        elif i == 'develop':
            conf = 'develop'
        elif i == 'developSimulUc':
            conf = 'developSimulUc'
        elif i == '':
            conf = 'develop'
    
    profil = lib.conf.Conf(conf)


# Chargement des constantes en variable globale
exec('import profils.'+conf+'.constantes')
exec('__builtin__.constantes = profils.'+conf+'.constantes.constantes')

__builtin__.constantes['couleur'] = couleur

# Initialisation des logs
import lib.log
log = lib.log.Log(__name__)

log.logger.info('Profil de configuration chargé : ' + conf)

log.logger.info('Injection des données de la carte')
exec('import profils.'+conf+'.injection.elements_jeu')

if conf == 'develop':
    exec('import profils.'+conf+'.injection.robot')
else:
    exec('import profils.'+conf+'.injection')

import lib.peripherique
#import lib.detection_peripheriques

# Association manuelle des périphériques
#for p in constantes['Serie']['peripheriques']:
    #p_obj = lib.peripherique.Peripherique(p)
    #if p_obj.associer():
        #lib.peripherique.liste.append(p_obj)
# Fin association manuelle des périphériques

# Association automatique des périphériques

#lib.detection_peripheriques.Detection_peripheriques()

import lib.chargement_lib

# WARNING variable globale pour instancier le robot
import lib.robot
__builtin__.robotInstance = lib.robot.Robot()

first = True
erreur = False
while first or erreur:
    mode = raw_input('Indiquer le mode de lancement (autonome, [console], visualisation_table, e (etalonnage_constantes), h[omologation]), m[atch] : \n')
    first = False
    #try:
    if mode == '' or mode == 'console':
        mode = 'console'
        
        # Importation de l'instant où on lance le robot (avant l'arrivée du bouton poussoir) (par Thibaut)
        import time
        __builtin__.constantes["t0"] = time.time()
        
    if mode == 'h':
        mode = "homologation"
    if mode == 'e':
        mode = 'etalonnage_constantes'
    if mode == "m" :
        mode = "match"
    log.logger.info("Chargement du fichier de lancement " + mode)
    exec('import bin.'+ mode)
    if mode == "visualisation_table":
        first = True
        
    #except:
        #log.logger.warning("Le mode '" + mode + "' n'a pas pu etre charge")
        #erreur = True