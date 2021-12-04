from constante import *
from controller import pieces_handler
import graph
import pygame
import gestion_fichier
import GUI


"""
 Source : https://fr.wikipedia.org/wiki/Pi%C3%A8ce_(%C3%A9checs) 
 wikipedia a été utilisé pour les règles, les conventions d'écriture FEN et l'utilisation des jpeg des pieces.
 
"""
## A IMPLEMENT : gestion des couleurs CAD OPTION POUR CHANGER LA COULEUR DU HAUT ET BAS


"""
Fichier main

Choix des positions blancs : 1 = haut, -1 = bas
"""

def temps():
    minute, seconde = pygame.time.get_ticks()//(1000*60), (pygame.time.get_ticks()//1000)%60
    return minute, seconde

def main():
    fin_de_partie = 0
    haut = -1
    limite = 5


    #création echiquier
    pieces = gestion_fichier.lecture_fichier_FEN(FICHIER, haut)
    echec = graph.echiquier()

    #creatoin du gui    
    boutons = [GUI.bouton(nom, attribut["Position"], attribut["Taille"], attribut["Fonction"], pieces) for nom, attribut in GUI.BOUTONS.items()]
    gui = GUI.GUI(boutons)


    #recherche du roi noir et blanc
    rois = { 1 : pieces.rechercher_piece_nom("roi", 1), -1 : pieces.rechercher_piece_nom("roi", -1)}


    pieces.actualiser_trajectoires()
    echec.dessiner_gui(gui)
    while True:
        ev = pygame.event.get()
        for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_depart = echec.pixel_vers_case(pygame.mouse.get_pos())
                    piece = pieces.rechercher_piece(pos_depart)
                    pos_arrive = echec.mouse_tracker(event, pieces, gui, piece)
                    pieces_handler(pieces, piece, pos_depart, pos_arrive, rois)
                    gui.click_sur_bouton(pygame.mouse.get_pos(), pieces)
        echec.refresh(pieces, gui)


if __name__ == "__main__":
    main()