
# représente les bâtiments
# tout ce qui fait partie de la carte, même l'herbe
class Building:
    nbBuilding = 0

    # on affecte des informations permettant d'ajuster le comportement dans le jeu
    def __init__(self, name, can_be_erase, can_constructible_over, can_be_walk_through, square_size):
        self.name                   = name                   # le nom du bâtiment représenté ( herbe, arbre, route, etc.)
        self.can_be_erase           = can_be_erase           # le bâtiment peut-il être effacer, action de clear
        self.can_constructible_over = can_constructible_over # peut-on construire par dessus le bâtiment, ( herbe )
        self.can_be_walk_through    = can_be_walk_through    # peut-on passer à travers ce bâtiments, ( ex: False pour l'eau )
        self.square_size            = square_size            # inutile, pour le moment, anticipation de tuile d'une certaine taille
        self.position_reference = None                       # emplacement sur la carte
        self.id = Building.nbBuilding+1
        Building.nbBuilding = self.id

    # permet d'affecter la position de reference
    def set_position_reference(self, position_reference):
        self.position_reference = position_reference

    # utile pour le pathfinding 
    def get_canbewalkthrough_into_integer(self):
        return 0 if self.can_be_walk_through else 1