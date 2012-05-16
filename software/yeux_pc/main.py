# -*- coding: utf-8 -*-

"""
Editeur graphique qui permet de sortir des 
matrices C++ pour la matrice à led des yeux
sous la forme :
byte sprite[4]={B00111100,B00111100,B00111100,B00111100};

7x4 leds

TODO :
* Améliorer les arguments de dessiner_quadrillage
"""

import pygame, sys
from pygame.locals import *
import bisect

CASE_COTE = 40
CASES_LARGEUR = 14
CASES_HAUTEUR = 7

COULEUR_ZONES = (255, 255, 255)
COULEUR_LIGNES = (0, 0, 0)
COULEUR_CASE = (0, 212, 45)

ZONES = (
    (0, 0, CASE_COTE*CASES_LARGEUR, CASE_COTE*CASES_HAUTEUR),
    (CASE_COTE*(CASES_LARGEUR+1), 0, CASE_COTE*CASES_LARGEUR, CASE_COTE*CASES_HAUTEUR)
)

MATRICE = [{},{}]

def dessiner_zone(numero):
    """
    Dessine les deux zones blanches
    """
    pygame.draw.rect(
        DISPLAYSURF,
        COULEUR_ZONES,
        ZONES[numero]
    )

def dessiner_quadrillage(x_ini, y_ini, x_fin, y_fin):
    """
    Dessine le quadrillage d'une zone
    """
    for y in range(y_ini, y_fin+1, CASE_COTE):
        pygame.draw.line(
            DISPLAYSURF,
            COULEUR_LIGNES,
            (x_ini, y),
            (x_fin, y),
            1
        )
    for x in range(x_ini, x_fin+1, CASE_COTE):
        pygame.draw.line(
            DISPLAYSURF,
            COULEUR_LIGNES,
            (x, y_ini),
            (x, y_fin),
            1
        )

#def case_coords(x_index, y_index, zone):
    #"""
    #Donne les coordonnées d'une case en fonction de son index dans la zone voulue
    #"""
    
    
    
def dessiner_remplir_case(x_click, y_click, couleur = COULEUR_CASE):
    """
    Dessine dans la bonne case selon la position en (x,y) de la souris
    """
    zone = 0
    for (x_ini, y_ini, zone_largeur, zone_hauteur) in ZONES:
        x_fin = x_ini+zone_largeur
        y_fin = y_ini+zone_hauteur
        x_range = range(x_ini, x_fin+1, CASE_COTE)
        y_range = range(y_ini, y_fin+1, CASE_COTE)
        x_bisect = bisect.bisect_left(x_range, x_click)
        y_bisect = bisect.bisect_left(y_range, y_click)
        if (x_bisect and x_bisect <= CASES_LARGEUR and y_bisect and y_bisect <= CASES_HAUTEUR):
            x = x_range[x_bisect-1]
            y = y_range[y_bisect-1]
            if couleur == COULEUR_ZONES:
                MATRICE[zone][(x_bisect, y_bisect)] = 0
            else:
                MATRICE[zone][(x_bisect, y_bisect)] = 1
            pygame.draw.rect(
                DISPLAYSURF,
                couleur,
                (x, y, CASE_COTE, CASE_COTE)
            )
        zone += 1
    
def dessiner_vider_case(x_click, y_click):
    """
    Efface la bonne case selon la position en (x,y) de la souris
    """
    dessiner_remplir_case(x_click, y_click, COULEUR_ZONES)
    
pygame.init()
DISPLAYSURF = pygame.display.set_mode((CASE_COTE*(2*CASES_LARGEUR+1), ((CASE_COTE*CASES_HAUTEUR)+100)))
    
dessiner_zone(0)
dessiner_zone(1)
dessiner_quadrillage(0, 0, CASE_COTE*CASES_LARGEUR, CASE_COTE*CASES_HAUTEUR)
dessiner_quadrillage(CASE_COTE*(CASES_LARGEUR+1), 0, CASE_COTE*(2*CASES_LARGEUR+1), CASE_COTE*CASES_HAUTEUR)

# Create a font
font = pygame.font.Font(None, 17)

# Render the text
text = font.render('Powered by Python and PyGame', True, (255,
255, 255), (159, 182, 205))

# Create a rectangle
textRect = text.get_rect()

# Center the rectangle
textRect.centerx = DISPLAYSURF.get_rect().centerx
textRect.centery = DISPLAYSURF.get_rect().centery

# Blit the text
DISPLAYSURF.blit(text, textRect)



pygame.display.set_caption('Editeur yeux')
ETAT_SOURIS = 'lache'
SIDE = 1 # NOTE 1 pour gauche, 3 pour droite
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION: # Souris en mouvement
            sourisx, sourisy = event.pos
        elif event.type == MOUSEBUTTONUP and event.button == SIDE: # Click lâché
            sourisx, sourisy = event.pos
            ETAT_SOURIS = 'lache'
        elif event.type == MOUSEBUTTONDOWN: # Click enfoncé
            sourisx, sourisy = event.pos
            SIDE = event.button
            ETAT_SOURIS = 'enfonce'
        elif event.type == MOUSEBUTTONUP:
            ETAT_SOURIS = 'lache'
        if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN: # On dessine
            if ETAT_SOURIS == 'enfonce' and SIDE == 1:
                dessiner_remplir_case(sourisx, sourisy)
            if ETAT_SOURIS == 'enfonce' and SIDE == 3:
                dessiner_vider_case(sourisx, sourisy)
            dessiner_quadrillage(0, 0, CASE_COTE*CASES_LARGEUR, CASE_COTE*CASES_HAUTEUR)
            dessiner_quadrillage(CASE_COTE*(CASES_LARGEUR+1), 0, CASE_COTE*(2*CASES_LARGEUR+1), CASE_COTE*CASES_HAUTEUR)
        pygame.display.update()