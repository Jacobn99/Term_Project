from abc import ABC, abstractmethod
from sprite import Sprite
from PIL import Image


class Builder():
    def __init__(self, settlement):
        self.settlement = settlement
        self.unit = None
        self.costRemaining = 0
        self.productionPerTurn = 10
   
    def updateProgress(self):
        self.costRemaining -= self.productionPerTurn

    def getCostRemaining(self):
        return self.costRemaining

    def setUnit(self, unit):
        self.unit = unit
        self.costRemaining = unit.getProductionCost()
        print('New unit set!')


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

        