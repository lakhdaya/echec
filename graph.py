import pygame
from constante import COULEUR_BOUTON, COULEUR_LIGNES, COULEUR_TRAJECTOIRE, NB_CASE_ECHEC, PADDING_PIECE, PADDING_TRAJECTOIRE, PATH_PIECE, TAILLE_CASE, TAILLE_GUI_X, TAILLE_GUI_Y, TYPE_CASE
from gestion_pieces import Piece
"""
Fichier permettant la gestion des pieces au niveau frontend
"""



class Echiquier(): #ecran du jeu
    """
    objet permettant la gestion graphique de tout l'echiquier
    """
    def __init__(self, taille_case=TAILLE_CASE) -> None:
        pygame.display.init()
        self.name = "echiqiuer"
        self.taille_case = taille_case
        self.widthp = self.taille_case*NB_CASE_ECHEC
        self.heightp = self.taille_case*NB_CASE_ECHEC
        self.fpms = 30
        self.fenetre = pygame.display.set_mode((self.widthp+TAILLE_GUI_X, self.heightp+TAILLE_GUI_Y))
        self.dessiner_echiquier()

    def case_vers_pixel(self, get_pos:tuple) -> tuple:
        return get_pos[0]*self.taille_case, get_pos[1]*self.taille_case

    def pixel_vers_case(self, get_pos:tuple) -> tuple:
        """
        Conversion de coordonnées en pixel de l'ecran en case du jeu
        """
        return get_pos[0]//self.taille_case, get_pos[1]//self.taille_case

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
    
    def dessiner_piece(self, piece:Piece, pixel = 0) -> None:
        """
        Dessine une piece selon le nom,
        la get_position donnée en pixel, et la couleur
        
        """
        canvas = pygame.transform.scale(pygame.image.load("pieces/"+PATH_PIECE[(piece.name, piece.couleur)]), (TAILLE_CASE-PADDING_PIECE//2, TAILLE_CASE-PADDING_PIECE//2))
        if pixel:
            self.fenetre.blit(canvas, piece.get_pos())
        else:
            x, y = self.case_vers_pixel(piece.get_pos())
            self.fenetre.blit(canvas, (x+PADDING_PIECE//4,y+PADDING_PIECE//4))

    def dessiner_trajectoires(self, piece:Piece) -> None:
        for traj in piece.trajectoire:
            x, y = self.case_vers_pixel(traj)
            pygame.draw.circle(self.fenetre, COULEUR_TRAJECTOIRE, pygame.Vector2(x+self.taille_case//2, y+self.taille_case//2), self.taille_case//2-PADDING_TRAJECTOIRE)

    def dessiner_pieces(self, pieces, exception:Piece = None) -> None:
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

    def refresh(self, pieces, gui, exception:Piece = None) -> None:
        """
        Actualise la fenetre du jeu
        """
        pygame.time.wait(self.fpms)
        self.dessiner_ecran(gui)
        if exception:
            self.dessiner_trajectoires(exception)
            self.dessiner_piece(exception, 1)
        self.dessiner_pieces(pieces, exception)
        pygame.time.wait(self.fpms)
        pygame.display.flip()

    def centrer(self, get_pos):
        return get_pos[0]-self.taille_case//2, get_pos[1]-self.taille_case//2

    def mouse_tracker(self, pieces, gui, piece):
        if piece:
            print("choix2")
            piece.mouv(self.centrer(pygame.mouse.get_pos()))
            choix = True
            while choix:
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONUP:
                        choix = False
                    piece.mouv(self.centrer(pygame.mouse.get_pos()))
                    self.refresh(pieces, gui, piece)
        return self.pixel_vers_case(pygame.mouse.get_pos())

    def choix_promotion(self, get_pos):
        pass


if __name__ == "__main__":
    import pylint.lint
    #disable des no member car probleme avec pygame
    pylint_opts = ['--disable=no-member', '--disable=line-too-long', __file__]
    pylint.lint.Run(pylint_opts)
