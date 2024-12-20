from resources import ResourceStack
import numpy as np
from settlement import Settlement

class Civilization:
    id = -1
    def __init__(self):
        self.isSettled = False
        self.settlements = []
        self.yieldsByType = {ResourceStack.ResourceTypes['production'] : 0, 
                             ResourceStack.ResourceTypes['food'] : 0}
        self.id = Civilization.id
        self.startRow = None
        self.startCol = None
        Civilization.id+=1

    def __repr__(self):
        return f'civilization(id={Civilization.id})'
    
    def __eq__(self,other):
        return isinstance(other, Civilization) and self.id == other.id
    
    def setSpawnLocation(self, spawnLoc):
        self.startRow, self.startCol = spawnLoc
    
    def useProduction(self):
        for settlement in self.settlements:
            self.isSettled = True
            builder = settlement.builder
            settlement.updateYields()
            builder.updateProgress()
            
    def resetYieldsByType(self):
        for key in self.yieldsByType:
            self.yieldsByType[key] = 0

    def getCivilizationTiles(self):
        result = np.array([])
        for settlement in self.settlements:
            result = np.union1d(result, settlement.settlementTiles.flatten())
        return result
    
    def createSettlement(self, tile, app):
        settlement = Settlement(app, tile, self, app.mapRenderer)
        settlement.instantiate()

    def updateAllYields(self):
        self.resetYieldsByType()
        for settlement in self.settlements:
            settlement.harvestResources()
            for type in settlement.yieldsByType:
                if type in self.yieldsByType:
                    self.yieldsByType[type] += settlement.yieldsByType[type]

    def addYield(self, stack):
        ResourceStack.addStackToCivilization(stack, self)

    def getYield(self, resourceType):
        if resourceType not in self.yieldsByType: return 0
        else: return self.yieldsByType[resourceType]

    def addSettlement(self, settlement):
        self.settled = True
        if settlement not in self.settlements: self.settlements.append(settlement)
    
    def removeSettlement(self, settlement, app):
        self.settlements.remove(settlement)
        if len(self.settlements) <= 0: 
            app.win = True

    