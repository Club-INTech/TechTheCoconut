import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

modules = []
modules.append("actions_in")
modules.append("actions_out")
modules.append("outils_math")
modules.append("recherche_chemin")
modules.append("simul_uc")
modules.append("visualisation")
modules.append("actionneur")
modules.append("asservissement")
modules.append("capteur")
modules.append("carte")
modules.append("conf")
modules.append("decision")
modules.append("elements_jeu")
modules.append("evenement")
modules.append("evitement")
modules.append("jeu")
modules.append("log")
modules.append("peripherique")
modules.append("robot")
modules.append("serie")
modules.append("strategie")
modules.append("recherche_chemin.astar")
modules.append("recherche_chemin.graph")
modules.append("recherche_chemin.graph_tool_test")
modules.append("recherche_chemin.thetastar")

for module in modules:
    try:
        exec("import lib."+module)
    except:
        print >> sys.stderr, "Erreur lors de l'importation du module lib."+module