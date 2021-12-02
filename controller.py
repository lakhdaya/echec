from constante import *
from gestion_pieces import piece, pieces
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
        if piece.can_mouv_here(pos_arrive) and not len(pieces.en_echec(rois[pieces.tour_joueur].pos(), piece.couleur)) and pieces.tour_joueur == piece.couleur:
            piece_mange = piece.deplacer_piece(pieces, pos_arrive)
            pieces.changement_tour()
            pieces.enregistrer_trajectoire(piece, pos_depart, pos_arrive, piece_mange)
        else:
            piece.mouv(pos_depart)
