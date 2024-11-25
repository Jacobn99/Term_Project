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

    def __init__(self, mapRenderer,sprite, x, y):
        self.sprite = sprite
        self.mapRenderer = mapRenderer
        self.x = x # col in map
        self.y = y # row in map
        self.isHighlighted = False

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
    def redrawTile(tile, spriteDrawer, screenSize, map, mapRenderer):
        screenX, screenY = Tile.mapToScreenCords((tile.x, tile.y), tile.getSize(),screenSize, map, mapRenderer)
        spriteDrawer.drawSprite(tile.getSprite(), screenX, screenY)

    @staticmethod
    def mapToScreenCords(tileMapLoc, tileSize, screenSize, map, mapRenderer):
        tileWidth = tileSize[0]
        tileHeight = tileSize[1]
        mapX,mapY = tileMapLoc
        startX, startY = mapRenderer.getMapStartLocation(screenSize, tileSize, len(map))
        screenX = (mapX - mapY) * tileWidth//2 + startX
        screenY = (mapX + mapY) * tileHeight//2 + startY

        return screenX, screenY
    
    @staticmethod
    def changeHighlight(tile, map, mapRenderer, screenSize, spriteDrawer):
        color = []
        if tile.isHighlighted: color = Tile.defaultBorderColor
        else: color = Tile.highlightColor    

        tile.isHighlighted = not tile.isHighlighted
        Tile.changeTileBorder(tile, color)
        Tile.redrawTile(tile, spriteDrawer, screenSize, map, mapRenderer)
