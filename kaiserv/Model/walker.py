import json
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
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        walker = Walker(json_dict['actualPosition'], json_dict['destination'])
        walker.ID = json_dict['ID']
        walker.nextPosition = json_dict['nextPosition']
        walker.name = json_dict['name']
        walker.chemin = json_dict['chemin']
        walker.nombreDeplacement = json_dict['nombreDeplacement']
        walker.nb_deplacement_max = json_dict['nb_deplacement_max']
        return walker