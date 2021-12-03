# , ici le nombre de case de lechiquier
NB_CASE_ECHEC = 8

#fichier a ouvrir : 
FICHIER = "partie/sauvegarde_test.fen"

#TRADUCTION objet --> file : 
TRADUCTION_OBJET_FILE = PATH_PIECE = {("reine", 1) : "q", ("roi", 1) : "k", ("tour", 1) : "t", 
("cheval", 1) : "c", ("fou", 1) : "f", ("pion", 1) : "p", 
("reine", -1) : "Q", ("roi", -1) : "K", ("tour", -1) : "T", 
("cheval", -1) : "C", ("fou", -1) : "F", ("pion", -1) : "P"}

#path relative de chaque piece
PATH_PIECE = {("reine", 1) : "reine_blanc.png", ("roi", 1) : "roi_blanc.png", ("tour", 1) : "tour_blanc.png", 
("cheval", 1) : "cheval_blanc.png", ("fou", 1) : "fou_blanc.png", ("pion", 1) : "pion_blanc.png", 
("reine", -1) : "reine_noir.png", ("roi", -1) : "roi_noir.png", ("tour", -1) : "tour_noir.png", 
("cheval", -1) : "cheval_noir.png", ("fou", -1) : "fou_noir.png", ("pion", -1) : "pion_noir.png"}


#couleur des differents cases, couleur inspiré de Quiet_Sub sur le forum:
#https://www.chess.com/forum/view/general/best-chess-board-color-setting


#constante de l'echiquier
TAILLE_CASE = 75
COULEUR_LIGNES = (0, 0, 0)
COULEUR_CASES_BLANCHE = (125, 135, 150)
COULEUR_CASE_NOIR = (232, 235, 239)
COULEUR_TRAJECTOIRE = (96, 96, 96)
LIMITEX_ECHIQUIER = TAILLE_CASE*NB_CASE_ECHEC
LIMITEY_ECHIQUIER = TAILLE_CASE*NB_CASE_ECHEC

TAILLE_GUI_X = 200
TAILLE_GUI_Y = 100

LONGUEUR_ECHIQUIER = TAILLE_CASE*NB_CASE_ECHEC

TAILLE_FENETRE = TAILLE_CASE*NB_CASE_ECHEC + TAILLE_GUI_X, TAILLE_CASE*NB_CASE_ECHEC + TAILLE_GUI_Y 

TYPE_CASE = {0 : COULEUR_CASE_NOIR, 1 : COULEUR_CASES_BLANCHE}

#bouton

PADDING_BOUTON = 30
PADDING_BOUTON_ECRAN = 10
COULEUR_BOUTON = (0, 0, 0)  #couleur des bontons a l'intèrieur

#bouton sauvegarde
TAILLE_BOUTON_SAUVEGARDE = (150, 30)
POSITION_BOUTON_SAUVEGARDE = (PADDING_BOUTON_ECRAN, TAILLE_FENETRE[1]-TAILLE_BOUTON_SAUVEGARDE[1]-PADDING_BOUTON_ECRAN)

#bouton retour arriere
TAILLE_BOUTON_ARRIERE = (70, 35)
POSITION_BOUTON_ARRIERE = (LONGUEUR_ECHIQUIER+PADDING_BOUTON_ECRAN, LONGUEUR_ECHIQUIER-PADDING_BOUTON_ECRAN-TAILLE_BOUTON_ARRIERE[1])

#bouton retour arriere
TAILLE_BOUTON_AVANT = (70, 35)
POSITION_BOUTON_AVANT = (TAILLE_FENETRE[0]-PADDING_BOUTON_ECRAN-TAILLE_BOUTON_AVANT[0], LONGUEUR_ECHIQUIER-PADDING_BOUTON_ECRAN-TAILLE_BOUTON_AVANT[1])



#padding de l'echiquier et des pieces dans une case
PADDING = 200
PADDING_PIECE = 40
PADDING_TRAJECTOIRE = PADDING_PIECE//2




#la case de debut
ORIGINE = (0, 0)

#nom des pieces

NOM_PIECES  = ("t", "f", "c", "q", "k", "T", "F", "C", "Q", "K")

#les direction possibles dans lechiquier
DIRECTIONS = { 'N' : (0,1), 'E' : (1,0), 'S' : (0, -1), 'W' : (-1, 0), 'NE' : (1, 1), 'SE' : (1, -1), 'NW' : (-1, 1), 'SW' : (-1, -1)}

#direction des lignes et colonnes
LIGNES = [DIRECTIONS["N"], DIRECTIONS["S"], DIRECTIONS["E"], DIRECTIONS["W"]]

#direction en diagonales
DIAGONALES = [DIRECTIONS["NE"], DIRECTIONS["SE"], DIRECTIONS["NW"], DIRECTIONS["SW"]]

#direction du cheval
CHEVAL = [(2, 1), (1, 2), (-2, 1), (-1, 2), (-2, -1), (1, -2), (2, -1), (-1, -2)]