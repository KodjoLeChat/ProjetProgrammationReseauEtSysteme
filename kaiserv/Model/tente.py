from Model.building import Building
import random

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