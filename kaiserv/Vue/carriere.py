import pygame
import pickle

from .camera import Camera
from .zoom import Zoom

# permet de gérer l'affichage de la carte ainsi que les evenements associées
class Carriere:
    def __init__(self, controleur):
        self.controleur = controleur
        self.width, self.height = self.controleur.screen.get_size()

        # camera pour se déplacer dans le monde
        self.camera = Camera(self.width, self.height) # camera de mouvement 
        # path selon tile
        self.dictionnaire = self.get_tile()
        self.dictionnaire_reverse_by_path = self.get_dictionnary_by_path()
        # surface sur lesquels notre map de base s'affiche
        self.basic_surface   = None # surface de base, servant de surface de reference 
        self.current_surface = None # surface actuelle à draw
        self.basic_surface_size = None # taille de la surface originale
        # informations sur les tuiles
        self.informations_tiles = None # informations sur nos tuiles dans notre carte
        # zoom sur la carte
        self.zoom = Zoom() # gestion du zoom
        self.zoom.update(0) # met un certain niveau de zoom au début

    # reintialise le zoom et la camera pour se replacer correctement 
    def reset(self):
        self.zoom = Zoom()
        self.zoom.update(0)
        self.camera = Camera(self.width, self.height)

    # draw les composants principaux de notre carriere
    def draw_main_components(self):
        # on met un fond noir
        self.controleur.screen.fill((0, 0, 0))
        if self.zoom.should_scale: # si nous devons zoomer alors on scale la surface
            self.current_surface = pygame.transform.scale(self.basic_surface,(self.basic_surface_size[0]*self.zoom.multiplier, self.basic_surface_size[1]*self.zoom.multiplier) )
            self.zoom.should_scale = False
        
        # on draw la surface
        self.controleur.screen.blit(self.current_surface, (self.camera.scroll.x, self.camera.scroll.y))

    # permet d'afficher les walkers de la carte
    def draw_walker(self):
        walkers_infos = self.controleur.get_walker_infos()
        if walkers_infos != None:
            for walker in walkers_infos:
                if ( walker.name == "citizen" and walker.destination != walker.actualPosition or walker.name == "citizen_engeneer" )and self.informations_tiles[walker.actualPosition[0]][walker.actualPosition[1]]["position_rendu"] != None \
                    and self.informations_tiles[walker.nextPosition[0]][walker.nextPosition[1]]["position_rendu"] != None:
                    coef = walker.nombreDeplacement / walker.nb_deplacement_max
                    image = self.dictionnaire[walker.name]
                    image = pygame.transform.scale(image, (image.get_width()*self.zoom.multiplier, image.get_height()*self.zoom.multiplier))
                    positionActuelle = self.informations_tiles[walker.actualPosition[0]][walker.actualPosition[1]]["position_rendu"]
                    positionSuivante = self.informations_tiles[walker.nextPosition  [0]][walker.nextPosition  [1]]["position_rendu"]
                    positionFinale   = (positionActuelle[0]+(positionSuivante[0] - positionActuelle[0])*coef, positionActuelle[1]+(positionSuivante[1] - positionActuelle[1])*coef)
                    positionFinale = (
                        ((positionFinale[0]*self.zoom.multiplier + self.current_surface.get_width()/2 + self.camera.scroll.x)),
                        ((positionFinale[1]*self.zoom.multiplier - (image.get_height() - self.controleur.TILE_SIZE*self.zoom.multiplier )+ self.camera.scroll.y))
                    )

                    self.controleur.screen.blit(image, positionFinale)

    def events(self, event):
    # met à jour le zoom 
        if event.type == pygame.MOUSEWHEEL:
                self.zoom.update(event.y)
       
    # permet d'enregistrer la partie
    def Save_game(self):
        object = self.controleur.metier
        filename = "save.sav"
        filehandler = open(filename, 'wb') 
        pickle.dump(object, filehandler)

    # permet de recharger la surface principale du jeu, utile si notamment, nous changeons des batiments dans la partie
    def reload_board(self):
        self.informations_tiles = self.controleur.get_board()
        self.basic_surface_size = (self.controleur.TILE_SIZE*self.controleur.grid_width*2,
                                   self.controleur.TILE_SIZE*self.controleur.grid_height*2+self.controleur.TILE_SIZE)
        self.basic_surface = pygame.Surface(self.basic_surface_size)
        self.current_surface = self.basic_surface
        self.informations_tiles = self.controleur.get_board()

        for num_lig in range(len(self.informations_tiles)):
            for num_col in range(len(self.informations_tiles[num_lig])):
                name = self.informations_tiles[num_lig][num_col]["building"].name
                image = self.dictionnaire[name] if name != None else None
                position = self.informations_tiles[num_lig][num_col]["position_rendu"]
                self.basic_surface.blit(image, (position[0] + self.basic_surface.get_width()/2,
                                                position[1] -(image.get_height() - self.controleur.TILE_SIZE)))
        
        self.current_surface = pygame.transform.scale(self.basic_surface,(self.basic_surface_size[0]*self.zoom.multiplier, self.basic_surface_size[1]*self.zoom.multiplier) )

    # met à jour la carriere
    def update(self):
        self.camera.update()
        habitations = self.controleur.get_habitations()
        should_reload =  False
        for habitation in habitations:
            if habitation.should_refresh and habitation.collapsing_state == 0:
                should_reload = True
                habitation.name = 'destruction'
                habitation.should_refresh = False

        if should_reload:
            self.reload_board()


    # initialise chaque sprite à afficher 
    def init_sprite(self):
        self.reload_board()

    
    # permet de récupérer le chemin d'une image
    def get_tile(self):
        dictionnaire = {
            'destruction'                   : pygame.image.load("assets/upscale_land/Land2a_00114.png").convert_alpha(),
            'while_crafting'                : pygame.image.load("assets/upscale_land/Land2a_00001.png").convert_alpha(),
            'eau'                           : pygame.image.load("assets/upscale_sea/Land1a_00120.png").convert_alpha(),
            'eau_haut'                      : pygame.image.load("assets/upscale_sea/Land1a_00136.png").convert_alpha(),
            'eau_bas'                       : pygame.image.load("assets/upscale_sea/Land1a_00128.png").convert_alpha(),
            'eau_droite'                    : pygame.image.load("assets/upscale_sea/Land1a_00140.png").convert_alpha(),
            'eau_gauche'                    : pygame.image.load("assets/upscale_sea/Land1a_00132.png").convert_alpha(),
            'eau_coin_haut_gauche'          : pygame.image.load("assets/upscale_sea/Land1a_00148.png").convert_alpha(),
            'eau_coin_haut_droite'          : pygame.image.load("assets/upscale_sea/Land1a_00152.png").convert_alpha(),
            'eau_coin_bas_droite'           : pygame.image.load("assets/upscale_sea/Land1a_00156.png").convert_alpha(),
            'eau_coin_bas_gauche'           : pygame.image.load("assets/upscale_sea/Land1a_00144.png").convert_alpha(),
            'eau_coin_bas_droite_interieur' : pygame.image.load("assets/upscale_sea/Land1a_00173.png").convert_alpha(),
            'eau_coin_bas_gauche_interieur' : pygame.image.load("assets/upscale_sea/Land1a_00170.png").convert_alpha(),
            'eau_coin_haut_gauche_interieur': pygame.image.load("assets/upscale_sea/Land1a_00171.png").convert_alpha(),
            'eau_coin_haut_droite_interieur': pygame.image.load('assets/upscale_sea/Land1a_00172.png').convert_alpha(),
            'eau_coin_bas_droite_exterieur' : pygame.image.load('assets/upscale_sea/Land1a_00173.png').convert_alpha(),
            'eau_coin_bas_gauche_exterieur' : pygame.image.load('assets/upscale_sea/Land1a_00173.png').convert_alpha(),
            'eau_coin_haut_droite_exterieur': pygame.image.load('assets/upscale_sea/Land1a_00173.png').convert_alpha(),
            'eau_coin_haut_gauche_exterieur': pygame.image.load('assets/upscale_sea/Land1a_00173.png').convert_alpha(),
            'eau_redirection_droite'        : pygame.image.load('assets/upscale_sea/Land1a_00176.png').convert_alpha(),
            'eau_redirection_gauche'        : pygame.image.load('assets/upscale_sea/Land1a_00174.png').convert_alpha(),
            'eau_redirection_haut'          : pygame.image.load('assets/upscale_sea/Land1a_00175.png').convert_alpha(),
            'eau_redirection_bas'           : pygame.image.load('assets/upscale_sea/Land1a_00177.png').convert_alpha(),
            'eau_redirection_two_to_gauche_droite' : pygame.image.load('assets/upscale_sea/Land1a_00193.png').convert_alpha(),
            'eau_redirection_two_to_gauche_gauche' : pygame.image.load('assets/upscale_sea/Land1a_00192.png').convert_alpha(),
            'eau_redirection_two_to_droite_droite' : pygame.image.load('assets/upscale_sea/Land1a_00187.png').convert_alpha(),
            'eau_redirection_two_to_droite_gauche' : pygame.image.load('assets/upscale_sea/Land1a_00186.png').convert_alpha(),
            'eau_redirection_two_to_bas_gauche'    : pygame.image.load('assets/upscale_sea/Land1a_00190.png').convert_alpha(),
            'eau_redirection_two_to_bas_droite'    : pygame.image.load('assets/upscale_sea/Land1a_00189.png').convert_alpha(),
            'eau_redirection_two_to_haut_gauche'   : pygame.image.load('assets/upscale_sea/Land1a_00183.png').convert_alpha(),
            'eau_redirection_two_to_haut_droite'   : pygame.image.load('assets/upscale_sea/Land1a_00184.png').convert_alpha(),
            'eau_intersection_bas'          : pygame.image.load('assets/upscale_sea/Land1a_00185.png').convert_alpha(),
            'eau_intersection_haut'         : pygame.image.load('assets/upscale_sea/Land1a_00191.png').convert_alpha(),
            'eau_intersection_gauche'       : pygame.image.load('assets/upscale_sea/Land1a_00188.png').convert_alpha(),
            'eau_intersection_droite'       : pygame.image.load('assets/upscale_sea/Land1a_00194.png').convert_alpha(),
            'eau_virage_bas_droite'         : pygame.image.load('assets/upscale_sea/Land1a_00198.png').convert_alpha(),
            'eau_virage_bas_gauche'         : pygame.image.load('assets/upscale_sea/Land1a_00195.png').convert_alpha(),
            'eau_virage_haut_droite'        : pygame.image.load('assets/upscale_sea/Land1a_00197.png').convert_alpha(),
            'eau_virage_haut_gauche'        : pygame.image.load('assets/upscale_sea/Land1a_00196.png').convert_alpha(),
            'eau_isole'                     : pygame.image.load('assets/upscale_sea/Land1a_00199.png').convert_alpha(),
            'eau_fin_gauche'                : pygame.image.load('assets/upscale_sea/Land1a_00164.png').convert_alpha(),
            'eau_fin_droite'                : pygame.image.load('assets/upscale_sea/Land1a_00166.png').convert_alpha(),
            'eau_fin_haut'                  : pygame.image.load('assets/upscale_sea/Land1a_00167.png').convert_alpha(),
            'eau_fin_bas'                   : pygame.image.load('assets/upscale_sea/Land1a_00165.png').convert_alpha(),
            'eau_intersection'              : pygame.image.load('assets/upscale_sea/Land1a_00182.png').convert_alpha(),
            'eau_isole_verticale'           : pygame.image.load('assets/upscale_sea/Land1a_00160.png').convert_alpha(),
            'eau_isole_horizontale'         : pygame.image.load('assets/upscale_sea/Land1a_00162.png').convert_alpha(),
            'eau_couloir'                   : pygame.image.load('assets/upscale_sea/Land1a_00189.png').convert_alpha(),
            'panneau'                       : pygame.image.load("assets/upscale_house/Housng1a_00045.png").convert_alpha(),
            'citizen'                       : pygame.image.load("assets/upscale_citizen/Citizen05_00001.png").convert_alpha(),
            'tente'                         : pygame.image.load("assets/upscale_house/Housng1a_00002.png").convert_alpha(),
            'citizen_engeneer'              : pygame.image.load("assets/upscale_citizen/Citizen01_01226.png").convert_alpha(),
            'engeneer'                      : pygame.image.load("assets/upscale_house/transport_00056.png").convert_alpha(),
            'route droite'                  : pygame.image.load('assets/upscale_road/Land2a_00093.png').convert_alpha(),
            'route verticale'               : pygame.image.load('assets/upscale_road/Land2a_00094.png').convert_alpha(),
            'route droitebis'               : pygame.image.load('assets/upscale_road/Land2a_00095.png').convert_alpha(),
            'route horizontale'             : pygame.image.load('assets/upscale_road/Land2a_00096.png').convert_alpha(),
            'route virage vers le bas'            : pygame.image.load('assets/upscale_road/Land2a_00097.png').convert_alpha(),
            'route Virage gauche vers droite'     : pygame.image.load('assets/upscale_road/Land2a_00098.png').convert_alpha(),
            'route Virage gauche vers le bas'     : pygame.image.load('assets/upscale_road/Land2a_00099.png').convert_alpha(),
            'route Virage gauche vers droite vers le haut': pygame.image.load('assets/upscale_road/Land2a_00100.png').convert_alpha(),
            'route Debut de route'   : pygame.image.load('assets/upscale_road/Land2a_00101.png').convert_alpha(),
            'route Debut de routebis': pygame.image.load('assets/upscale_road/Land2a_00102.png').convert_alpha(),
            'route Fin de route'     : pygame.image.load('assets/upscale_road/Land2a_00103.png').convert_alpha(),
            'route Fin de routebis'  : pygame.image.load('assets/upscale_road/Land2a_00104.png').convert_alpha(),
            'route Fin de routebis2' : pygame.image.load('assets/upscale_road/Land2a_00105.png').convert_alpha(),
            'route Début intersection deux voix'   : pygame.image.load('assets/upscale_road/Land2a_00106.png').convert_alpha(),
            'route Debut intersection deux voixbis': pygame.image.load('assets/upscale_road/Land2a_00107.png').convert_alpha(),
            'route Intersection'   : pygame.image.load('assets/upscale_road/Land2a_00108.png').convert_alpha(),
            'route Intersectionbis': pygame.image.load('assets/upscale_road/Land2a_00109.png').convert_alpha(),
            'route Carrefour'      : pygame.image.load('assets/upscale_road/Land2a_00110.png').convert_alpha()
        }

        # permet de récupérer les chemins des sprites des arbres
        for i in range(40, 62):
            dictionnaire["arbre_{}".format(i)] = pygame.image.load('assets/upscale_land/Land1a_000{}.png'.format(i)).convert_alpha()

        # peremt de récuperer les herbes existantes
        for i in range(110, 120):
            dictionnaire["herbe_{}".format(i)] = pygame.image.load('assets/upscale_land/Land1a_00{}.png'.format(i)).convert_alpha()

        return dictionnaire

    # dictionnaire inverse, utile pour recuper, un nom de sprite selon le path
    # utilise pour peu de nom en réalité, mais dans un souvis d'anticipation, nous avons set pour tout le monde
    def get_dictionnary_by_path(self):
        dictionnaire = {
            "assets/upscale_citizen/Citizen01_01226.png":'citizen_engeneer'        ,
            "assets/upscale_house/transport_00056.png"  :'engeneer'                ,
            "assets/upscale_house/Land2a_00068.png"  : "destruction"               ,
            "assets/upscale_sea/Land2a_00001.png"    : "while_crafting"            ,
            "assets/upscale_house/Housng1a_00045.png": "panneau"                   ,
            "assets/upscale_sea/Land1a_00120.png": 'eau'                           ,
            "assets/upscale_sea/Land1a_00136.png": 'eau_haut'                      ,
            "assets/upscale_sea/Land1a_00128.png": 'eau_bas'                       ,
            "assets/upscale_sea/Land1a_00140.png": 'eau_droite'                    ,
            "assets/upscale_sea/Land1a_00132.png": 'eau_gauche'                    ,
            "assets/upscale_sea/Land1a_00150.png": 'eau_coin_haut_gauche'          ,
            "assets/upscale_sea/Land1a_00152.png": 'eau_coin_haut_droite'          ,
            "assets/upscale_sea/Land1a_00156.png": 'eau_coin_bas_droite'           ,
            "assets/upscale_sea/Land1a_00146.png": 'eau_coin_bas_gauche'           ,
            "assets/upscale_sea/Land1a_00173.png": 'eau_coin_bas_droite_interieur' ,
            "assets/upscale_sea/Land1a_00170.png": 'eau_coin_bas_gauche_interieur' ,
            "assets/upscale_sea/Land1a_00171.png": 'eau_coin_haut_gauche_interieur',
            'assets/upscale_sea/Land1a_00172.png': 'eau_coin_haut_droite_interieur',
            'assets/upscale_sea/Land1a_00189.png': 'eau_couloir',
            'assets/upscale_sea/Land1a_00164.png' : 'eau_fin_gauche',
            'assets/upscale_sea/Land1a_00160.png': 'eau_isole_verticale',
            'assets/upscale_sea/Land1a_00162.png': 'eau_isole_horizontale',
            'assets/upscale_sea/Land1a_00199.png': 'eau_isole',
            "assets/upscale_house/Housng1a_00002.png": 'tente',
            "assets/upscale_road/Land2a_00093.png" : 'route droite',
            "assets/upscale_road/Land2a_00094.png" : 'route verticale',
            "assets/upscale_road/Land2a_00095.png" : 'route droitebis',
            "assets/upscale_road/Land2a_00096.png" : 'route horizontale',
            "assets/upscale_road/Land2a_00097.png" : 'route virage vers le bas',
            "assets/upscale_road/Land2a_00098.png" : 'route Virage gauche vers droite',
            "assets/upscale_road/Land2a_00099.png" : 'route Virage gauche vers le bas',
            "assets/upscale_road/Land2a_00100.png" : 'route Virage gauche vers droite vers le haut',
            "assets/upscale_road/Land2a_00101.png" : 'route Debut de route',
            "assets/upscale_road/Land2a_00102.png" : 'route Debut de routebis',
            "assets/upscale_road/Land2a_00103.png" : 'route Fin de route',
            "assets/upscale_road/Land2a_00104.png" : 'route Fin de routebis',
            "assets/upscale_road/Land2a_00105.png" : 'route Fin de routebis2',
            "assets/upscale_road/Land2a_00106.png" : 'route Début intersection deux voix',
            "assets/upscale_road/Land2a_00107.png" : 'route Debut intersection deux voixbis',
            "assets/upscale_road/Land2a_00108.png" : 'route Intersection',
            "assets/upscale_road/Land2a_00109.png" : 'route Intersectionbis',
            "assets/upscale_road/Land2a_00110.png" : 'route Carrefour'
        }

        for i in range(40, 62):
            dictionnaire["assets/upscale_land/Land1a_000{}.png".format(i)] = "arbre_{}".format(i)
        
        for i in range(110, 120):
            dictionnaire["assets/upscale_land/Land1a_00{}.png".format(i)] = "herbe_{}".format(i)

        return dictionnaire

