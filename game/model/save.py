import pickle
from game.controller.worldController import WorldController

def saveGame():
    outfile = open("worldSave","wb")
    worldModel = WorldController.get_world_model()
    pickle.dump(worldModel,"worldSave")
    outfile.close()

