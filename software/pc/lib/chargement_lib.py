import sys, os
import instance
import __builtin__

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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
modules.append("detection_peripheriques")
modules.append("elements_jeu")
modules.append("log")
modules.append("outils_math")
modules.append("peripherique")
modules.append("robot")
modules.append("serie")
modules.append("serie_simple")
modules.append("strategie")
modules.append("recherche_chemin")
modules.append("recherche_chemin.astar")
modules.append("recherche_chemin.thetastar")
modules.append("tests_mecha")
modules.append("timer")
modules.append("jumper")
modules.append("script")

__builtin__.instance = instance.Instance()
__builtin__.instance.instanciation()

for module in modules:
    try:
        exec("import lib."+module)
    except:
        print >> sys.stderr, "Erreur lors de l'importation du module lib."+module