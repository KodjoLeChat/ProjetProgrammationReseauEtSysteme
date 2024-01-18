from Model.building import Building
import random
import json

# représente les tente dans lesquelles vont habiter les walkers
class Tente(Building):
    def __init__(self, name, can_be_erase, can_constructible_over, can_be_walk_through, square_size):
        super().__init__(name, can_be_erase, can_constructible_over, can_be_walk_through, square_size)
        self.collapsing_state = random.randint(25000, 40000) # pour estimer une durée avant effondrement 
        self.should_refresh = False

    # permet de remonter l'état d'éffondrement
    def reset_collapsing_state(self):
        if self.collapsing_state > 0:
            self.collapsing_state = random.randint(25000, 40000)
            self.should_refresh = True
    
    # permet de réduire l'état déffondrement
    # plus l'état est bas, plus le bâtiment est proche de s'effondrer
    def reduce_collapsing_state(self):
        if self.collapsing_state > 0:
            self.collapsing_state = self.collapsing_state - random.randint(3,10)
            if self.collapsing_state <= 0:
                self.collapsing_state = 0
                self.should_refresh = True

    def to_json(self):
        tente_dict = self.__dict__.copy()
        tente_dict['current_time'] = self.current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        tente_dict['last_action_time'] = self.last_action_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        return json.dumps(tente_dict, indent=4)


    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        tente = Tente(json_dict['name'], json_dict['can_be_erase'], json_dict['can_constructible_over'],
        json_dict['can_be_walk_through'], json_dict['square_size'])
        tente.position_reference = json_dict['position_reference']
        tente.id = json_dict['id']
        tente.owner = json_dict['owner']
        tente.current_time = json_dict['current_time']
        tente.check_interval = json_dict['check_interval']
        tente.last_action_time = json_dict['last_action_time']
        tente.collapsing_state = json_dict['collapsing_state']
        tente.should_refresh = json_dict['should_refresh']
        return tente