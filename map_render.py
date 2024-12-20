import numpy as np
from tiles import Tile
from tile_types import *
import random

class MapRenderer:
    @staticmethod
    def render(map, app, viewMapLoc, screenSize, spriteDrawer, tileSize):
        tileList = map.tileList
        viewMapRow, viewMapCol = viewMapLoc
        renderedMap = MapRenderer.createRenderedMap(map, app, viewMapLoc, screenSize, tileSize)
        map.setRenderedMap(renderedMap)
        renderedRows = len(renderedMap.tileList)
        renderedCols = len(renderedMap.tileList[0])     
        tileWidth, tileHeight = tileSize[0], tileSize[1]
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        startX,startY = MapRenderer.getMapStartLocation(screenSize,tileSize, renderedRows, renderedCols)
        relativeRow = 0
        relativeCol = 0
        m = np.zeros((len(tileList), len(tileList[0])))
        l = []
        renderer = MapRenderer()
        i = 0

        for relativeRow in range(renderedRows):
            for relativeCol in range(renderedCols):
                tile = renderedMap.tileList[relativeRow, relativeCol]
                tileSprite = tile.getSprite()
                l.append(tile)
                screenX,screenY = Tile.mapToScreenCords((relativeRow, relativeCol), tile.getSize(),screenSize, map.renderedMap, renderer)
                
                if -tileWidth<=startX + screenX<=screenWidth + tileWidth and -tileHeight<=startY + screenY<=screenHeight + tileHeight:
                    spriteDrawer.drawSprite(tileSprite, screenX, screenY)
                relativeCol+=1
                i+=1
        a = np.array(l)
        a = a.reshape(renderedRows, renderedCols)
        m[renderedMap.lowerY: renderedMap.upperY, renderedMap.lowerX: renderedMap.upperX] = 1
        return renderedMap
    
    def generateRandomMap(self, app, size):
        typeList = [GrassTile(), ForestTile(), RockTile()]
        rows = size[0]
        cols = size[1]
        mapList = []

        for row in range(rows):
            for col in range(cols):
                rand = random.randrange(len(typeList))
                type = typeList[rand]
                tile = Tile(self,row,col, None)
                mapList.append(tile)
                tile.setType(type, app)

        m = np.array(mapList)
        map = Map(m.reshape(rows,cols), (0, row, 0, cols))

        return map

    def generateRepeatMap(self, size, type, sprite = Tile.defaultSprites['empty']):
        rows = size[0]
        cols = size[1]
        mapList = []

        for row in range(rows):
            for col in range(cols):
                mapList.append(Tile(self,row,col, type, sprite = sprite))

        m = np.array(mapList)
        map = Map(m.reshape(rows,cols), (0, row, 0, cols))

        return map

    @staticmethod
    def getRelativeMapLocation(currentViewRow, currentViewCol, absoluteRow, absoluteCol, map):
        if (map == None): return absoluteRow, absoluteCol
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
        rows,cols = len(tileList), len(tileList[0])

        y, x = viewMapLoc
        renderedRows, renderedCols = app.viewRowSize, app.viewColSize        
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
       
        map.setRenderedMap(renderedMap)
        return renderedMap
    
    @staticmethod
    def getViewSize(map, screenSize, tileSize):
        screenWidth, screenHeight = screenSize
        tileWidth, tileHeight = tileSize
        maxRows, maxCols = len(map), len(map[0])

        desiredRows = screenHeight//tileHeight
        desiredCols = screenWidth//tileWidth

        return min(desiredRows,maxRows), min(desiredCols,maxCols)
    
class Map:
    def __init__(self, tileList, range):
        self.tileList = tileList
        self.range = range
        self.lowerX, self.upperX, self.lowerY, self.upperY = range
        self.renderedMap = None
    
    def setRenderedMap(self, renderedMap):
        self.renderedMap = None
        self.renderedMap = renderedMap

    def getRenderedMap(self):
        return self.renderedMap