"""
Permet la gestion des fichiers

rappel :
fichier fen selon convention international avec acronyme traduit en francais AUSSI majuscule = blanc et minuscule = noir
echiqiuer en [y][x]
1 haut donc ...
-1 bas donc ...
"""
from typing import List
from constante import NB_CASE_ECHEC, SETUP_BASE, TRADUCTION_OBJET_FILE
from gestion_pieces import Pieces



def positionner_pieces(disposition_pieces:List, pieces:Pieces) -> None:
    """
    Crée une liste de piece aux coordonnées donnée par une liste
    contenant le type de la piece et ses coordonnées
    """
    for y, ligne in enumerate(disposition_pieces):
        avance = 0
        if y == len(disposition_pieces)-1:
            break
        for x, case in enumerate(ligne):
            if case in ('\\', '\n'):
                break
            if case == '0':
                avance+=1
            else:
                pieces.creer_piece(case, x+avance, y)

def ajouter_historique(pieces:Pieces, historique:int):
    """
    Ajoute les coups dans l'historique de la partie
    et remets la partie dans l'etat de la
    sauvegarde.
    """
    for coup in historique.split("\n")[1:-1]:
        pieces.historique.append(coup)
    for _ in range(len(pieces.historique)):
        pieces.jouer_coup()

def lecture_fichier_fen(nom_fichier, haut:int) -> Pieces:
    """
    Créé l'objet pieces à partie d'un fichier .FEN respectant les
    conventions d'écriture FEN sauf pour le roi
    roi : k pour blanc et K pour noir
    #question fonction dans pieces ou dans le fichier gestion_fichier ?
    """
    with open(nom_fichier, encoding="utf-8") as file:
        with open(SETUP_BASE, encoding="utf-8") as base:
            pieces = Pieces(haut, [])
            disposition_pieces = file.read().split("\\")
            base = base.read().split("\\")
            positionner_pieces(base, pieces)
            pieces.rois = { 1 : pieces.rechercher_piece_nom("roi", 1), -1 : pieces.rechercher_piece_nom("roi", -1)}
            ajouter_historique(pieces, disposition_pieces[-1])
            return pieces



#A faire : Lecture d'un match traduction de la forme algébrique a l'echiquier


def sauvegarder_partie(pieces:Pieces) -> None:
    """
    Pour linstant crée juste le positionnement de la fin de partie
    A terme : sauvegarde les coups aussi
    """
    print("choisissez le nom du fichier : ")
    nom_fichier = input()
    with open(f"partie/{nom_fichier}.fen", "w+", encoding="utf-8") as file:
        for y in range(NB_CASE_ECHEC):
            for x in range(NB_CASE_ECHEC):
                piece = pieces.rechercher_piece((x, y))
                if piece:
                    file.write(TRADUCTION_OBJET_FILE[(piece.name, piece.couleur)])
                else:
                    file.write("0")
            file.write("\\")
        file.write("\n")
        for coup in pieces.historique:
            file.write(coup)
            file.write("\n")



if __name__ == "__main__":
    import pylint.lint
    #disable des no member car probleme avec pygame
    pylint_opts = ['--disable=no-member', '--disable=line-too-long', __file__]
    pylint.lint.Run(pylint_opts)
