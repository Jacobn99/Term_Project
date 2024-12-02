from resources import ResourceStack
import numpy as np

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
    
    def __eq__(self,other):
        return isinstance(other, Civilization) and self.id == other.id
    
    def useProduction(self):
        for settlement in self.settlements:
            builder = settlement.builder
            settlement.updateYields()
            # print(settlement.yieldsByType)
            builder.updateProgress()
            # print(builder.getCostRemaining())
            
    def resetYieldsByType(self):
        for key in self.yieldsByType:
            self.yieldsByType[key] = 0

    def getCivilizationTiles(self):
        result = np.array([])
        for settlement in self.settlements:
            result = np.union1d(result, settlement.settlementTiles.flatten())
        return result
    
    def updateAllYields(self):
        self.resetYieldsByType()
        for settlement in self.settlements:
            settlement.harvestResources()
            for type in settlement.yieldsByType:
                # print(key, settlement.yieldsByType[key])
                if type in self.yieldsByType:
                    self.yieldsByType[type] += settlement.yieldsByType[type]

    def addYield(self, stack):
        ResourceStack.addStackToCivilization(stack, self)

    def getYield(self, resourceType):
        if resourceType not in self.yieldsByType: return 0
        else: return self.yieldsByType[resourceType]

    def addSettlement(self, settlement):
        self.settlements.append(settlement)
    
    def removeSettlement(self, settlement):
        self.settlements.remove(settlement)

    