class Walker:
    nb_walker = 0

    def __init__(self,actualPosition,destination):
        self.ID = Walker.nb_walker+1
        Walker.nb_walker=self.ID             # identifiant du walker
        self.actualPosition = actualPosition # comment récupérer la position actuelle d'un walker?
        self.nextPosition = None
        self.destination = destination       # position généralement désignée par la construction d'une maison
        self.name = "citizen"                # fichier sprite du walker
        self.chemin = None                   # chemins à réaliser pour atteindre un point
        """
        Pour simuler la sensation de fluidité entre chaque tuile,
        nous faisons de plus petits déplacements entre deux tuiles.
        """
        self.nombreDeplacement = 0           # le nombre de petits déplacements réalisés
        self.nb_deplacement_max = 10         # le nombre de déplacements à faire entre chaque tuile

    # permet d'incrémenter le nombre de déplacement 
    def set_nbdeplacement(self):
        self.nombreDeplacement = (self.nombreDeplacement+1)%self.nb_deplacement_max

    # permet de set la position suivante dans le cas ou nous avons encore un tuple dans les chemins
    def set_nextPosition(self):
        if self.chemin != None and self.chemin != False and len(self.chemin) > 1:
            self.nextPosition = self.chemin[1]