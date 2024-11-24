from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite

class MapRenderer:
    # TO-DO: Add map 2d list with data on the tiles
    @staticmethod
    def render(map, screenSize, spriteDrawer, tileSize):
        # rows, cols = mapSize
        rows, cols = len(map), len(map[0])
        tileWidth, tileHeight = tileSize[0], tileSize[1]

        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        middleX = screenWidth//2
        middleY = screenHeight//2

        xEdgeTilesToCenter = middleX//tileWidth

        # Adding/subtracting tileWidth//2 and tileHeight//2 because program draws tiles from edge, not center
        startX = middleX-((xEdgeTilesToCenter//2)*tileWidth) + tileWidth//2

        startY = middleY-((rows//2)*tileHeight) - tileHeight//2

        for row in range(rows):
            # if row*tileHeight>= screenHeight: continue
            for col in range(cols):
                tile = map[row,col].getSprite()

                screenX = (row - col) * tileWidth//2;
                screenY = (row + col) * tileHeight//2;
                if -tileWidth<=startX + screenX<=screenWidth + tileWidth and -tileHeight<=startY + screenY<=screenHeight + tileHeight:
                    spriteDrawer.drawSprite(tile, startX + screenX, startY + screenY)
    
    @staticmethod
    def generateRepeatMap(tile, size):
        rows = size[0]
        cols = size[1]
        map = np.repeat(tile, rows*cols)
        map = map.reshape(rows,cols)
        return map


class Tile:
    # Making references to default tileSprites so that they are cached unless they are modified
    defaultSprites = {'empty' : Sprite(Image.open("sprites/TileShape.png"))}
    defaultBorderColor = [0,0,0,0]

    def __init__(self, sprite):
        self.sprite = sprite

    # Changes sprite without making an alias
    def changeSprite(self, newSprite):
        self.sprite = newSprite

    def getSprite(self):
        return self.sprite
    
    def getSize(self):
        print(self.sprite.getSize())
        return self.sprite.getSize()
    
    @staticmethod
    def changeTileBorder(tile, borderColor):
        borderData = Tile.getSpriteByName('empty').getData().copy()
        newSpriteData = tile.getSprite().getData().copy()

        rows, cols = len(borderData), len(borderData[0])

        for row in range(rows):
            for col in range(cols):
                if borderData[row,col].tolist()[:3] == Tile.defaultBorderColor[:3]:
                    # print(newSpriteData[row,col], borderColor + [int(newSpriteData[row,col][-1])])
                    newSpriteData[row,col] = borderColor + [int(newSpriteData[row,col][-1])]

        tile.changeSprite(Sprite(Image.fromarray(newSpriteData, mode = "RGB")))
        
    @staticmethod
    def getSpriteByName(name):
        if name in Tile.defaultSprites:
            return Tile.defaultSprites[name]
        else: return None

