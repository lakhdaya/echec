from constante import FICHIER, NB_CASE_ECHEC, TAILLE_CASE, TRADUCTION_OBJET_FILE
import gestion_pieces
#rappel : 
# fichier fen selon convention international avec acronyme traduit en francais AUSSI majuscul = blanc et minuscule = noir
#echiqiuer en [y][x]
# 1 haut donc ...
#-1 bas donc ...

def ouverture_fichier(nom_fichier:str, mode_ouverture:str = "r") -> None:
    """
    fonction permettant le control de l'ouverture d'un fichier
    et control l'erreur sans quitter le programme
    
    """
    try:
        file = open(nom_fichier, mode_ouverture)
        return file
    except:
        print("Probleme ouverture fichier")
        return None

def positionner_pieces(disposition_pieces:list(), pieces:gestion_pieces.pieces, haut:int) -> None:
    """
    Crée une liste de piece aux coordonnées donnée par une liste
    contenant le type de la piece et ses coordonnées
    
    """
    for y, ligne in enumerate(disposition_pieces):
        avance = 0
        if y == len(disposition_pieces)-1:
            break
        for x, case in enumerate(ligne):
            if x == len(ligne):
                break
            try:    
                int(case)
                avance+=int(case)
            except:
                pieces.creer_piece(case, x+avance, y)

def lecture_fichier_FEN(fichier, haut:int) -> gestion_pieces.pieces:
    """
    Créé l'objet pieces à partie d'un fichier .FEN respectant les
    conventions d'écriture FEN sauf pour le roi
    roi : k pour blanc et K pour noir
    #question fonction dans pieces ou dans le fichier gestion_fichier ?
    """
    pieces= gestion_pieces.pieces(haut, [])
    disposition_pieces = fichier.read().split("\\")
    positionner_pieces(disposition_pieces, pieces, haut)
    return pieces


"""
A faire : Lecture d'un match traduction de la forme algébrique a l'echiquier

"""

def sauvegarder_partie(pieces:gestion_pieces.pieces) -> None:
    """
    Pour linstant crée juste le positionnement de la fin de partie
    A terme : sauvegarde les coups aussi
    """
    file = open("partie/sauvegarde_test.fen", "w+")
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