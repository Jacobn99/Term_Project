from abc import ABC, abstractmethod
from sprite import Sprite
from PIL import Image
from resources import ResourceStack


class Builder():
    def __init__(self, settlement):
        self.settlement = settlement
        self.unit = None
        self.costRemaining = 0
        self.productionPerTurn = 0
   
    def updateProgress(self):
        self.updateProductionPerTurn()
        if self.unit != None:
            self.costRemaining -= self.productionPerTurn
            if self.costRemaining <= 0: 
                self.costRemaining = 0
                self.unit.instantiate((self.settlement.row - 1, self.settlement.col))
            print(self.costRemaining)


    def getCostRemaining(self):
        return self.costRemaining
    
    def updateProductionPerTurn(self):
        self.productionPerTurn = self.settlement.yieldsByType[ResourceStack.getResource('production')]

    def setUnit(self, unit):
        self.unit = unit
        self.costRemaining = unit.getProductionCost()
        print(f'New unit under construction! (Cost: {self.costRemaining})')

    def getConstructing(self):
        return self.unit

class BuildableUnit(ABC):
    @abstractmethod
    def getProductionCost(self):
        pass


class MovableUnit(BuildableUnit):
    
    # def move(self, newLoc):
    #     oldRow,oldCol = self.location
    #     oldTile = self.app.map
    @abstractmethod
    def getProductionCost(self):
        pass
    

class Warrior(MovableUnit):
    warriorSprite = Sprite(Image.open("sprites/warrior.png"))
    # in drawUnits, all units in given set will be drawn
    def __init__(self, civilization, app):
        self.civilization = civilization
        self.app = app
        self.location = None
        self.sprite = Warrior.warriorSprite
        self.productionCost = 30

    def getProductionCost(self):
        return self.productionCost

    def instantiate(self, spawnTile):
        self.location = spawnTile
        row,col = self.location
        tile = self.app.map.tileList[row, col]
        tile.movableUnit = self
        self.drawUnit()

    def drawUnit(self):
        self.app.drawableUnits.append(self)

    def getLocation(self):
        return self.location
    
    def getSprite(self):
        return self.sprite
    
    def move(self, newLoc):
        oldRow,oldCol = self.location
        tile = self.app.map.tileList[oldRow,oldCol]
        tile.movableUnit = None
        self.location = newLoc
        newTile = self.app.map.tileList[newLoc[0],newLoc[1]]
        newTile.movableUnit = self
    
    def getSpriteLoc(self):
        # numOfResources = len(resources)
        # tileWidth, tileHeight = self.tile.getSize()
        relativeRow,relativeCol = self.tile.realToRelativeLoc(self.tile.row, self.tile.col, self.app.map,
                                                              self.app.currentViewRow, self.app.currentViewCol)
        
        x,y = self.tile.mapToScreenCords((relativeRow, relativeCol), self.tile.getSize(), 
                                                    (self.app.width, self.app.height), self.app.map.getRenderedMap(), 
                                                    self.app.mapRenderer)
        return x,y

        