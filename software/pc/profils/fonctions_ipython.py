# -*- coding: utf-8 -*-


import IPython.ipapi

ip = IPython.ipapi.get()


print """
Bienvenue dans la console IPython qu\'elle est belle.
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
    Fonction utilisée pour afficher la liste des commandes INTech
    """

    print """
    Liste des commandes conçues pour INTech :
        - %readme : Affiche le README du dossier software/pc qui décrit l'organisation du code PC.
        - %tuto : Affiche un tutoriel qui permet une première prise en main de Ipython.
    """
    
ip.expose_magic('commandes', commandes)

def aide(self, arg):
    """
    Affiche une aide pour utiliser la fonction
    """
    print arg
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
   4. Quitter le menu
   """
   
    print menu
    
    
    chapitre_deux = """
            
   """
   
    chapitre_trois = """
    """
    flag = True
    while flag:
        choix = raw_input('Indiquer le chapitre a ouvrir avec le chiffre correspondant\n')
        if choix == '1':
            chapitre_un = open("../ipython/tutoriel_un", 'r')
            print chapitre_un.read()
            chapitre_un.close()
            print menu
            
        elif choix == '2':
            chapitre_deux = open('../ipython/tutoriel_deux', 'r')
            print chapitre_deux.read()
            chapitre_deux.close()
            print menu
            
        elif choix == '3':
            chapitre_trois = open('../ipython/tutoriel_trois', 'r')
            print chapitre_trois.read()
            chapitre_trois.close()
            print menu
            
        elif choix == '4':
            flag = False
            
        else:
            print 'Impossible d\'afficher la documentation, veuillez vérifier votre choix'
            print menu
       
                      
        
ip.expose_magic('tuto', tuto)
