from tiles import Tile
from sprite import Sprite
from map_render import Map, MapRenderer
from tile_types import *

class Settlement():
    def __init__(self, app, tile, mapRenderer):
        self.app = app
        self.row = tile.row
        self.col = tile.col
        self.sprite = Tile.defaultSprites['brown_tile']
        self.mapRenderer = mapRenderer
        self.size = 2
        self.settlementTiles = Settlement.createTileList(self.row, self.col, self.size, self.app.map)
        self.population = 2

    def __repr__(self):
        return f'settlement(row={self.row}, col={self.col})'
    
    def __eq__(self,other):
        return isinstance(other, Settlement) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(str(self))
    
    def instantiate(self):
        tile = self.app.map.tileList[self.row, self.col]
        Settlement.colorSettlementTiles(self.app, self)
        tile.setType(SettlementCenter(), self.app)
        # tile.changeSprite(Tile.defaultSprites['brown_tile'])
        tile.redrawTile(tile, (self.app.currentViewRow,self.app.currentViewCol), self.app.spriteDrawer, 
                        (self.app.width, self.app.height), self.app.map, self.app.mapRenderer)
        
    def getSettlementTiles(self):
        return self.settlementTiles
    
    def addPopulation(self, number):
        self.population += number
    
    @staticmethod
    def colorSettlementTiles(app, settlement):
        for rowList in settlement.getSettlementTiles():
                for tile in rowList:
                    tile.setType(ForestTile(), app)
                    # tile.changeSprite(Tile.defaultSprites['green_tile'])
                    tile.redrawTile(tile, (app.currentViewRow, app.currentViewCol), app.spriteDrawer, 
                            (app.width, app.height), app.map, app.mapRenderer)

    @staticmethod
    def createTileList(row, col, size, map):
        rows,cols = len(map.tileList), len(map.tileList[0])
        lowerRow = row - size
        upperRow = row + size + 1
        lowerCol = col - size
        upperCol = col + size + 1

        print(f'row + size: {row + size}')
        print(min(rows, row + size))

        lowerRow = max(0, lowerRow)
        upperRow = min(rows, upperRow)
        lowerCol = max(0,lowerCol)
        upperCol = min(cols, upperCol)


        print(lowerRow,upperRow, lowerCol, upperCol)

        settlementTiles = map.tileList[lowerRow:upperRow, lowerCol:upperCol]
        return settlementTiles

    