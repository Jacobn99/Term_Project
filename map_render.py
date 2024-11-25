from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from tiles import Tile

class MapRenderer:
    @staticmethod
    def render(map, viewMapLoc, screenSize, spriteDrawer, tileSize):
        Tile.renderedTilesSet = set()
        renderedMap = MapRenderer.getRenderedMap(map, viewMapLoc, screenSize, tileSize)
        renderedRows = len(renderedMap.tileList)
        
        tileWidth, tileHeight = tileSize[0], tileSize[1]
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        startX,startY = MapRenderer.getMapStartLocation(screenSize,tileSize, renderedRows)

        # print((renderedMap.lowerX, renderedMap.upperX), (renderedMap.lowerY, renderedMap.upperY))
        relativeRow = 0
        relativeCol = 0
        for row in range(renderedMap.lowerY, renderedMap.upperY):
            relativeCol = 0
            for col in range(renderedMap.lowerX, renderedMap.upperX):
                tile = map[row,col]
                tileSprite = tile.getSprite()
                
                screenX = (relativeRow - relativeCol) * tileWidth//2;
                screenY = (relativeRow + relativeCol) * tileHeight//2;
                # print(f'map: {(row,col)}, screen: {screenX,screenY}')


                if -tileWidth<=startX + screenX<=screenWidth + tileWidth and -tileHeight<=startY + screenY<=screenHeight + tileHeight:
                    Tile.renderedTilesSet.add((row,col))

                    spriteDrawer.drawSprite(tileSprite, startX + screenX, startY + screenY)
                relativeCol+=1

            relativeRow+=1
    
    def generateRepeatMap(self, sprite, size):
        rows = size[0]
        cols = size[1]
        mapList = []

        tileSprites = (sprite, Tile.defaultSprites['green_tile'])
        i = 0
        for row in range(rows):
            for col in range(cols):
                mapList.append(Tile(self,tileSprites[i%2], row, col))
                i+=1
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
        renderedRows, renderedCols = 8,8

        # renderedRows, renderedCols = MapRenderer.getViewSize(map, screenSize, tileSize)

        xLowerBound = x - renderedCols//2
        yLowerBound = y - renderedRows//2
        xUpperBound = x + renderedCols//2
        yUpperBound = x + renderedRows//2

        xLowerBound = max(0, xLowerBound)
        yLowerBound = max(0, yLowerBound)
        xUpperBound = min(cols, xUpperBound)
        yUpperBound = min(rows, yUpperBound)
        
        # print("renderedSize:", (renderedRows, renderedCols), "bounds:", (xLowerBound, x + renderedCols), (yLowerBound, y + renderedRows))
        renderedMap = Map(map[xLowerBound:xUpperBound, yLowerBound:yUpperBound], 
                          (xLowerBound, xUpperBound, yLowerBound, yUpperBound))
        m[xLowerBound:xUpperBound, yLowerBound: yUpperBound] = 1
        # print(m)
        return renderedMap
    
    @staticmethod
    def getViewSize(map, screenSize, tileSize):
        screenWidth, screenHeight = screenSize
        tileWidth, tileHeight = tileSize
        maxRows, maxCols = len(map), len(map[0])

        desiredRows = screenHeight//tileHeight
        desiredCols = screenWidth//tileWidth

        # print(f'maxRows: {maxRows}, maxCols: {maxCols}, desiredRows: {desiredRows}, desiredCols: {desiredCols}')

        return min(desiredRows,maxRows), min(desiredCols,maxCols)
    
class Map:
    def __init__(self, tileList, range):
        self.tileList = tileList
        self.range = range
        self.lowerX, self.upperX, self.lowerY, self.upperY = range
