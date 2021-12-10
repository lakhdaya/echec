"""
Permet la gestion de toutes les pieces au niveau backend
Gère la partie d'echec et les mouvements de spieces
Detecte aussi la fin de la partie ou pas
"""

from typing import List
from constante import CHEVAL, DIAGONALES, DIRECTIONS, LIGNES, NB_CASE_ECHEC, TRADUCTION_OBJET_FILE


def addition_tuple(tuple_1:tuple(), tuple_2:tuple()) -> tuple:
    """
    Addtionne les valeurs d'un tuple de dim2
    Rq peut se generaliser pour n dimension
    mais inutile ici

    """
    x, y = tuple_1
    x1, y1 = tuple_2
    return (x+x1, y+y1)

def multiplier_tuple(tuple:tuple, val:int) -> tuple:
    """
    Multiple le valeur d'un tuple de dim2
    Rq peut se generaliser pour n dimension
    mais inutile ici
    """
    x, y = tuple
    return (x*val, y*val)

class Piece():
    """
    Caracterise une piece de l'echiquier
    x --> position en x
    y --> position en y
    origin --> piece a deja bouge ou pas
    direction_avec_obstacle --> la direction que peut prendre une piece en
    prenant en compte les autres pieces
    direction_sans_obstacle --> les endroit ou peut aller
    la piece selon la position
    protege --> regarde si un piece la protege
    """
    def __init__(self, x = 0, y = 0, couleur = 1, haut:int = 1):
        self.couleur = couleur #1 pour blanc ,-1 pour noir pour aller de l'avant ou arriere ( noir en bas blanc en haut)# 1 haut donc ...#-1 bas donc ...
        self.x = x
        self.y = y
        self.haut = haut
        self.origin = True
        self.direction_avec_obstacle = []
        self.direction_sans_obstacle = []
        self.trajectoire = []
        self.protege = False

    def move(self, pos):
        """
        Place la piece a l'endroit pos
        """
        self.x, self.y = pos

    def get_pos(self):
        """"
        Get position of object
        """
        return self.x, self.y

    def manger_piece(self, pieces):
        """
        Verifie si la piece est sur une piece si oui elle le "mange"
        """
        pieces_manges = pieces.rechercher_pieces(self.get_pos())
        for piece_mange in pieces_manges:
            if piece_mange.couleur != self.couleur:
                pieces.supprimer_piece(piece_mange)
                return piece_mange
        return None

    def rajout_derniere_case(self, traj, pieces, pos):
        """
        Verifie la derniere case a la fin de la trajectoire si cest la meme couleur
        on considere quelle la protege sinn elle peut la manger
        """
        p = pieces.rechercher_piece(pos)
        if p:
            if p.couleur != self.couleur:
                traj.append(pos)
            else:
                p.protege = True

    def pos_dans_trajectoire(self, pos):
        """
        Regarde si une position est dans la trajectoire de la piece
        """
        return pos in self.trajectoire

    def trajectoire_avec_obstacle(self, pieces, direction):
        """
        Creer la trajectoire selon la direction et verifie si elle est possible
        """
        t = []
        pos = addition_tuple(self.get_pos(), direction)
        while pieces.dedans(pos) and not pieces.rechercher_piece(pos):
            t.append(pos)
            pos = addition_tuple(direction, pos)
        self.rajout_derniere_case(t, pieces, pos)
        return t

    def trajectoire_sans_obstacle(self, pieces, pos):
        """
        Creer la trajectoire selon la position et everifie si cc'est possible
        """
        pos = addition_tuple(self.get_pos(), pos)
        if pieces.dedans(pos):
            p = pieces.rechercher_piece(pos)
            if p:
                if p.couleur == self.couleur:
                    p.protege = True
                    return None
            return pos
        return None

    def actualiser_trajectoire(self, pieces):
        """
        Actualise la trajectoire de la piece
        """
        self.trajectoire = []
        for pos in self.direction_avec_obstacle:
            traj = self.trajectoire_avec_obstacle(pieces, pos)
            if traj:
                self.trajectoire+=traj
        so = [self.trajectoire_sans_obstacle(pieces, pos)
        for pos in self.direction_sans_obstacle if self.trajectoire_sans_obstacle(pieces, pos) is not None]
        if len(so):
            self.trajectoire+=so

    def deplacer_piece(self, pieces, pos):
        """
        Deplace la piece si celle-ci est dans la trajectoire
        """
        if self.pos_dans_trajectoire(pos): # and piece_selec.couleur == tour: #a rajjouter pour le tour par tour
            self.move(pos)
            piece = self.manger_piece(pieces)
            pieces.actualiser_trajectoires()
        return piece

    def can_mouv_here(self, pos_arrive:tuple):
        """
        Verifie si une piece peut bouger
        sur la position
        """
        return pos_arrive in self.trajectoire

"""
Ici les objet permettent de decrire chaque piece des echecs
"""


class Pion(Piece):
    def __init__(self, x:int = 0, y:int = 0, couleur:int = 1, tour:int = 1):
        super().__init__(x, y, couleur, tour)
        self.name = "pion"
        self.origin = True
        self.direction_sans_obstacle = [multiplier_tuple(DIRECTIONS["N"], self.haut*self.couleur), multiplier_tuple((0, 2), self.haut*self.couleur)]
        self.pion_passant = False
    def promotion(self, pieces, pos_arrive):
        """
        Promotion du pion si possible, choix a faire graphiquement ?
        """
        if not pos_arrive[1]%(NB_CASE_ECHEC-1):
            print("choisissez la pieces : ")
            nom_piece = input()
            pieces.supprimer_piece(self)
            pieces.creer_piece(nom_piece, pos_arrive[0], pos_arrive[1])
            return True
        return False

    @staticmethod
    def is_pion_passant(pos_depart, pos_arrive):
        """
        Detecte si lors de son déplacement
        le pion est passant.
        """
        if abs(pos_arrive[1]-pos_depart[1])==2:
            return True
        return False

    def can_eat_pion_passant(self, pieces):
        """
        Verifie si le pion peut manger un pion
        passant a cote de lui.
        """
        trajectoires = [addition_tuple(self.get_pos(), DIRECTIONS["E"]),
        addition_tuple(self.get_pos(), DIRECTIONS["W"])]
        pions_passants = [pieces.rechercher_piece(trajectoire) for trajectoire in
        trajectoires]
        for pion_passant in pions_passants:
            if pion_passant:
                if pion_passant.couleur != self.couleur:
                    if pion_passant.name == "pion" and pion_passant.pion_passant:
                        self.trajectoire.append(addition_tuple(pion_passant.get_pos(),
                        self.direction_sans_obstacle[0]))

    def actualiser_trajectoire(self, pieces):
        """
        Pion special car peut manger les diagonales et ne peut pas manger tout droit
        donc on réecrit la fonction pour actualiser la trajectoire selon cette regle
        """
        self.trajectoire = []
        self.can_eat_pion_passant(pieces)
        traj = [addition_tuple(self.get_pos(), self.direction_sans_obstacle[0]),
        addition_tuple(self.get_pos(), self.direction_sans_obstacle[1])]
        if (self.y == 1 and self.couleur*self.haut == 1) or (self.y == 6 and self.couleur*self.haut == -1):
            if not pieces.rechercher_piece(traj[0]) and not pieces.rechercher_piece(traj[1]):
                self.trajectoire.append(traj[1])
        if not pieces.rechercher_piece(traj[0]):
            self.trajectoire.append(traj[0])
        self.rajout_derniere_case(self.trajectoire, pieces,
        addition_tuple(self.get_pos(), (1, self.couleur*self.haut)))
        self.rajout_derniere_case(self.trajectoire, pieces,
        addition_tuple(self.get_pos(), (-1, self.couleur*self.haut)))


class Roi(Piece):
    def __init__(self, x:int, y:int, couleur:int):
        super().__init__(x, y, couleur)
        self.name = "roi"
        self.rock = True
        self.direction_sans_obstacle = list(DIRECTIONS.values())

    def add_rock(self, pieces, limite, mode):
        """
        Verifie si le roi peut rock
        """
        if pieces.en_echec(self.get_pos()):
            return None
        for x in range(limite+mode, self.x, mode):
            if pieces.rechercher_piece((x, self.y)) or pieces.en_echec((x, self.y)):
                return None
        piece = pieces.rechercher_piece((limite, self.y))
        if piece:
            if piece.name == "tour" and piece.couleur == self.couleur and piece.origin:
                return addition_tuple(self.get_pos(), (mode*2, 0))
        return None

    def actualiser_trajectoire(self, pieces):
        """
        Verifie si la trajectoire est possible sans que le roi soit menacé
        """
        super().actualiser_trajectoire(pieces)
        for rock in [self.add_rock(pieces, NB_CASE_ECHEC-1, -1), self.add_rock(pieces, 0, 1)]:
            if rock:
                self.trajectoire.append(rock)

class Tour(Piece):
    def __init__(self, x = 0, y = 0, couleur = 1):
        super().__init__(x, y, couleur, haut = 1)
        self.name = "tour"
        self.direction_avec_obstacle = LIGNES


class Fou(Piece):
    def __init__(self, x, y, couleur):
        super().__init__(x, y, couleur, haut = 1)
        self.name = "fou"
        self.direction_avec_obstacle = DIAGONALES

class Cavalier(Piece):
    def __init__(self, x, y, couleur):
        super().__init__(x, y, couleur, haut = 1)
        self.name = "cheval"
        self.direction_sans_obstacle = CHEVAL

class Reine(Piece):
    def __init__(self, x:int, y:int, couleur):
        super().__init__(x, y, couleur)
        self.name = "reine"
        self.direction_avec_obstacle = LIGNES + DIAGONALES




class Pieces():
    """
    Decrit l'echiquier niveau backend, on pourrait utiliser unne
    liste mais a trme on veut stocker dautres parametres :
    - historique
    - systeme de points
    - etc...
    """
#base de la classe
    def __init__(self, haut:int, liste_pieces:list()):
        self.liste_pieces = liste_pieces
        self.haut = haut
        self.historique = []
        self.pieces_manges = {}
        self.tour_joueur = 1
        self.nombre_tour = -1
        self.rois = {}

    def __str__(self) -> str:
        """
        Return toutes les pieces sous forme pos, couleur dans la liste piece
        """
        for piece in self.liste_pieces:
            print(piece)
        return "Pieces"

    def __contains__(self, piece:Piece):
        """
        Verifie la presence d'une piece dans l'echiquier
        """
        if piece in self.liste_pieces:
            return True
        return False

    @staticmethod
    def dedans(pos:tuple):
        """
        Verifie si une piece est dans lechiquier
        """
        x, y=pos
        if 0 <= x < NB_CASE_ECHEC:
            return 0 <= y < NB_CASE_ECHEC
        return False

#gestion tour

    def changement_tour(self, arriere = 1):
        self.nombre_tour+=(1*arriere)
        self.tour_joueur*=-1

    def get_tour(self):
        return self.tour_joueur

    def get_nombre_tour(self):
        return self.nombre_tour

#recherche des pieces

    def rechercher_piece(self, pos:tuple):
        """
        Recherche unique piece sur une position (x, y) donné
        """
        for piece in self.liste_pieces:
            if piece.get_pos() == pos:
                return piece
        return None

    def rechercher_piece_nom(self, nom:str, couleur:int):
        """
        Recherche unique piece selon nom et couleur donné
        """
        for piece in self.liste_pieces:
            if piece.name == nom and piece.couleur == couleur:
                return piece
        return None

    def rechercher_pieces(self, pos:tuple):
        """
        Recherche toutes les pieces sur la position (x, y) donné
        """
        ps = []
        for piece in self.liste_pieces:
            if piece.get_pos() == pos:
                ps.append(piece)
        return ps

#gestion des pieces

    def creer_piece(self, nom_piece:str, x:int, y:int):
        """
        Créer piece selon le nom et la pos donné (x, y) et le nom
        doit respecter la convention FEN modifie pour ce projet
        """
        #peut etre autre maniere moins redondante ???
        if nom_piece == "p":
            self.liste_pieces.append(Pion(x, y, 1, self.haut))
        elif nom_piece == "P":
            self.liste_pieces.append(Pion(x, y, -1, self.haut))
        elif nom_piece == "t":
            self.liste_pieces.append(Tour(x, y, 1))
        elif nom_piece == "T":
            self.liste_pieces.append(Tour(x, y, -1))
        elif nom_piece == "f":
            self.liste_pieces.append(Fou(x, y, 1))
        elif nom_piece == "F":
            self.liste_pieces.append(Fou(x, y, -1))
        elif nom_piece == "c":
            self.liste_pieces.append(Cavalier(x, y, 1))
        elif nom_piece == "C":
            self.liste_pieces.append(Cavalier(x, y, -1))
        elif nom_piece == "K":
            self.liste_pieces.append(Roi(x, y, -1))
        elif nom_piece == "k":
            self.liste_pieces.append(Roi(x, y, 1))
        elif nom_piece == "Q":
            self.liste_pieces.append(Reine(x, y, -1))
        elif nom_piece == "q":
            self.liste_pieces.append(Reine(x, y, 1))

    def supprimer_piece(self, piece):
        """
        Retire une piece de la liste de l'objet pieces
        """
        for i, p in enumerate(self.liste_pieces):
            if p.x == piece.x and p.y == piece.y and p.couleur == piece.couleur:
                self.pieces_manges[self.nombre_tour] = piece
                del self.liste_pieces[i]


#gestions des trajectoires des pieces

    def rock_tour(self, position_depart, position_arrive:tuple):
        """
        Bouge la tour pour faire  un rock
        pos : position de depart
        Note : fonction de deplacement mis en dehors de la piece concerne car elle
        en concerne plusieurs
        """
        if position_depart[0] < position_arrive[0]:
            self.rechercher_piece((NB_CASE_ECHEC-1, position_arrive[1])).move(addition_tuple(position_arrive, (-1, 0)))
        else:
            self.rechercher_piece((0, position_arrive[1])).move(addition_tuple(position_arrive, (1, 0)))

    def actualiser_trajectoires(self):
        """"
        Actualise les trajectoires de toutes les pieces
        """
        for piece in self.liste_pieces:
            if piece.couleur == self.tour_joueur and piece.name == "pion" and piece.pion_passant:
                piece.pion_passant = False
            piece.protege = False
        for piece in self.liste_pieces:
            piece.actualiser_trajectoire(self)
        roi = self.rois[self.tour_joueur]
        pieces_attaquantes = self.en_echec(piece_attaque=roi)
        if pieces_attaquantes:
            for piece in self.liste_pieces:
                piece.trajectoire = self.counter_en_echec(roi, piece, pieces_attaquantes)


#jeu des coups selon historique

    def ajouter_trajectoire_dans_historique(self, traj:str):
        if self.get_nombre_tour() >= len(self.historique):
            self.historique.append(traj)
        else:
            self.historique[self.get_nombre_tour()] = traj

    @staticmethod
    def traduction_position_norme_echec(position:int):
        return chr(position[0]+97)+str(position[1])

    @staticmethod
    def traduction_norme_echec_position(position:int):
        return ord(position[0])-97, int(position[1])

    def enregistrer_trajectoire(self, piece:Piece, pos_depart:int, pos_arrive:int, piece_mange:Piece):
        """
        enregistre le coup fait en format coonventionel
        """
        if piece_mange:
            self.ajouter_trajectoire_dans_historique(
                TRADUCTION_OBJET_FILE[(piece.name, piece.couleur)] +
                self.traduction_position_norme_echec(pos_depart) +
                "X" + self.traduction_position_norme_echec(pos_arrive)
            )
        else:
            self.ajouter_trajectoire_dans_historique(
               TRADUCTION_OBJET_FILE[(piece.name, piece.couleur)] +
               self.traduction_position_norme_echec(pos_depart)
               + " " + self.traduction_position_norme_echec(pos_arrive)
            )

    def jouer_coup(self):
        if self.get_nombre_tour()+1 < len(self.historique):
            self.changement_tour()
            pos_depart = self.traduction_norme_echec_position(
                self.historique[self.get_nombre_tour()][1:3]
                )
            pos_arrive = self.traduction_norme_echec_position(
                self.historique[self.get_nombre_tour()][4:]
                )
            piece = self.rechercher_piece(pos_depart)
            if abs(piece.get_pos()[0] - self.traduction_norme_echec_position(self.historique[self.get_nombre_tour()][4:])[0]) > 1 and piece.name == "roi":
                pos = piece.get_pos()
                piece.move()        
                self.rock(piece, pos)
            elif piece.name == "pion" and pos_depart[0]-pos_arrive[0] and not piece.manger_piece(self):
                self.supprimer_piece(
                    self.rechercher_piece((pos_arrive[0], pos_depart[1]))
                )
                piece.move(pos_arrive)
            else:
                piece.move(pos_arrive)
                piece.manger_piece(self)
            self.actualiser_trajectoires()

    def revenir_sur_le_coup(self):
        if self.get_nombre_tour() >= 0:
            pos_depart =  self.traduction_norme_echec_position(self.historique[self.nombre_tour][4:])
            pos_arrive = self.traduction_norme_echec_position(self.historique[self.nombre_tour][1:3])
            piece = self.rechercher_piece(pos_depart)
            if piece.name == "pion" and not self.rechercher_piece(pos_arrive) and  pos_depart[0]-pos_arrive[0]:
                self.liste_pieces.append((self.pieces_manges[self.nombre_tour]))
            if self.historique[self.nombre_tour][3] == "X":
                self.liste_pieces.append(self.pieces_manges[self.nombre_tour])
            elif piece.get_pos()[0] - pos_depart[0] > 1 and piece.name == "roi":
                self.rechercher_piece((piece.get_pos()[0], pos_depart[1]))
            elif piece.get_pos()[0] - pos_depart[0] < 1 and piece.name == "roi":
                self.rechercher_piece((piece.get_pos[0], pos_depart[1]))
            piece.move(pos_arrive)
            self.actualiser_trajectoires()
            self.changement_tour(-1)

#recherche de fin de partie

    def en_echec(self, pos:tuple = 1, couleur:int = 1, piece_attaque:Piece = None):
        """
        Verifie si une position est menace par une piece adverse
        """
        if piece_attaque:
            pos = piece_attaque.get_pos()
            couleur = piece_attaque.couleur
        pieces_attaquantes = []
        for piece in self.liste_pieces:
            if pos in piece.trajectoire and piece.couleur != couleur:
                if piece.couleur != couleur and (piece.name != "pion" or piece.x != pos[0]):#rajouter traj diago des pions
                    pieces_attaquantes.append(piece)
            else:
                pions = [self.rechercher_piece(addition_tuple(pos, (-1, couleur*self.haut))), self.rechercher_piece(addition_tuple(pos, (1, couleur*self.haut)))]
                for pion in pions:
                    if pion and pion.name == "pion" and pion.couleur != couleur:
                        pieces_attaquantes.append(pion)
        return pieces_attaquantes

    def counter_en_echec(self, piece_attaque:Piece, piece:Piece, pieces_attaquantes):
        """
        Verifie si une piece peut protege une position en echec
        """
        trajectoires =[]
        position_depart = piece.get_pos()
        for trajectoire in piece.trajectoire:
            piece.move(trajectoire)
            piece_mange = piece.manger_piece(self)
            for piece_attaquante in pieces_attaquantes:
                piece_attaquante.actualiser_trajectoire(self)
            if not self.en_echec(piece_attaque=piece_attaque):
                trajectoires.append(trajectoire)
            if piece_mange:
                    self.liste_pieces.append(piece_mange)
        piece.move(position_depart)
        return trajectoires

    def en_mat(self):
        """
        Verifie si le roi est en mat ou pas
        """
        if self.en_echec(self.rois[self.tour_joueur].get_pos()):
            for piece in self.liste_pieces:
                if piece.trajectoire:
                    return False
            return True
        return False

    def en_pat(self):
        """
        Verifie si le roi est en pat
        """
        if not self.en_echec(self.rois[self.tour_joueur].get_pos()):
            for piece in self.liste_pieces:
                if piece.trajectoire:
                    return False
            return True
        return False

if __name__ == "__main__":
    #disable des no member car probleme avec pygame
    import pylint.lint
    pylint_opts = ['--disable=trailing-whitespace', '--disable=no-member', '--disable=line-too-long', __file__]
    pylint.lint.Run(pylint_opts)

