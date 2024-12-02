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
                #self.unit.instantiate()
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

    # def getQueue(self):
    #     pass

    # def lowerCost(self, productionAmount):
    #     pass

    # def setCost(self, cost):
    #     pass

class BuildableUnit(ABC):
    @abstractmethod
    def getProductionCost(self):
        pass


class MovableUnit(BuildableUnit):
    @abstractmethod
    def getLocation(self):
        pass
    
    @abstractmethod
    def move(self, newTile):
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
        self.drawUnit(self)

    def drawUnit(self):
        self.app.drawableUnits.append(self)

    def getLocation(self):
        return self.location
    
    def move(self, newTile):
        pass
    
    # def getSpriteLoc(self):
    #     result = []
    #     resources = self.getResources()
    #     numOfResources = len(resources)
    #     tileWidth, tileHeight = self.tile.getSize()
    #     relativeRow,relativeCol = self.tile.realToRelativeLoc(self.tile.row, self.tile.col, self.app.map,
    #                                                           self.app.currentViewRow, self.app.currentViewCol)
        
    #     centerX,y = self.tile.mapToScreenCords((relativeRow, relativeCol), self.tile.getSize(), 
    #                                                 (self.app.width, self.app.height), self.app.map.getRenderedMap(), 
    #                                                 self.app.mapRenderer)
    #     centerX = centerX + tileWidth//2 - self.imgSize[0]//2
    #     y = y + tileHeight//2 - 1*self.imgSize[1]//4

    #     for i in range(numOfResources):
    #         correction = i * ResourceIcon.ImgSpacing - (ResourceIcon.ImgSpacing * (numOfResources))//4
    #         result.append((centerX + correction, y))

    #     return result

        