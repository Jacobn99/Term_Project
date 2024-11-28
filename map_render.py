from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from tiles import Tile

class MapRenderer:
    @staticmethod
    def render(map, app, viewMapLoc, screenSize, spriteDrawer, tileSize):
        tileList = map.tileList
        renderedMap = MapRenderer.createRenderedMap(map, app, viewMapLoc, screenSize, tileSize)
        renderedRows = len(renderedMap.tileList)
        renderedCols = len(renderedMap.tileList[0])
        
        tileWidth, tileHeight = tileSize[0], tileSize[1]
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        startX,startY = MapRenderer.getMapStartLocation(screenSize,tileSize, renderedRows, renderedCols)
        print(startX,startY)

        relativeRow = 0
        relativeCol = 0
        m = np.zeros((len(tileList), len(tileList[0])))

        print("upperY-lowerY:", renderedMap.upperY - renderedMap.lowerY)
        print("upperX-lowerX:", renderedMap.upperX - renderedMap.lowerX)

        # --------- this code still breaks things ---------
        for relativeRow in range(len(renderedMap.tileList)):
            for relativeCol in range(len(renderedMap.tileList[0])):
                realRow = relativeRow + renderedMap.lowerY
                realCol = relativeCol + renderedMap.lowerX
                tile = tileList[realRow,realCol]
                tileSprite = tile.getSprite()
                
                screenX = (relativeRow - relativeCol) * tileWidth//2;
                screenY = (relativeRow + relativeCol) * tileHeight//2;

                if -tileWidth<=startX + screenX<=screenWidth + tileWidth and -tileHeight<=startY + screenY<=screenHeight + tileHeight:
                    spriteDrawer.drawSprite(tileSprite, startX + screenX, startY + screenY)
                relativeCol+=1

        # for row in range(renderedMap.lowerY, renderedMap.upperY):
        #     relativeCol = 0
        #     for col in range(renderedMap.lowerX, renderedMap.upperX):
        #         tile = tileList[row,col]
        #         tileSprite = tile.getSprite()
                
        #         screenX = (relativeRow - relativeCol) * tileWidth//2;
        #         screenY = (relativeRow + relativeCol) * tileHeight//2;

        #         if -tileWidth<=startX + screenX<=screenWidth + tileWidth and -tileHeight<=startY + screenY<=screenHeight + tileHeight:
        #             spriteDrawer.drawSprite(tileSprite, startX + screenX, startY + screenY)
        #         relativeCol+=1
        #     relativeRow+=1
        m[renderedMap.lowerY: renderedMap.upperY, renderedMap.lowerX: renderedMap.upperX] = 1
        # print(m)
        # print(map.to1DList() in renderedMap.to1DList())
        return renderedMap
    
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
        m = np.array(mapList)
        map = Map(m.reshape(rows,cols), (0, row, 0, cols))

        return map


    @staticmethod
    def getRelativeMapLocation(currentViewRow, currentViewCol, absoluteRow, absoluteCol, map):
        if (map == None): return absoluteRow, absoluteCol
        rows, cols = len(map.tileList), len(map.tileList[0])
        # viewColDistanceFromCenter = (currentViewCol - cols//2)
        # viewRowDistanceFromCenter = (currentViewRow - rows//2)

        # print(absoluteRow - currentViewRow, absoluteCol - currentViewCol)
        return (absoluteRow -  currentViewRow, absoluteCol - currentViewCol)

    @staticmethod
    def getMapStartLocation(screenSize, tileSize, mapRows, mapCols):
        tileWidth, tileHeight = tileSize

        screenWidth, screenHeight = screenSize

        middleX = screenWidth//2
        middleY = screenHeight//2

        xEdgeTilesToCenter = middleX//tileWidth

        # Adding/subtracting til1eWidth//2 and tileHeight//2 because program draws tiles from edge, not center
        startX = middleX-((xEdgeTilesToCenter//2)*tileWidth) + tileWidth//2
        startY = middleY-((mapRows//2)*tileHeight) - tileHeight//2

        return startX,startY
    
    @staticmethod
    def createRenderedMap(map, app, viewMapLoc, screenSize, tileSize):
        tileList = map.tileList
        # m = np.zeros((len(tileList), len(tileList[0])))
        rows,cols = len(tileList), len(tileList[0])

        x, y = viewMapLoc
        renderedRows, renderedCols = app.viewRowSize, app.viewColSize

        # renderedRows, renderedCols = MapRenderer.getViewSize(map, screenSize, tileSize)
        
        xLowerBound = x - renderedCols//2
        yLowerBound = y - renderedRows//2
        xUpperBound = x + renderedCols//2
        yUpperBound = y + renderedRows//2

        xLowerBound = max(0, xLowerBound)
        yLowerBound = max(0, yLowerBound)
        xUpperBound = min(cols, xUpperBound)
        yUpperBound = min(rows, yUpperBound)
        
        renderedMap = Map(tileList[yLowerBound:yUpperBound, xLowerBound:xUpperBound], 
                          (xLowerBound, xUpperBound, yLowerBound, yUpperBound))
        print("bounds:", (xLowerBound, xUpperBound), (yLowerBound, yUpperBound))
        print(renderedMap.tileList[:,0])
        print(f'rows: {len(renderedMap.tileList)}, cols: {len(renderedMap.tileList[0])}')

        # m[xLowerBound:xUpperBound, yLowerBound: yUpperBound] = 1
        map.setRenderedMap(renderedMap)
        # print(renderedMap.tileList)
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
        self.renderedMap = None
    
    def setRenderedMap(self, renderedMap):
        self.renderedMap = renderedMap

    def getRenderedMap(self):
        return self.renderedMap
    
    # def inBounds(self, row, col):
    #     return self.lowerY<=row<self.upperY and self.lowerX<=col<self.upperX
    
    # def to1DList(self):
    #     return self.tileList.reshape(1, len(self.tileList) * len(self.tileList[0]))
