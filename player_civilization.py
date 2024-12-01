from resources import ResourceStack

class Civilization:
    id = 0
    def __init__(self):
        self.settlements = []
        # self.sciencePerTurn = 0
        # self.goldPerTurn = 0
        # self.productionPerTurn = 0
        # self.foodPerTurn = 0
        self.yieldsByType = {ResourceStack.ResourceTypes['production'] : 0, 
                             ResourceStack.ResourceTypes['food'] : 0}
        self.id = Civilization.id
        Civilization.id+=1

    def __repr__(self):
        return f'civilization(id={Civilization.id})'

    def addSettlement(self, settlement):
        self.settlements.append(settlement)
    
    def removeSettlement(self, settlement):
        self.settlements.pop(settlement)

    