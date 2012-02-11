# -*- coding: utf-8 -*-
import IPython.ipapi

ip = IPython.ipapi.get()


print """
Bienvenue dans la console IPython.
Pour voir la liste des commandes faites pour INTech, taper %commandes.
Pour voir le tutoriel pour débuter, taper %tuto.
"""

def readme(self, arg):
    """
    Fonction utilisée pour afficher le README du dossier software/pc
    """
    
    text = open('../README', 'r')
    print text.read()
    text.close()

ip.expose_magic('readme', readme)


def commandes(self, arg):
    """
    Fonction utilisée pour afficher la liste des commandes INTech.
    """
    text = open('../ipython/commandes', 'r')
    print text.read()
    text.close()
    
ip.expose_magic('commandes', commandes)

def aide(self, arg):
    """
    Fonction utilisée pour afficher l'aide sur une liste de fonctions.
    """

    fonction = raw_input('Entrer le nom de la fonction qui vous pose problème')
    
    
    
ip.expose_magic('aide', aide)

def tuto(self, arg):
    """
    Fonction utilisée pour afficher un tutoriel qui permet une première prise en main de Ipython.
    """
    
    print """
   Introduction:
    IPython est un interpréteur python qui offre des fonctionnalités poussées comme l'autocomplétion, ou la conservation de l'historiquee même après fermeture et réouverture. 
   """
    menu = """
   Menu:
   1. Fonctions de base et choses à savoir.
   2. Commandes magiques.
   3. Créer ses propres fonctions
   4. Graph Tool (recherche de chemin
   5. Quitter le menu
   """
   
    print menu
    
    flag = True
    while flag:
        choix = raw_input('Indiquer le chapitre a ouvrir avec le chiffre correspondant\n')
        tableau = {'1' : 'tutoriel_un', '2' : 'tutoriel_deux', '3' : 'tutoriel_trois', '4' : 'tutoriel_quatre', '5' : 'exit'}
        
        if tableau[choix]:
            if tableau[choix] == 'exit':
                flag = False
            else:
                chapitre = open('ipython/' + tableau[choix], 'r')
                print chapitre.read()
                print menu
                chapitre.close()
        else:
            print 'Impossible d\'afficher la documentation, veuillez vérifier votre choix'
            print menu
        
                      
        
ip.expose_magic('tuto', tuto)
