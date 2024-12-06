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
                self.unit = None
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
        if self not in app.hasMoved:
            oldRow,oldCol = self.location
            tile = self.app.map.tileList[oldRow,oldCol]
            tile.movableUnit = None
            self.setLocation(newLoc)
            newTile = app.map.tileList[newLoc[0],newLoc[1]]
            newTile.movableUnit = self

            app.hasMoved.add(self)
            print('moving')

    
    def getProductionCost(self):
        return self.productionCost

    def instantiate(self, spawnLoc):
        self.setLocation(spawnLoc)
        row,col = self.location
        tile = self.app.map.tileList[row, col]
        tile.movableUnit = self
        self.drawUnit()

    def setLocation(self, newLoc):
        self.location = newLoc

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
        self.updateHP(app)
        self.getHPLabel().display(app)

    def hideHPDisplay(self,app):
        self.getHPLabel().removeAll(app)

    def getHPLabel(self):
        return self.hpLabel
        
    def updateHP(self,app):
        if self.hp <= 0: self.die(app)
        else:
            self.hpLabel.setText(f'HP:{self.hp}')
            self.hpLabel.x, self.hpLabel.y = self.getTileScreenLocation(app) 
    
    def changeHP(self, dHP, app):
        self.hp += dHP
        self.updateHP(app)

    def getHP(self):
        return self.hp
    
    def die(self,app):
        row,col = self.location
        tile = app.map.tileList[row,col]

        self.hpLabel.removeAll(app)
        self.hpLabel = None
        self.civilization = None
        tile.movableUnit = None
        if self in self.app.drawableUnits: self.app.drawableUnits.remove(self)
        self.isAlive = False

    @abstractmethod
    def getType(self):
        pass
    

class Warrior(MovableUnit):
    warriorSprite = Sprite(pil.Image.open("sprites/warrior.png"))
    # in drawUnits, all units in given set will be drawn
    def __init__(self, civilization, app):
        self.civilization = civilization
        self.app = app
        self.location = None
        self.sprite = Warrior.warriorSprite
        self.productionCost = 5
        self.hp = 100
        self.hpLabel = CustomLabel(f'HP:{self.hp}', 20, (app.width//2,app.height//2), color = 'red')
        self.attackDamage = 35
        self.isAlive = True
        self.isOffensive = True
        self.type = Warrior

    def attack(self, otherUnit):
        if self not in self.app.hasMoved:
            otherUnit.changeHP(-self.app.lastClickedUnit.attackDamage, app)
            self.app.hasMoved.add(self)
    
    def getType(self):
        return self.type

class Spearman(MovableUnit):
    spearmanSprite = Sprite(pil.Image.open("sprites/Spearman.png"))
    # in drawUnits, all units in given set will be drawn
    def __init__(self, civilization, app):
        self.civilization = civilization
        self.app = app
        self.location = None
        self.sprite = Spearman.spearmanSprite
        self.productionCost = 15
        self.hp = 100
        self.hpLabel = CustomLabel(f'HP:{self.hp}', 20, (app.width//2,app.height//2), color = 'red')
        self.attackDamage = 50
        self.isAlive = True
        self.isOffensive = True
        self.type = Spearman

    def attack(self, otherUnit):
        if self not in self.app.hasMoved:
            otherUnit.changeHP(-self.app.lastClickedUnit.attackDamage, app)
            self.app.hasMoved.add(self)
    
    def getType(self):
        return self.type


class Settler(MovableUnit):
    settlerSprite = Sprite(pil.Image.open("sprites/settler.png"))
    # in drawUnits, all units in given set will be drawn
    def __init__(self, civilization, app):
        self.civilization = civilization
        self.app = app
        self.location = None
        self.sprite = Settler.settlerSprite
        self.productionCost = 15
        self.hp = 10
        self.hpLabel = CustomLabel(f'HP:{self.hp}', 20, (app.width//2,app.height//2), color = 'red')
        self.isAlive = True
        self.isOffensive = False
        self.attackDamage = 0
        self.settlementButton = None
        self.type = Settler

    def getSettlementButton(self):
        if self.settlementButton == None:
            self.settlementButton = SettlementButton(self.app.gameManager, self.location, (200,100), 'gray', None, self, 'Settle?', 20)
        return self.settlementButton

    def displaySettlementButton(self):
        self.settlementButton.display(app)

    def hideSettlementButton(self):
        self.getHPLabel().removeAll(app)

    def getType(self):
        return self.type

    def createSettlement(self):
        tile = self.app.map.tileList[self.location[0],self.location[1]]
        self.civilization.createSettlement(tile,self.app)
        self.die(self.app)