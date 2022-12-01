class BuildingController:

    def __init__(self):
        self.listBuildingModel = list()

    def add_listBuildingModel(self, building):
        self.listBuildingModel.append(building)

    def updateBuilding(self):
        for building in self.listBuildingModel:
            building.add_damage(5)
