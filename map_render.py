from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from tiles import Tile

class MapRenderer:
    @staticmethod
    def render(map, screenSize, spriteDrawer, tileSize):
        rows, cols = len(map), len(map[0])
        tileWidth, tileHeight = tileSize[0], tileSize[1]

        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        startX,startY = MapRenderer.getMapStartLocation(screenSize,tileSize, rows)

        for row in range(rows):
            for col in range(cols):
                tile = map[row,col].getSprite()

                screenX = (row - col) * tileWidth//2;
                screenY = (row + col) * tileHeight//2;

                if -tileWidth<=startX + screenX<=screenWidth + tileWidth and -tileHeight<=startY + screenY<=screenHeight + tileHeight:
                    spriteDrawer.drawSprite(tile, startX + screenX, startY + screenY)
    
    def generateRepeatMap(self, sprite, size):
        rows = size[0]
        cols = size[1]
        mapList = []

        for row in range(rows):
            for col in range(cols):
                mapList.append(Tile(self,sprite, row, col))
        map = np.array(mapList)
        map = map.reshape(rows,cols)

        mapList = None
        return map
    
    @staticmethod
    def getMapStartLocation(screenSize, tileSize, mapRows):
        tileWidth, tileHeight = tileSize

        screenWidth, screenHeight = screenSize

        middleX = screenWidth//2
        middleY = screenHeight//2

        xEdgeTilesToCenter = middleX//tileWidth

        # Adding/subtracting tileWidth//2 and tileHeight//2 because program draws tiles from edge, not center
        startX = middleX-((xEdgeTilesToCenter//2)*tileWidth) + tileWidth//2

        startY = middleY-((mapRows//2)*tileHeight) - tileHeight//2
        # assert(startY >=0)

        return startX,startY