from tiles import Tile
from sprite import Sprite
from map_render import Map, MapRenderer
from tile_types import *
from resources import ResourceStack
from buildable_units import Builder
from ui import SettlementUI, CustomLabel

class Settlement():
    def __init__(self, app, tile, civilization, mapRenderer):
        self.app = app
        self.row = tile.row
        self.col = tile.col
        self.sprite = Tile.defaultSprites['brown_tile']
        self.mapRenderer = mapRenderer
        self.civilization = civilization
        self.size = 2
        self.settlementTiles = Settlement.createTileList(self.row, self.col, self.size, self.app.map)
        self.population = 2
        self.harvestedTiles = set()
        self.civilization.addSettlement(self)
        self.builder = Builder(self)
        self.yieldsByType = {ResourceStack.ResourceTypes['production'] : 0, 
                             ResourceStack.ResourceTypes['food'] : 0}
        self.settlementUI = SettlementUI(app, self, app.gameManager)
        self.populationProgress = 0
        self.hp = 150
        self.label = CustomLabel(f'Settlement Attacked! (HP:{self.hp})', 30, (app.width//2, 50), color = 'red', time = 15, bold = True)



    def __repr__(self):
        return f'settlement(row={self.row}, col={self.col})'
    
    def __eq__(self,other):
        return isinstance(other, Settlement) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(str(self))
    
    def displayUI(self):
        self.settlementUI.display(self.app)

    def getYields(self, resourceType):
        if resourceType not in self.yieldsByType: return 0
        else: return self.yieldsByType[resourceType]
    
    def addYield(self, stack):
        ResourceStack.addStackToSettlement(stack,self)

    def placePopulation(self, tile, app, ui = None):
        if tile.civilization == app.players[app.currentPlayerID]:
            if tile not in self.harvestedTiles: 
                if len(self.harvestedTiles) < self.population:
                    ui.label.setText('Population Placed')
                    ui.label.display(app)
                    self.harvestedTiles.add(tile)
                else:
                    ui.label.setText(f'Cant Place Max Population Used')
                    ui.label.display(app)
            else: 
                ui.label.setText('Population Removed')
                self.harvestedTiles.remove(tile)
                ui.label.display(app)

    def updateYields(self):
        self.harvestResources()

    def resetYieldsByType(self):
        for key in self.yieldsByType:
            self.yieldsByType[key] = 0

    def harvestResources(self):
        self.resetYieldsByType()
        for tile in self.harvestedTiles:
            resources = tile.getResources()
            if resources == []: continue
            else: 
                for stack in resources:
                    self.addYield(stack)

        if self.populationProgress >= self.population * 10:
            self.populationProgress = 0
            self.population+=1
        else: self.populationProgress += self.yieldsByType[ResourceStack.ResourceTypes['food']]
            
    def instantiate(self):
        tile = self.app.map.tileList[self.row, self.col]
        tile.setType(SettlementCenter(), self.app)
        for tile in self.getSettlementTiles().flatten():
            tile.civilization = self.civilization
            self.civilization.addSettlement(self)
            tile.settlement = self
            tile.redrawTile(tile, (self.app.currentViewRow, self.app.currentViewCol), self.app.spriteDrawer, 
                            (self.app.width, self.app.height), self.app.map, self.app.mapRenderer)
            
        self.civilization.isSettled = True
        
    def getSettlementTiles(self):
        return self.settlementTiles
    
    def addPopulation(self, number):
        self.population += number

    def updateHP(self,app):
        if self.hp <= 0: self.die(app)
       
    def changeHP(self, dHP, app):
        self.hp += dHP
        self.updateHP(app)
        self.label.setText(f'Settlement Attacked! (HP:{self.hp})')
        self.label.display(app)

    def getHP(self):
        return self.hp
    
    def die(self,app):
        self.civilization.removeSettlement(self, app)
        rows,cols = len(self.settlementTiles), len(self.settlementTiles[0])

        for row in range(rows):
            for col in range(cols):
                tile = self.settlementTiles[row,col]
                tile.settlement = None
            centerTile = app.map.tileList[self.row,self.col]
        centerTile.setType(GrassTile(), app)
    
    @staticmethod
    def colorSettlementTiles(app, settlement):
        for rowList in settlement.getSettlementTiles():
                for tile in rowList:
                    tile.setType(ForestTile(), app)

    @staticmethod
    def createTileList(row, col, size, map):
        rows,cols = len(map.tileList), len(map.tileList[0])
        lowerRow = row - size
        upperRow = row + size + 1
        lowerCol = col - size
        upperCol = col + size + 1
        lowerRow = max(0, lowerRow)
        upperRow = min(rows, upperRow)
        lowerCol = max(0,lowerCol)
        upperCol = min(cols, upperCol)
        settlementTiles = map.tileList[lowerRow:upperRow, lowerCol:upperCol]
        return settlementTiles

    