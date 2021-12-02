
from constante import POSITION_BOUTON_ARRIERE, POSITION_BOUTON_AVANT, TAILLE_BOUTON_ARRIERE, POSITION_BOUTON_SAUVEGARDE, TAILLE_BOUTON_AVANT, TAILLE_BOUTON_SAUVEGARDE
from gestion_fichier import sauvegarder_partie
from gestion_pieces import pieces

def creer_dico(position, taille, fonction, argument):
    return {"Position" : position, "Taille" : taille, "Fonction" : fonction, "Arguments" : argument}

BOUTONS = {"Sauvegarder" : creer_dico(POSITION_BOUTON_SAUVEGARDE, TAILLE_BOUTON_SAUVEGARDE, sauvegarder_partie, None), 
"Retour arriere" : creer_dico(POSITION_BOUTON_ARRIERE, TAILLE_BOUTON_ARRIERE, pieces.revenir_sur_le_coup, None),
"Retour avant" : creer_dico(POSITION_BOUTON_AVANT, TAILLE_BOUTON_AVANT, pieces.jouer_coup, None)}

class bouton():
    def __init__(self, name, pos, taille, fonction, param):
        self.name = name
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.taille = taille
        self.width = self.taille[0]
        self.height = self.taille[1]
        self.fonction = fonction
        self.param = param

    def get_taille(self):
        return self.width, self.height

    def dedans(self, pos):
        if pos[0] > self.x and pos[0] < self.x+self.width:
            return pos[1] > self.y and pos[1] < self.y+self.height
        return False
    
    def activer_bouton(self, pieces):
        if self.param:
            print("activer")
            self.fonction(self.param)
        else:
            self.fonction(pieces)

class GUI():
    def __init__(self, boutons):
        self.boutons = boutons

    def click_sur_bouton(self, pos:tuple, pieces:pieces):
        for bouton in self.boutons:
            if bouton.dedans(pos):
                print(bouton.name)
                bouton.activer_bouton(pieces)

    def rechercher_bouton(self, name):
        for bouton in self.boutons:
            if bouton.name == name:
                return bouton
        return None
