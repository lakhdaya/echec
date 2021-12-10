"""
Controleur du mouvement de la piece et
du choix de lutulisateur du mouvement de la
piece
"""


import pygame as py
from constante import NB_CASE_ECHEC, DIRECTIONS
from gestion_pieces import addition_tuple, Piece, Pieces
from graph import Echiquier






def control_manager(pieces:Pieces, echec:Echiquier):
    """"
    regarde si l'utilisateur maintient le click
    """
    for event in py.event.get():
        if event.type == py.MOUSEBUTTONDOWN:
            pos_depart = echec.pixel_vers_case(py.mouse.get_pos())
            piece = pieces.rechercher_piece(pos_depart)
            return piece
    return None

def pieces_handler(pieces:Pieces,  piece:Piece, pos_depart:tuple, pos_arrive:tuple):
    """
    Gere le mouvement d'un piece dans lechiquier.
    """
    if piece:
        if piece.can_mouv_here(pos_arrive) and pieces.tour_joueur == piece.couleur:
            pieces.changement_tour()
            if piece.name == "roi":
                pieces.rock_tour(pos_depart, pos_arrive)
            elif piece.name == "pion":
                piece.pion_passant = piece.is_pion_passant(pos_depart, pos_arrive)
                piece.promotion(pieces, pos_arrive)
                if pos_arrive[0]-pos_depart[0] and not pieces.rechercher_piece(pos_arrive):
                    pieces.supprimer_piece(pieces.rechercher_piece((pos_arrive[0], pos_depart[1])))
            
            piece_mange = piece.deplacer_piece(pieces, pos_arrive)
            if pieces.en_echec(piece_attaque = pieces.rois[pieces.tour_joueur*-1]):
                if piece_mange:
                    pieces.liste_pieces.append(piece_mange)
                piece.move(pos_depart)
                pieces.actualiser_trajectoires()
                pieces.changement_tour(-1)
            else:
                pieces.enregistrer_trajectoire(piece, pos_depart, pos_arrive, piece_mange)
        else:
            piece.move(pos_depart)


if __name__ == "__main__":
    #disable des no member car probleme avec pygame
    import pylint.lint
    pylint_opts = ['--disable=trailing-whitespace', '--disable=no-member', '--disable=line-too-long', __file__]
    pylint.lint.Run(pylint_opts)
    