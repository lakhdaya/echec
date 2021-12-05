from constante import *
from gestion_pieces import addition_tuple, piece, pieces
from graph import echiquier
from GUI import GUI
import pygame
import gestion_fichier





def control_manager(pieces:pieces, echec:echiquier, gui:GUI):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_depart = echec.pixel_vers_case(pygame.mouse.get_pos())
            piece = pieces.rechercher_piece(pos_depart)
            return piece


def pieces_handler(pieces:pieces,  piece:piece, pos_depart:tuple, pos_arrive:tuple, rois:dict):
    if piece:
        if piece.can_mouv_here(pos_arrive) and pieces.tour_joueur == piece.couleur:
            pieces.changement_tour()
            if piece.name == "roi":
                if piece.is_rocking(pos_depart, pos_arrive):
                    if pos_arrive[0] == 2:
                        tour = pieces.rechercher_piece((0, pos_arrive[1]))
                        tour.mouv(addition_tuple(pos_arrive, DIRECTIONS["E"]))
                    else:
                        tour = pieces.rechercher_piece((NB_CASE_ECHEC-1, pos_arrive[1]))
                        tour.mouv(addition_tuple(pos_arrive, DIRECTIONS["W"]))
            piece_mange = piece.deplacer_piece(pieces, pos_arrive)
            if piece.name == "pion":
                piece.promotion(pos_arrive) 
            if len(pieces.en_echec(rois[pieces.get_tour()*-1].get_pos(), piece.couleur)):
                if piece_mange:
                    pieces.ajouter_piece(piece_mange)
                piece.mouv(pos_depart)
                piece.actualiser_trajectoire(pieces)
                pieces.changement_tour(-1)
            else:
                pieces.enregistrer_trajectoire(piece, pos_depart, pos_arrive, piece_mange)
        else:
            piece.mouv(pos_depart)
