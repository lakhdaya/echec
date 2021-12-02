from typing import overload
import pygame
from constante import *
from gestion_pieces import pieces, piece
"""
Fichier permettant la gestion des pieces au niveau frontend
"""



class echiquier(): #ecran du jeu
    """
    objet permettant la gestion graphique de tout l'echiquier
    """
    def __init__(self, NB_CASE_X:int = 8, NB_CASE_Y:int = 8, position_blanc:int = 1) -> None:
        pygame.display.init()
        self.name = "echiqiuer"
        self.width = NB_CASE_X #taille en case
        self.height = NB_CASE_Y #taille en case
        self.taille_case = TAILLE_CASE
        self.widthp = self.taille_case*self.width
        self.heightp = self.taille_case*self.height
        self.fpms = 30
        self.fenetre = pygame.display.set_mode((self.width*self.taille_case+100, self.height*self.taille_case+100))
        self.dessiner_echiquier()

    def case_vers_pixel(self, pos:tuple) -> tuple:
        return pos[0]*self.taille_case, pos[1]*self.taille_case

    def pixel_vers_case(self, pos:tuple) -> tuple:
        """
        Conversion de coordonnées en pixel de l'ecran en case du jeu
        """
        return pos[0]//self.taille_case, pos[1]//self.taille_case

    def dessiner_echiquier(self) -> None:
        for y in range(NB_CASE_ECHEC+1):
            for x in range(NB_CASE_ECHEC):
                pygame.draw.rect(self.fenetre, TYPE_CASE[(x+y)%2], pygame.Rect(x*self.taille_case, y%(NB_CASE_ECHEC)*self.taille_case, self.taille_case, self.taille_case), 0)


    def dessiner_lignes(self) -> None:
        """
        Créer les lignes delimitant le plateau de jeu
        """
        pygame.draw.line(self.fenetre, COULEUR_LIGNES, pygame.Vector2(0, self.heightp), pygame.Vector2(self.widthp, self.heightp), 1)
        pygame.draw.line(self.fenetre, COULEUR_LIGNES, pygame.Vector2(self.widthp, 0), pygame.Vector2(self.widthp, self.heightp), 1)
    
    def dessiner_piece(self, piece:piece, pixel = 0) -> None:
        """
        Dessine une piece selon le nom, 
        la position donnée en pixel, et la couleur
        
        """
        canvas = pygame.transform.scale(pygame.image.load("pieces/"+PATH_PIECE[(piece.name, piece.couleur)]), (TAILLE_CASE-PADDING_PIECE//2, TAILLE_CASE-PADDING_PIECE//2))
        if pixel:
            self.fenetre.blit(canvas, piece.pos())
        else:
            x, y = self.case_vers_pixel(piece.pos())
            self.fenetre.blit(canvas, (x+PADDING_PIECE//4,y+PADDING_PIECE//4))
    
    def dessiner_trajectoires(self, piece:piece) -> None:
        for traj in piece.trajectoire:
            x, y = self.case_vers_pixel(traj)
            pygame.draw.rect(self.fenetre, COULEUR_TRAJECTOIRE, pygame.Rect(x, y, self.taille_case, self.taille_case))

    def dessiner_pieces(self, pieces, exception:piece = None) -> None:
        """
        Dessine toute les pieces de l'echiquier
        """
        for piece in pieces.liste_pieces:
            if piece != exception:
                self.dessiner_piece(piece)

    def dessiner_gui(self, gui):
        for bouton in gui.boutons:
            pygame.draw.rect(self.fenetre, COULEUR_BOUTON, pygame.Rect(bouton.x, bouton.y, bouton.width, bouton.height), 0)


    

    def dessiner_ecran(self, gui) -> None:
        self.fenetre.fill((255, 255, 255))
        self.dessiner_lignes()    
        self.dessiner_echiquier()
        self.dessiner_gui(gui)

    def refresh(self, pieces, gui, exception:piece = None) -> None:
        """
        Actualise la fenetre du jeu
        """
        pygame.time.wait(self.fpms)
        self.dessiner_ecran(gui)
        self.dessiner_pieces(pieces, exception)
        if exception:
            self.dessiner_trajectoires(exception)
            self.dessiner_piece(exception, 1)
        pygame.time.wait(self.fpms)
        pygame.display.flip()
        
    def centrer(self, pos):
        return pos[0]-self.taille_case//2, pos[1]-self.taille_case//2

    def mouse_tracker(self, event, pieces, gui, piece):
        if piece:
            piece.mouv(self.centrer(pygame.mouse.get_pos()))
            while(event.type!=pygame.MOUSEBUTTONUP):
                ev = pygame.event.get()
                for event in ev:
                    piece.mouv(self.centrer(pygame.mouse.get_pos()))
                self.refresh(pieces, gui, piece)
        return self.pixel_vers_case(pygame.mouse.get_pos())

    def choix_promotion(self, pos):
        pass