
# classe permettant de gérer la logique géométrique du monde
from .building import Building
from .tente import Tente
import math

class Monde:
    def __init__(self, tile_size, screen_size):
        self.board = [] # plateau de jeu à deux dimension avec un dictionnaire contenant tous les bâtiments et des données géométrique
        self.width, self.height = screen_size
        self.tile_size = tile_size
        self.information_for_each_tile = self.get_information_for_each_tile() # dictionnaire avec les infos pour la construction de batiment
        self.habitations = [] # bâtiment considérés comme habitation
        self.ingenieurs  = [] # bâtiment pour les ingénieurs

    # réduit pour chaque habitation leur taux d'effondrement 
    def update(self):
        for habitation in self.habitations:
            habitation.reduce_collapsing_state()

    # pour chaque case, nous donnons le rectangle permettant de placer une tile à l'avenir
    def grid_to_board(self, num_lig, num_col, name):
        rect = [
            (num_lig * self.tile_size                            , num_col * self.tile_size                 ),
            (num_lig * self.tile_size + self.tile_size, num_col * self.tile_size                            ),
            (num_lig * self.tile_size + self.tile_size, num_col * self.tile_size + self.tile_size           ),
            (num_lig * self.tile_size                            , num_col * self.tile_size + self.tile_size),
        ]

        # pour le passage en vue isométrique
        iso = [self.to_iso(x,y) for x, y in rect]

        minx = min([x for x, y in iso])
        miny = min([y for x, y in iso])

        # retour de la fonction par des informations sur la tuile
        information_building = self.information_for_each_tile[name]
        sortie = {
            "grid": [num_lig, num_col], # l'emplacement dans le plateau
            "cart_rect": rect,          # le rect avec les value géometrique
            "iso": iso,                 # pour les calculs de 2D à 2.5D
            "position_rendu": [minx, miny], # coordonnées de placement au sein d'une surface isométrique
            "building": self.craft_building(information_building) # bâtiment associé
        }

        return sortie
    
    # passe les coordonnées en isométrique
    def to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    # initialise l'entiéreté du plateau
    def init_board(self, file_names):
        file_names = self.manage_for_water(file_names)
        file_names = self.manage_for_road (file_names)

        for num_lig in range(len(file_names)):
            self.board.append([])
            for num_col in range(len(file_names[num_lig])):
                tile_board = self.grid_to_board(num_lig, num_col, file_names[num_lig][num_col])
                self.board[num_lig].append(tile_board)

    # permet de choisir les bons sprites et de construire les bonnes routes pour l'affichage
    # l'algorithme utilisé ici est le même que dans la méthode manage_for_water
    # il est expliqué dans la méthode manage_for_water
    def manage_for_road(self, file_names):
        file_names_return = []
        for num_lig in range(0, len(file_names)):
            file_names_return.append([])
            for num_col in range(0, len(file_names)):
                if file_names[num_lig][num_col][0:5] == "route": # verifie que c'est une route
                    coords = [(-1,0),(0,1),(1,0),(0,-1)]
                    binary_array = []
                    for coord in coords:
                        if (num_lig+coord[0]) >= 0 and (num_lig+coord[0]) < len(file_names)    and \
                            (num_col+coord[1] >= 0) and (num_col+coord[1] < len(file_names[num_lig])) and \
                            file_names[num_lig+coord[0]][num_col+coord[1]][0:5] == "route": # si le voisin est une route
                            binary_array.append(1)
                        else:
                            binary_array.append(0)

                    sum = 0
                    for binary_value, i in zip(binary_array, range(3,-1, -1)):
                        sum = int(sum + binary_value*math.pow(2, i))

                    tile = "route droite"
                    match sum:
                        case  0: pass
                        case  1: tile = "route Debut de route"
                        case  2: tile = "route Debut de routebis"
                        case  3: tile = "route virage vers le bas"
                        case  4: tile = "route Fin de route"
                        case  5: tile = "route droite"
                        case  6: tile = "route Virage gauche vers droite"
                        case  7: tile = "route Début intersection deux voix"
                        case  8: tile = "route Fin de routebis"
                        case  9: tile = "route Virage gauche vers droite vers le haut"
                        case 10: tile = "route verticale"
                        case 11: tile = "route Intersectionbis"
                        case 12: tile = "route Virage gauche vers le bas"
                        case 13: tile = "route Intersection"
                        case 14: tile = "route Debut intersection deux voixbis"
                        case 15: tile = "route Carrefour"
                    
                    file_names_return[num_lig].append(tile)
                else:
                    file_names_return[num_lig].append(file_names[num_lig][num_col])

        return file_names_return

    # permet de construire les surfaces d'eau et de récupérer les bons sprites pour le bâtiments
    def manage_for_water(self, file_names):
        # l'algorithme employés est le suivant
        """
        nous regardons toutes les tuiles de notre plateau
        si la tuile courante est de l'eau alors
            on regarde tous ces voisins # admettons X est notre tuile on regarde autour de cette manière
            # (-1,-1)(-1,0)(-1,1)
            # (0,-1 )   X  (0,1)
            # (1,-1 )(1,0 )(1,1)
            on créer un tableau contenant des 0 et des 1 indiquant si le voisin est de l'eau alors
                on place un 1 sinon 0
            # le tableau contient donc 8 données = à 0 ou 1, mis bout à bout nous avons comme un code binaire
            on fait la somme de ce code binaire et le convertit en decimal, par exemple 00010001 = 33
            la valeur en decimale représente un sprite à utiliser, on détermine le sprite ainsi
            
            # Problème de cet algo, nous avons pour l'eau 2^8 possibilités, soit 256
            # cependant, il n'y à pas 256 sprites différents, nous pouvons avoir le même sprite pour plusieurs valeurs
            # tous les cas ne sont pas traités, mais suffisament pour faire une carte propre

            # Dans le cas des routes nous n'avons que 16 cas car on ne regarde pas en diagonale, soit 2^4 = 16
        """

        file_names_return = []
        for num_lig  in range(len(file_names)):
            file_names_return.append([])
            for num_col in range(len(file_names[num_lig])):
                if file_names[num_lig][num_col] == "eau":
                    binary_traitement = []
                    for coord in [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]:
                        
                        if (num_lig+coord[0])>=0 and (num_lig+coord[0])<len(file_names) and (num_col+coord[1])>=0 and (num_col+coord[1])<len(file_names[num_lig]) and file_names[num_lig+coord[0]][num_col+coord[1]] == 'eau':
                            binary_traitement.append(1)
                        else:
                            binary_traitement.append(0)

                    sum = 0
                    for binary_value, i in zip(binary_traitement, range(7,-1, -1)):
                        sum = int(sum + binary_value*math.pow(2, i))
                    
                    """
                    for debug
                    liste = [255,250,248,249,230,224,240,236,155,177,225,241,206,108,59,198,110,227,243,235,200,185,179,175,140,137,138,130,193,128,50,40,42,98,35,38,190,168,160,251,254,239,162,152,143,159,10,191,27,131,195,184,135,199,136,62,63,58,56,60,120,124,48,39,32,30,114,156,170,201,112,34,24,15,31,14,28,8,2,7,0]
                    if sum not in liste:
                        print(binary_traitement, sum)
                    """

                    tile = "eau"
                    match sum:
                        case 255: tile = "eau"
                        case 250: tile = "eau_redirection_droite"
                        case 248 | 249: tile = "eau_droite"
                        case 236: tile = "eau_redirection_two_to_gauche_gauche"
                        case 224 | 240 | 225 | 241 : tile = "eau_coin_bas_droite"
                        case 227 | 243: tile = "eau_bas"
                        case 168: tile = "eau_intersection_droite"
                        case 235: tile = "eau_redirection_bas"
                        case 110: tile = "eau_redirection_two_to_bas_gauche"
                        case 230: tile = "eau_redirection_two_to_haut_droite"
                        case 184 | 185: tile = "eau_redirection_two_to_gauche_droite"
                        case 160 | 177: tile = "eau_virage_bas_droite"
                        case 175: tile = "eau_redirection_gauche"
                        case 206: tile = "eau_redirection_two_to_droite_gauche"
                        case 155: tile = "eau_redirection_two_to_droite_droite"
                        case 162: tile = "eau_intersection_bas"
                        case 179: tile = "eau_redirection_two_to_haut_gauche"
                        case 193 | 128: tile = "eau_fin_gauche"
                        case 190: tile = "eau_redirection_haut"
                        case 251: tile = "eau_coin_bas_droite_interieur"
                        case 254: tile = "eau_coin_haut_droite_interieur"
                        case 239: tile = "eau_coin_bas_gauche_interieur"
                        case 143 | 159: tile = "eau_gauche"
                        case 59: tile = "eau_redirection_two_to_bas_droite"
                        case 42: tile = "eau_intersection_haut"
                        case 40 | 108: tile = "eau_virage_haut_droite"
                        case 191: tile = "eau_coin_haut_gauche_interieur"
                        case 131 | 195 | 135 | 199: tile = "eau_coin_bas_gauche"
                        case 136 | 156 | 201 | 152 | 200 | 140 | 137: tile = "eau_isole_horizontale"
                        case 62 | 63: tile = "eau_haut"
                        case 10 | 27: tile = "eau_virage_haut_gauche"
                        case 138: tile = "eau_intersection_gauche"
                        case 130 | 198: tile = "eau_virage_bas_gauche"
                        case  58: tile = 'eau_couloir'
                        case 170: tile = "eau_intersection"
                        case  56 | 60 | 120 | 124 : tile = "eau_coin_haut_droite"
                        case  48 | 32 | 112: tile = "eau_fin_haut"
                        case  30 | 15 | 31 | 14 : tile = "eau_coin_haut_gauche"
                        case  34 | 39 | 114 | 35 | 38 | 98 | 50: tile = "eau_isole_verticale"
                        case  28 | 8 | 24: tile = "eau_fin_droite"
                        case  2 | 7: tile="eau_fin_bas"
                        case  0: tile = "eau_isole"
                        case  _ : tile = "eau"

                    file_names_return[num_lig].append(tile)
                else:
                    file_names_return[num_lig].append(file_names[num_lig][num_col])

        return file_names_return

    # contient les informations pour la création de bâtiment
    def get_information_for_each_tile(self):
        dictionnaire = {
            'engeneer'                               : ['engeneer'                              , True , False, False, 1],
            'panneau'                                : ['panneau'                               , True , False, True , 1],
            'tente'                                  : ['tente'                                 , True , False, False, 1],
            'eau'                                    : ['eau'                                   , False, False, False, 1],
            'eau_haut'                               : ['eau_haut'                              , False, False, False, 1],
            'eau_bas'                                : ['eau_bas'                               , False, False, False, 1],
            'eau_droite'                             : ['eau_droite'                            , False, False, False, 1],
            'eau_gauche'                             : ['eau_gauche'                            , False, False, False, 1],
            "eau_redirection_two_to_gauche_droite"   : ['eau_redirection_two_to_gauche_droite'  , False, False, False, 1],
            "eau_redirection_two_to_gauche_gauche"   : ['eau_redirection_two_to_gauche_gauche'  , False, False, False, 1],
            "eau_redirection_two_to_droite_gauche"   : ['eau_redirection_two_to_droite_gauche'  , False, False, False, 1],
            "eau_redirection_two_to_droite_droite"   : ['eau_redirection_two_to_droite_droite'  , False, False, False, 1],
            'eau_redirection_two_to_haut_gauche'     : ['eau_redirection_two_to_haut_gauche'    , False, False, False, 1],
            'eau_redirection_two_to_haut_droite'     : ['eau_redirection_two_to_haut_droite'    , False, False, False, 1],
            'eau_redirection_two_to_bas_gauche'      : ['eau_redirection_two_to_bas_gauche'     , False, False, False, 1],
            'eau_redirection_two_to_bas_droite'      : ['eau_redirection_two_to_bas_droite'     , False, False, False, 1],
            'eau_intersection_bas'                   : ['eau_intersection_bas'                  , False, False, False, 1],
            'eau_intersection_haut'                  : ['eau_intersection_haut'                 , False, False, False, 1],
            'eau_intersection_gauche'                : ['eau_intersection_gauche'               , False, False, False, 1],
            'eau_intersection_droite'                : ['eau_intersection_droite'               , False, False, False, 1],
            'eau_coin_haut_gauche'                   : ['eau_coin_haut_gauche'                  , False, False, False, 1],
            'eau_coin_haut_droite'                   : ['eau_coin_haut_droite'                  , False, False, False, 1],
            'eau_coin_bas_droite'                    : ['eau_coin_bas_droite'                   , False, False, False, 1],
            'eau_coin_bas_gauche'                    : ['eau_coin_bas_gauche'                   , False, False, False, 1],
            'eau_coin_bas_droite_interieur'          : ['eau_coin_bas_droite_interieur'         , False, False, False, 1],
            'eau_coin_bas_gauche_interieur'          : ['eau_coin_bas_gauche_interieur'         , False, False, False, 1],
            'eau_coin_haut_gauche_interieur'         : ['eau_coin_haut_gauche_interieur'        , False, False, False, 1],
            'eau_coin_haut_droite_interieur'         : ['eau_coin_haut_droite_interieur'        , False, False, False, 1],
            'eau_coin_bas_droite_exterieur'          : ['eau_coin_bas_droite_exterieur'         , False, False, False, 1],
            'eau_coin_bas_gauche_exterieur'          : ['eau_coin_bas_gauche_exterieur'         , False, False, False, 1],
            'eau_virage_bas_droite'                  : ['eau_virage_bas_droite'                 , False, False, False, 1],
            'eau_virage_bas_gauche'                  : ['eau_virage_bas_gauche'                 , False, False, False, 1],
            'eau_virage_haut_droite'                 : ['eau_virage_haut_droite'                , False, False, False, 1],
            'eau_virage_haut_gauche'                 : ['eau_virage_haut_gauche'                , False, False, False, 1],
            'eau_coin_haut_droite_exterieur'         : ['eau_coin_haut_droite_exterieur'        , False, False, False, 1],
            'eau_coin_haut_gauche_exterieur'         : ['eau_coin_haut_gauche_exterieur'        , False, False, False, 1],
            'eau_redirection_droite'                 : ['eau_redirection_droite'                , False, False, False, 1],
            'eau_redirection_gauche'                 : ['eau_redirection_gauche'                , False, False, False, 1],
            'eau_redirection_bas'                    : ['eau_redirection_bas'                   , False, False, False, 1],
            'eau_redirection_haut'                   : ['eau_redirection_haut'                  , False, False, False, 1],
            'eau_intersection'                       : ['eau_intersection'                      , False, False, False, 1],
            'eau_isole'                              : ['eau_isole'                             , False, False, False, 1],
            'eau_isole_horizontale'                  : ['eau_isole_horizontale'                 , False, False, False, 1],
            'eau_isole_verticale'                    : ['eau_isole_verticale'                   , False, False, False, 1],
            'eau_fin_gauche'                         : ['eau_fin_gauche'                        , False, False, False, 1],
            'eau_fin_droite'                         : ['eau_fin_droite'                        , False, False, False, 1],
            'eau_fin_bas'                            : ['eau_fin_bas'                           , False, False, False, 1],
            'eau_fin_haut'                           : ['eau_fin_haut'                          , False, False, False, 1],
            'eau_couloir'                            : ['eau_couloir'                           , False, False, False, 1],
            'route droite'                           : ['route droite'                          , True , False,  True, 1],
            'route verticale'                        : ['route verticale'                       , True , False,  True, 1],
            'route droitebis'                        : ['route droitebis'                       , True , False,  True, 1],
            'route horizontale'                      : ['route horizontale'                     , True , False,  True, 1],
            'route Virage gauche vers le bas'        : ['route Virage gauche vers le bas', True, False, True, 1],
            'route virage vers le bas'                     : ['route virage vers le bas'                    , True,  False,  True, 1],
            'route Virage gauche vers droite'              : ['route Virage gauche vers droite'             , True,  False,  True, 1],
            'route Virage gauche vers droite vers le haut' : ['route Virage gauche vers droite vers le haut', True,  False,  True, 1],
            'route Debut de route'                         : ['route Debut de route'                        , True,  False,  True, 1],
            'route Debut de routebis'                      : ['route Debut de routebis'                     , True,  False,  True, 1],
            'route Fin de route'                           : ['route Fin de route'                          , True,  False,  True, 1],
            'route Fin de routebis'                        : ['route Fin de routebis'                       , True,  False,  True, 1],
            'route Fin de routebis2'                       : ['route Fin de routebis2'                      , True,  False,  True, 1],
            'route Début intersection deux voix'           : ['route Début intersection deux voix'          , True,  False,  True, 1],
            'route Debut intersection deux voixbis'        : ['route Debut intersection deux voixbis'       , True,  False,  True, 1],
            'route Intersection'                           : ['route Intersection'                          , True,  False,  True, 1],
            'route Intersectionbis'                        : ['route Intersectionbis'                       , True,  False,  True, 1],
            'route Carrefour'                              : ['route Carrefour'                             , True,  False,  True, 1]
        }

        for i in range(40,62):
            dictionnaire['arbre_{}'.format(i)] = ['arbre_{}'.format(i) , True , False, False, 1]

        for i in range(110,120):
            dictionnaire['herbe_{}'.format(i)] = ['herbe_{}'.format(i) , False , True, True, 1]
        
        return dictionnaire

    def define_matrix_for_path_finding_road_without_panneau(self):
        return [[ 0 if self.board[i][j]["building"].name != "panneau" and self.board[i][j]["building"].get_canbewalkthrough_into_integer() == 0 else 1 for j in range(0, len(self.board[0]))] for i in range(0,len(self.board)) ]

    # permet de récuper une matrice composer de 0 et 1, utile pour le pathfinding, le 1 représentant un obstacle
    def define_matrix_for_path_finding(self):
        return [[self.board[i][j]["building"].get_canbewalkthrough_into_integer() for j in range(0, len(self.board[0]))] for i in range(0,len(self.board)) ]
            
    # permet de récuper une matrice composer de 0 et 1, utile pour le pathfinding, le 1 représentant un obstacle
    # tout est obstacle si ce n'est pas une route
    def define_matrix_for_path_finding_road(self):
        return [[ 0 if self.board[i][j]["building"].name[0:5] == "route" else 1 for j in range(0, len(self.board[0]))] for i in range(0,len(self.board)) ]

    def check_if_construction_possible_on_grid(self,grid):
        if grid[0] >= 0 and grid[0] < len(self.board) and grid[1] >= 0 and grid[1] < len(self.board[grid[0]]):
            return self.board[grid[0]][grid[1]]["building"].can_constructible_over
        
        return False

    def check_if_clear_possible_on_grid(self, grid):
        return self.board[grid[0]][grid[1]]["building"].can_be_erase

    # construit un bâtiment spécifique selon les informations récupérées
    def craft_building(self, infos_building):
        if ( infos_building[0] == "tente" ): 
            building = Tente(infos_building[0], infos_building[1], infos_building[2], infos_building[3], infos_building[4])
            self.habitations.append(building)
            return building
        if infos_building[0] ==  "engeneer":
            building = Building(infos_building[0], infos_building[1], infos_building[2], infos_building[3], infos_building[4])
            self.ingenieurs.append(building)
            return building
        
        return Building(infos_building[0], infos_building[1], infos_building[2], infos_building[3], infos_building[4])

    # ajoute un bâtiment dans le plateau à une certaines coordonées
    def add_building_on_point(self, grid_pos, name):
        infos_building = self.information_for_each_tile[name]
        building = self.craft_building(infos_building)
        building.set_position_reference(grid_pos)
        self.board[grid_pos[0]][grid_pos[1]]["building"] = building
