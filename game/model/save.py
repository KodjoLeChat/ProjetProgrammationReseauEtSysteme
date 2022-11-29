import pickle
from game.controller.worldController import WorldController


class Save:

    def __init__(self, modelWorld):
        self.modelWorld = modelWorld

    def saveGame(self):
        with open("worldSave", "wb") as f1:
            pickle.dump(self.modelWorld, f1)
        f1.close()
