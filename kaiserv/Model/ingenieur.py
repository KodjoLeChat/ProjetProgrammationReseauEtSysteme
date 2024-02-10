from .walker import Walker
import random

# cette classe représente le rôle d'ingénieur
class Ingenieur(Walker):
    def __init__(self, actualPosition, destination):
        super().__init__(actualPosition, destination)
        self.position_reference = actualPosition # sera la position du bâtiment de réference
        self.nextPosition = self.actualPosition  # position à atteindre 
        self.name = "citizen_engeneer"           # nom définit pour comparer avec les citoyens lambda
        self.old_position = None                 # permet de ne pas retourner sur ses pas
        self.nb_deplacement_max = 30             # nombre de déplacement entre chaque tuile, pour l'illusion de fluidité

    # Permet de revenir au point de départ, utilisé lors du changement de l'environnement
    def reset_position(self):
        self.nextPosition   = self.position_reference
        self.actualPosition = self.position_reference
        self.nombreDeplacement = 0

    # permet de trouver vers quel tuile l'ingénieur va se diriger
    def find_new_destination(self, monde):
        self.set_nbdeplacement()
        # dans le cas où il atteint une tuile
        if self.nombreDeplacement == 0:
            self.actualPosition = self.nextPosition # change la poisition courante

            matrix = [(-1,0),(1,0),(0,-1),(0,1)] # permet de consulter les voisins
            valid_matrix = [] # contient les voisins possibles
            for coord in matrix:
                new_grid = (self.actualPosition[0]+coord[0], self.actualPosition[1]+coord[1])
                # si nous sommes prêt d'une route ou que nous sommes prêt de notre bâtiment de réference
                # on ajoute la coordonnées aux voisins possibles
                if new_grid != self.old_position and new_grid[0] >= 0 and new_grid[1] >= 0 and \
                   new_grid[0] < len(monde.board) and new_grid[1] < len(monde.board[new_grid[0]]) and \
                   monde.board[new_grid[0]][new_grid[1]]["building"].name[0:5] == "route" or \
                   monde.board[new_grid[0]][new_grid[1]]["building"].name == "engeneer" and \
                   monde.board[new_grid[0]][new_grid[1]]["building"].position_reference == self.position_reference:
                    valid_matrix.append(coord)
            
            self.old_position = self.actualPosition # change l'ancienne position
            if len(valid_matrix) > 0:
                # si nous avons des voisins sans point de demi-tour
                new_dest = valid_matrix[random.randint(0,len(valid_matrix)-1)]
                new_dest = (self.actualPosition[0]+new_dest[0], self.actualPosition[1]+new_dest[1])
            else:
                # on fait demi-tour car nous ne pouvons pas avancer ailleurs
                new_dest = self.old_position

            self.nextPosition = new_dest

    # permet de soigner les bâtiments autour de l'ingénieur
    def heal_around(self, monde):
        if self.nombreDeplacement == 0:
            # on regarde tous les voisins même en diagonale
            matrix = [(-1,0),(1,0),(0,-1),(0,1),(-1,1),(-1,-1),(1,-1),(1,1)]
            for coord in matrix:
                new_grid = (self.actualPosition[0]+coord[0], self.actualPosition[1]+coord[1])
                if new_grid[0] >= 0 and new_grid[1] >= 0 and \
                   new_grid[0] < len(monde.board) and new_grid[1] < len(monde.board[new_grid[0]]) and \
                   monde.board[new_grid[0]][new_grid[1]]["building"].name == "tente":
                   # si on est ok alors on soigne le batiment pour éviter qu'il s'effondre
                    monde.board[new_grid[0]][new_grid[1]]["building"].reset_collapsing_state()