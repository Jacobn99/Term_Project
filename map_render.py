from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from tiles import Tile

class MapRenderer:
    @staticmethod
    def render(map, viewMapLoc, screenSize, spriteDrawer, tileSize):
        renderedMap = MapRenderer.getRenderedMap(map, viewMapLoc, screenSize, tileSize)
        renderedRows = len(renderedMap.tileList)
        
        tileWidth, tileHeight = tileSize[0], tileSize[1]
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        startX,startY = MapRenderer.getMapStartLocation(screenSize,tileSize, renderedRows)

        for row in range(renderedMap.lowerY, renderedMap.upperY):
            for col in range(renderedMap.lowerX, renderedMap.upperX):
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
        return startX,startY
    
    @staticmethod
    def getRenderedMap(map, viewMapLoc, screenSize, tileSize):
        m = np.zeros((len(map), len(map[0])))
        rows,cols = len(map), len(map[0])

        x, y = viewMapLoc
        renderedRows, renderedCols = MapRenderer.getViewSize(map, screenSize, tileSize)

        xLowerBound = x - renderedCols
        yLowerBound = y - renderedRows
        xUpperBound = x + renderedCols
        yUpperBound = x + renderedRows

        xLowerBound = max(0, xLowerBound)
        yLowerBound = max(0, yLowerBound)
        xUpperBound = min(cols, xUpperBound)
        yUpperBound = min(rows, yUpperBound)
        
        print(m[xLowerBound:x + renderedCols, yLowerBound: y + renderedRows])
        print("renderedSize:", (renderedRows, renderedCols), "bounds:", (xLowerBound, x + renderedCols), (yLowerBound, y + renderedRows))
        renderedMap = Map(map[xLowerBound:xUpperBound, yLowerBound: yUpperBound], 
                          (xLowerBound, xUpperBound, yLowerBound, yUpperBound))
        m[xLowerBound:xUpperBound, yLowerBound: yUpperBound] = 1
        print(m)
        return renderedMap
    
    @staticmethod 
    def getViewSize(screenSize, tileSize):
        tileWidth, tileHeight = tileSize
        screenWidth, screenHeight = screenSize
        rows = screenWidth//tileHeight
        cols = screenHeight//tileWidth
        return rows,cols
    
    @staticmethod
    def getViewSize(map, screenSize, tileSize):
        screenWidth, screenHeight = screenSize
        tileWidth, tileHeight = tileSize
        maxRows, maxCols = len(map), len(map[0])
        print(screenSize, tileSize, maxRows, maxCols)
        
        desiredRows = screenHeight//tileHeight
        desiredCols = screenWidth//tileWidth

        return min(desiredRows,maxRows), min(desiredCols,maxCols)
    
class Map:
    def __init__(self, tileList, range):
        self.tileList = tileList
        self.range = range
        self.lowerX, self.upperX, self.lowerY, self.upperY = range
