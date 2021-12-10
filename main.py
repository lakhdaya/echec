""""
Module principale a executer pour lancer le jeu d'echecs

Choix des positions blancs : 1 = haut, -1 = bas

Source : https://fr.wikipedia.org/wiki/Pi%C3%A8ce_(%C3%A9checs)
wikipedia a été utilisé pour les règles, les conventions d'écriture FEN et l'utilisation des jpeg des pieces.
"""


import pygame as py
import graph
import gestion_fichier
import gui as gi
from constante import FICHIER
from controller import pieces_handler
## A IMPLEMENT : gestion des couleurs CAD OPTION POUR CHANGER LA COULEUR DU HAUT ET BAS




def temps():
    """
    fonction retorunant le nombre de seconde et de minutes ecoulés
    à partir du debut du lancement du programmes
    """
    minute, seconde = py.time.get_ticks()//(1000*60), (py.time.get_ticks()//1000)%60
    return minute, seconde

def main():
    """
    fonction main a executer pour lancer le jeu
    dans le if en dessous
    """
    haut = -1
    jouer = True
    #création echiquier
    pieces = gestion_fichier.lecture_fichier_fen(FICHIER, haut)
    echec = graph.Echiquier()

    #creatoin du gui
    boutons = [gi.Bouton(nom, attribut["Position"], attribut["Taille"], attribut["Fonction"], pieces) for nom, attribut in gi.BOUTONS.items()]
    gui = gi.Gui(boutons)

    #recherche du roi noir et blanc
    pieces.actualiser_trajectoires()
    echec.dessiner_gui(gui)
    while jouer:
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                pos_depart = echec.pixel_vers_case(py.mouse.get_pos())
                piece = pieces.rechercher_piece(pos_depart)
                pos_arrive = echec.mouse_tracker(pieces, gui, piece)
                pieces_handler(pieces, piece, pos_depart, pos_arrive)
                gui.click_sur_bouton(py.mouse.get_pos(), pieces)
            if event.type == py.QUIT or pieces.en_mat() or piece.en_pat():
                jouer = False
        echec.refresh(pieces, gui)


if __name__ == "__main__":
    print("choix du type : ")
    #choix = input()
    choix = "jeux"
    if choix == "test qualite":
        import pylint.lint
        #disable des no member car probleme avec pygame
        pylint_opts = ['--disable=no-member', '--disable=line-too-long', __file__]
        pylint.lint.Run(pylint_opts)
    elif choix == "jeux":
        main()
    py.quit()
