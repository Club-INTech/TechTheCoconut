import sys, os
import instance
import __builtin__

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    #instances pour une simulation
    if __builtin__.simulation:
        print "INSTANCES DE SIMULATION"
        __builtin__.instance = instance.Instance()
    else:
        __builtin__.instance = instance.Instance()
except:
    __builtin__.instance = instance.Instance()

__builtin__.instance.instanciation()

modules = []
modules.append("outils_math")
modules.append("simul_uc")
modules.append("visualisation")
modules.append("actionneur")
modules.append("asservissement")
#modules.append("balise")
modules.append("capteur")
modules.append("carte")
modules.append("conf")
modules.append("elements_jeu")
modules.append("log")
modules.append("outils_math")
#modules.append("peripherique")
#modules.append("detection_peripheriques")
modules.append("robot")
modules.append("serie")
modules.append("serie_simple")
modules.append("strategie")
modules.append("recherche_chemin")
modules.append("recherche_chemin.astar")
modules.append("recherche_chemin.thetastar")
#modules.append("tests_mecha")
modules.append("timer")
modules.append("jumper")
modules.append("script")
modules.append('lolilol')

for module in modules:
    try:
        exec("import lib."+module)
    except:
        print >> sys.stderr, "Erreur lors de l'importation du module lib."+module