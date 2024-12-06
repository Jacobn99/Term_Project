from abc import ABC, abstractmethod
from sprite import Sprite
import PIL as pil
from resources import ResourceStack
from ui import *


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
            print(f'costRemaining: {self.costRemaining}')


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
    
    def move(self, app, newLoc):
        oldRow,oldCol = self.location
        tile = self.app.map.tileList[oldRow,oldCol]
        tile.movableUnit = None
        self.location = newLoc
        newTile = app.map.tileList[newLoc[0],newLoc[1]]
        newTile.movableUnit = self
        app.hasMoved.add(self)
        
    @abstractmethod
    def getProductionCost(self):
        pass
    

class Warrior(MovableUnit):
    warriorSprite = Sprite(pil.Image.open("sprites/warrior.png"))
    # in drawUnits, all units in given set will be drawn
    def __init__(self, civilization, app):
        self.civilization = civilization
        self.app = app
        self.location = None
        self.sprite = Warrior.warriorSprite
        self.productionCost = 0
        self.hp = 100
        self.hpLabel = CustomLabel(f'HP:{self.hp}', 20, (app.width//2,app.height//2), color = 'red')
        self.attackDamage = 25

    def getProductionCost(self):
        return self.productionCost

    def instantiate(self, spawnLoc):
        self.location = spawnLoc
        row,col = self.location
        tile = self.app.map.tileList[row, col]
        tile.movableUnit = self
        self.drawUnit()

    def drawUnit(self):
        self.app.drawableUnits.append(self)

    def getLocation(self):
        return self.location
    
    def getTileScreenLocation(self,app):
        row,col = self.location
        tile = app.map.tileList[row,col]
        relativeLoc = tile.getRelativeLoc(tile.row,tile.col,app.map)
        
        return tile.mapToScreenCords(relativeLoc, tile.getSize(), (app.width,app.height), app.map.getRenderedMap(), app.mapRenderer)
    
    def getSprite(self):
        return self.sprite
    
    def displayHP(self, app):
        self.updateHP()
        print('displaying :(')
        self.hpLabel.display(app)

    def hideHPDisplay(self,app):
        print('got here hiding now')
        self.hpLabel.removeAll(app)

    def getHPLabel(self):
        return self.hpLabel

    def updateHP(self):
        if self.hp <= 0: self.die()
        else:
            self.hpLabel.setText(f'HP:{self.hp}')
            self.hpLabel.x, self.hpLabel.y = self.getTileScreenLocation(app) 
    
    def changeHP(self, dHP):
        self.hp += dHP
        self.updateHP()

    def getHP(self):
        return self.hp
    
    def die(self):
        row,col = self.location
        tile = app.map.tileList[row,col]

        self.hpLabel.removeAll()
        self.hpLabel = None
        self.civilization = None
        tile.movableUnit = None
        if self in self.app.drawableUnits: self.app.drawableUnits.remove(self)
        

        