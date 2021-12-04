from constante import *
"""
Fichier permettant la gestion de toutes les pieces au niveau backend

"""

def addition_tuple(t1:tuple, t2:tuple) -> tuple:
    """
    Addtionne les valeurs d'un tuple de dim2
    Rq peut se generaliser pour n dimension 
    mais inutile ici

    """
    x, y = t1
    x1, y1 = t2
    return (x+x1, y+y1)

def multiplier_tuple(t:(tuple), val:int) -> tuple:
    """
    Multiple le valeur d'un tuple de dim2
    Rq peut se generaliser pour n dimension 
    mais inutile ici
    """
    x, y = t
    return (x*val, y*val)

class piece():
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

    def trajectoire_vide(self):
        """
        Regarde si les trajectoires que peut prendre la piece
        existe
        """
        for traj in self.trajectoire:
            if traj != None:
                return False
        return True

    def pos_dans_trajectoire(self, pos):
        """
        Regarde si une position est dans la trajectoire de la piece
        """
        for p in self.trajectoire:
            if p == pos:
                return True
        return False

    def __str__(self):
        return "nom : " + self.name + "(" + str(self.x) + ", " + str(self.y ) + "," + str(self.couleur) + ")"

    def __eq__(self, other):
        """
        Compare la position de deux piece
        """
        if other == None:
            return False
        if self.x == other.x:
            return self.y == other.y
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def mouv(self, pos):
        """
        Place la piece a l'endroit pos
        """
        self.x, self.y = pos
        

    def pos(self):
        """"
        Get position of object
        """
        return self.x, self.y

    def manger_piece(self, pieces):
        """
        Verifie si la piece est sur une piece si oui elle le "mange"
        """
        ps = pieces.rechercher_pieces(self.pos())
        for p in ps:
            if p.couleur != self.couleur:
                pieces.supprimer_piece(p)
                return p
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

    def trajectoire_avec_obstacle(self, pieces, direction):
        """
        Creer la trajectoire selon la direction et verifie si elle est possible
        """
        t = []
        pos = addition_tuple(self.pos(), direction)
        while pieces.dedans(pos) and not pieces.rechercher_piece(pos):
            t.append(pos)
            pos = addition_tuple(direction, pos)
        self.rajout_derniere_case(t, pieces, pos)
        return t
    
    def trajectoire_sans_obstacle(self, pieces, pos):
        """
        Creer la trajectoire selon la position et everifie si cc'est possible
        """
        pos = addition_tuple(self.pos(), pos)
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
            self.trajectoire+=self.trajectoire_avec_obstacle(pieces, pos)
        so = [self.trajectoire_sans_obstacle(pieces, pos) 
        for pos in self.direction_sans_obstacle if self.trajectoire_sans_obstacle(pieces, pos) != None]
        if len(so):
            self.trajectoire+=so

    def deplacer_piece(self, pieces, pos):
        """
        Deplace la piece si celle-ci est dans la trajectoire
        """
        if self.pos_dans_trajectoire(pos): # and piece_selec.couleur == tour: #a rajjouter pour le tour par tour
            self.mouv(pos)
            piece = self.manger_piece(pieces)
            pieces.actualiser_trajectoires()  
        return piece

    def can_mouv_here(self, pos_arrive:tuple):
        return pos_arrive in self.trajectoire


    def plus_origin(self, pieces):
        """
        Permet de considerer hypothetiquepment que la piece n'est plus protege
        """
        self.origin = False
        self.actualiser_trajectoire(pieces)

"""
Ici les objet permettent de decrire chaque piece des echecs
"""


class pion(piece):
    def __init__(self, x:int = 0, y:int = 0, couleur:int = 1, tour:int = 1):
        super().__init__(x, y, couleur, tour)    
        self.name = "pion"
        self.origin = True
        self.direction_sans_obstacle = [multiplier_tuple(DIRECTIONS["N"], self.haut*self.couleur), multiplier_tuple((0, 2), self.haut*self.couleur)]

    def promotion(self):
        """
        Promotion du pion si possible, choix a faire graphiquement ?
        """
        if not self.y%(NB_CASE_ECHEC-1):
            return True
        return False
            
    def actualiser_trajectoire(self, pieces):
        """
        Pion special car peut manger les diagonales et ne peut pas manger tout droit
        donc on réecrit la fonction pour actualiser la trajectoire selon cette regle
        """
        self.trajectoire = []
        traj = [addition_tuple(self.pos(), self.direction_sans_obstacle[0]), addition_tuple(self.pos(), self.direction_sans_obstacle[1])]
        if (self.y == 1 and self.couleur*self.haut == 1) or (self.y == 6 and self.couleur*self.haut == -1):
            if not pieces.rechercher_piece(traj[0]) and not pieces.rechercher_piece(traj[1]):
                self.trajectoire.append(traj[1])
        if not pieces.rechercher_piece(traj[0]):
            self.trajectoire.append(traj[0])
        self.rajout_derniere_case(self.trajectoire, pieces, addition_tuple(self.pos(), (1, self.couleur*self.haut)))
        self.rajout_derniere_case(self.trajectoire, pieces, addition_tuple(self.pos(), (-1, self.couleur*self.haut)))

class tour(piece):
    def __init__(self, x = 0, y = 0, couleur = 1):
        super().__init__(x, y, couleur, haut = 1)
        self.name = "tour"
        self.direction_avec_obstacle = LIGNES


class fou(piece):
    def __init__(self, x, y, couleur):
        super().__init__(x, y, couleur, haut = 1)
        self.name = "fou"
        self.direction_avec_obstacle = DIAGONALES

class cavalier(piece):
    def __init__(self, x, y, couleur):
        super().__init__(x, y, couleur, haut = 1)
        self.name = "cheval"
        self.direction_sans_obstacle = CHEVAL

class roi(piece):
    def __init__(self, x:int, y:int, couleur:int):
        super().__init__(x, y, couleur)
        self.name = "roi"
        self.rock = True
        self.direction_sans_obstacle = list(DIRECTIONS.values())

    def actualiser_trajectoire(self, pieces):
        """
        Verifie si la trajectoire est possible sans que le roi soit menacé
        """
        super().actualiser_trajectoire(pieces)
        i = 0
        rocks = [self.add_rock(pieces, 1, NB_CASE_ECHEC-1), self.add_rock(pieces, -1)]
        for rock in rocks:
            if rock:
                self.trajectoire.append(rock)
        while i < len(self.trajectoire):
            traj = self.trajectoire[i]
            if pieces.en_echec(traj, self.couleur):
                del self.trajectoire[i]
                continue
            else:
                piece = pieces.rechercher_piece(traj)
                if piece:
                    if piece.protege:
                        del self.trajectoire[i]
                        continue                    
            i+=1
    @staticmethod
    def is_rocking(pos_depart, pos_arrive):
        if abs(pos_depart[0]- pos_arrive[0]) == 2:
            return True
        return False

    def verif_rock(self, pos, pieces):
        """
        Verifie si le roi peut rock
        """
        piece = pieces.rechercher_piece(pos)
        if piece:
            if piece.name == "tour" and piece.couleur == self.couleur and piece.origin:
                return True
        return False

    def add_rock(self, pieces, mode = 1, limite = 0):
        """
        Si verif rock alors dorock le roi se deplace alors
        de deux cases
        """
        rock = True
        if self.origin:
            for x in range(self.x+mode, limite, mode):
                pos = x, self.y
                if len(pieces.en_echec(pos, self.couleur)) or pieces.rechercher_piece(pos):
                    rock = False
            pos = (0, self.y)
            if self.verif_rock(pos, pieces) and rock:
                return addition_tuple(self.pos(), (mode*2, 0))    
        return None  
              
class reine(piece):
    def __init__(self, x:int, y:int, couleur):
        super().__init__(x, y, couleur)
        self.name = "reine"
        self.direction_avec_obstacle = LIGNES + DIAGONALES

class pieces():
    """
    Decrit l'echiquier niveau backend, on pourrait utiliser unne
    liste mais a trme on veut stocker dautres parametres : 
    - historique
    - systeme de points
    - etc...
    """

    def __init__(self, haut:int, liste_pieces:list):
        self.liste_pieces = liste_pieces
        self.haut = haut
        self.historique = []
        self.pieces_manges = {}
        self.tour_joueur = -1
        self.nombre_tour = -1
        
    def changement_tour(self, arriere = 1):
        self.nombre_tour+=(1*arriere)
        self.tour_joueur*=-1

    def get_tour(self):
        return self.tour_joueur

    def get_nombre_tour(self):
        return self.nombre_tour

    def rechercher_piece(self, pos:tuple):
        """
        Recherche unique piece sur une position (x, y) donné
        """
        for piece in self.liste_pieces:
            if piece.pos() == pos:
                return piece
        return None

    def rechercher_piece_nom(self, nom:str, couleur:int):
        """
        Recherche unique piece selon nom et couleur donné
        """
        for piece in self.liste_pieces:
            if piece.name == nom and piece.couleur == couleur:
                return piece
        
    def rechercher_pieces(self, pos:tuple):
        """
        Recherche toutes les pieces sur la position (x, y) donné
        """
        ps = []
        for piece in self.liste_pieces:
            if piece.pos() == pos:
                ps.append(piece)
        return ps
    
    def creer_piece(self, nom_piece:str, x:int, y:int):
        """
        Créer piece selon le nom et la pos donné (x, y) et le nom
        doit respecter la convention FEN modifie pour ce projet
        """
        #peut etre autre maniere moins redondante ???
        if nom_piece == "p":
            self.liste_pieces.append(pion(x, y, 1, self.haut))
        elif nom_piece == "P":
            self.liste_pieces.append(pion(x, y, -1, self.haut))
        elif nom_piece == "t":
            self.liste_pieces.append(tour(x, y, 1))
        elif nom_piece == "T":
            self.liste_pieces.append(tour(x, y, -1))
        elif nom_piece == "f":
            self.liste_pieces.append(fou(x, y, 1))
        elif nom_piece == "F":
            self.liste_pieces.append(fou(x, y, -1))
        elif nom_piece == "c":
            self.liste_pieces.append(cavalier(x, y, 1))
        elif nom_piece == "C":
            self.liste_pieces.append(cavalier(x, y, -1))
        elif nom_piece == "K":
            self.liste_pieces.append(roi(x, y, -1))
        elif nom_piece == "k":
            self.liste_pieces.append(roi(x, y, 1))
        elif nom_piece == "Q":
            self.liste_pieces.append(reine(x, y, -1))
        elif nom_piece == "q":
            self.liste_pieces.append(reine(x, y, 1))
    
    def ajouter_piece(self, piece):
        """
        Rajoute une piece a la liste de piece
        """
        self.liste_pieces.append(piece)

    def supprimer_piece(self, piece):
        """
        Retire une piece de la liste de l'objet pieces
        """
        for i, p in enumerate(self.liste_pieces):
            if p.x == piece.x and p.y == piece.y and p.couleur == piece.couleur:
                del self.liste_pieces[i]
        self.pieces_manges[self.nombre_tour] = piece

    def __str__(self) -> str:
        """
        Return toutes les pieces sous forme pos, couleur dans la liste piece
        """
        for piece in self.liste_pieces:
            print(piece)
        return "Pieces"

    def __contains__(self, piece:piece):
        """
        Verifie la presence d'une piece dans l'echiquier
        """
        if piece in self.liste_pieces:
            return True
        return False

    def reset_protection(self):
        """
        Eneleve la protection sur toutes les pieces
        """
        for piece in self.liste_pieces:
            piece.protege = False
    
    def actualiser_trajectoires(self):
        """"
        Actualise les trajectoires de toutes les pieces
        """
        self.reset_protection()
        r = []
        for piece in self.liste_pieces:
            if piece.name == "roi":
                r.append(piece)
            else:
                piece.actualiser_trajectoire(self)
        for roi in r:
            roi.actualiser_trajectoire(self)

    @staticmethod
    def traduction_position_norme_echec(position:int):
        return chr(position[0]+97)+str(position[1])

    @staticmethod
    def traduction_norme_echec_position(position:int):
        return ord(position[0])-97, int(position[1])

    def ajouter_trajectoire_dans_historique(self, traj:tuple):
        if self.get_nombre_tour() >= len(self.historique):
            self.historique.append(traj)
        else:
            self.historique[self.get_nombre_tour()] = traj
    
    def enregistrer_trajectoire(self, piece:piece, pos_depart:int, pos_arrive:int, piece_mange:piece):
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
            piece = self.rechercher_piece(self.traduction_norme_echec_position(self.historique[self.nombre_tour][1:3]))
            piece.mouv(self.traduction_norme_echec_position(self.historique[self.nombre_tour][4:]))
            piece.manger_piece(self)
            self.actualiser_trajectoires()

    def revenir_sur_le_coup(self):
        if self.get_nombre_tour() >= 0:
            if self.historique[self.nombre_tour][3] == "X":
                self.ajouter_piece(self.pieces_manges[self.nombre_tour-1])
            piece = self.rechercher_piece(self.traduction_norme_echec_position(self.historique[self.nombre_tour][4:]))
            piece.mouv( self.traduction_norme_echec_position(self.historique[self.nombre_tour][1:3])
            )
            self.actualiser_trajectoires()
            self.changement_tour(-1)
            
    def dedans(self, pos:tuple):
        """
        Verifie si une piece est dans lechiquier
        """
        x, y = pos
        if x  >= 0 and x< NB_CASE_ECHEC:
            return y >= 0 and y < NB_CASE_ECHEC
        return False

    def en_echec(self, pos:tuple, couleur:int,):
        """
        Verifie si une position est menace par une piece adverse
        """
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

    def counter_en_echec(self, pos:tuple, piece:piece, piece_attaque:piece, couleur:int):
        """
        Verifie si une piece peut protege une position en echec
        """
        p = piece.pos()
        for traj in piece.trajectoire:
            piece.mouv(traj)
            piece_attaque.actualiser_trajectoire(self)
            if not self.en_echec(pos, couleur): 
                piece.mouv(p)
                piece_attaque.actualiser_trajectoire(self)
                return True
        piece.mouv(p)
        piece_attaque.actualiser_trajectoire(self)
        return False
    
    def en_mat(self, piece:piece):
        """
        Verifie si le roi est en mat ou pas
        """
        pieces_attaque = self.en_echec(piece.pos(), piece.couleur)
        if len(pieces_attaque) and not len(piece.trajectoire):
            for p in self.liste_pieces:
                if p.couleur == piece.couleur:
                    for piece_attaque in pieces_attaque:
                        if self.counter_en_echec(piece.pos(), p, piece_attaque, piece.couleur):
                            return False
            return True
        return False
    
    def en_pat(self, couleur:int):
        """
        Verifie si le roi est en pat
        """
        for piece in self.liste_pieces:
            if piece.couleur == couleur and not piece.trajectoire_vide():
                return False 
        return True

    def fin_de_partie(self, roi_blanc, roi_noir, tour):
        """
        Regarde is la partie est terminée
        """
        if self.en_mat(roi_blanc):
            return -self.haut
        elif self.en_mat(roi_noir):
            return self.haut
        elif self.en_pat(tour):
            return 2
        else:
            return 0

    def rock(self, roi, pos:tuple):
        """
        Bouge la tour pour faire  un rock

        Note : fonction de deplacement mis en dehors de la piece concerne car elle
        en concerne plusieurs
        """
        if pos[0] < roi.x:
            self.rechercher_piece((NB_CASE_ECHEC-1, roi.y)).mouv(self,
                addition_tuple(roi.pos(), (-1, 0)))
        else:
            self.rechercher_piece((0, roi.y)).mouv(self, 
                addition_tuple(roi.pos(), (1, 0)))


