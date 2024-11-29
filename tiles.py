from PIL import Image
import numpy as np
from sprite import Sprite

class Tile():
    # Making references to default tileSprites so that they are cached unless they are modified
    tileShape = Image.open("sprites/TileShape.png")
    greenTile = Image.open("sprites/green_tile.png")
    defaultSprites = {'empty' : Sprite(tileShape), 'green_tile': Sprite(greenTile)}
    defaultBorderColor = [0,0,0]
    highlightColor = [255,0,0]

    def __init__(self, mapRenderer,sprite, row, col):
        self.sprite = sprite
        self.mapRenderer = mapRenderer
        self.col = col # col in map
        self.row = row # row in map
        self.isHighlighted = False

    def __repr__(self):
        return f'Tile(row:{self.row},col:{self.col})'
    
    def __eq__(self,other):
        return isinstance(other, Tile) and self.col == other.col and self.row == other.row

    # Changes sprite without making an alias
    def changeSprite(self, newSprite):
        self.sprite = newSprite

    def getSprite(self):
        return self.sprite
    
    def getSize(self):
        return self.sprite.getSize()
    
    @staticmethod
    def changeTileBorder(tile, borderColor):
        borderData = Tile.getSpriteByName('empty').getData()
        newSpriteData = tile.getSprite().getData()
        rows, cols = len(borderData), len(borderData[0])

        for row in range(rows):
            for col in range(cols):
                if borderData[row,col].tolist()[:3] == Tile.defaultBorderColor[:3]:
                    newSpriteData[row,col] = borderColor


        img = Image.fromarray(newSpriteData, mode = "RGB")
        tile.changeSprite(Sprite(img))
        
    @staticmethod
    def getSpriteByName(name):
        if name in Tile.defaultSprites:
            return Tile.defaultSprites[name]
        else: return None

    @staticmethod
    def redrawTile(tile, viewMapLoc, spriteDrawer, screenSize, map, mapRenderer):
        currentViewMapRow, currentViewMapCol = viewMapLoc
        # relativeRow,relativeCol = mapRenderer.getRelativeMapLocation(currentViewMapRow, currentViewMapCol, tile.row, tile.col, map)
        relativeRow = tile.row - currentViewMapRow
        relativeCol = tile.col - currentViewMapCol
        # print(f'absRow: {tile.row}, absCol: {tile.col}, relativeRow: {relativeRow}, relativeCol: {relativeCol}')

        screenX, screenY = Tile.mapToScreenCords((relativeRow, relativeCol), tile.getSize(),screenSize, map.renderedMap, mapRenderer)
        spriteDrawer.drawSprite(tile.getSprite(), screenX, screenY)

    @staticmethod
    def mapToScreenCords(tileMapLoc, tileSize, screenSize, renderedMap, mapRenderer):
        tileWidthHalf = tileSize[0]/2
        tileHeightHalf = tileSize[1]/2
        mapRow,mapCol = tileMapLoc
        startX, startY = mapRenderer.getMapStartLocation(screenSize, tileSize, len(renderedMap.tileList), len(renderedMap.tileList[0]))
        screenX = (mapCol - mapRow) * tileWidthHalf+ startX
        screenY = (mapCol + mapRow) * tileHeightHalf + startY
        # screenX = (mapCol/tileWidthHalf + mapRow/tileHeightHalf)//2
        # screenY = ((mapRow/tileHeightHalf) - (mapCol/tileWidthHalf))//2;

        return screenX, screenY
    
    @staticmethod
    def changeHighlight(tile, viewMapLoc, map, mapRenderer, screenSize, spriteDrawer):
        color = []
        if tile.isHighlighted: color = Tile.defaultBorderColor
        else: color = Tile.highlightColor    

        tile.isHighlighted = not tile.isHighlighted
        Tile.changeTileBorder(tile, color)
        Tile.redrawTile(tile, viewMapLoc, spriteDrawer, screenSize, map, mapRenderer)