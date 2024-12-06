from map_render import *
from resources import ResourceStack
import math
import random
from tile_types import *

class GameManager:

    def __init__(self):
        self.tileTypes = {'forest_tile' : ForestTile(), 'grass_tile' : GrassTile(), 'rock_tile' : RockTile(), 
                     'settlement_center' : SettlementCenter()}


    def startGame(self, app):
        startLocs = []
        for _ in range(len(app.players)):
            startLocs.append(self.createRandomSpawnLocation(app))

        app.map = MapRenderer.generateRandomMap(app.mapRenderer, app, (app.mapRows,app.mapCols))
        # app.map.tileList[0,0].changeSprite(Tile.defaultSprites['green_tile'],app)
        app.currentViewRow, app.currentViewCol = startLocs[0]
        app.rendereredMap = MapRenderer.render(app.map, app, (app.currentViewRow,app.currentViewCol), 
                                               (app.width,app.height), app.spriteDrawer, (app.tileWidth,app.tileHeight))
        
        self.initializeCivilizations(app, startLocs)

    def getAllTileTypes(self):
        return self.tileTypes
    
    def getTileType(self, typeStr):
        return self.tileTypes[typeStr]
    
    def removeAllUI(app):
        while len(app.renderedUI) > 0:
            app.renderedUI[0].remove(app)

    def initializeCivilizations(self, app, startLocs):
        for i in range(len(app.players)):
            player = app.players[i]
            startLoc = startLocs[i]
            player.setSpawnLocation(startLoc)
    
    def createRandomSpawnLocation(self, app):
        mapRows, mapCols = (app.mapRows, app.mapCols)

        randRow = random.randrange(mapRows)
        randCol = random.randrange(mapCols)

        return randRow, randCol

    def endPlayerTurn(self, app):
        if app.currentPlayerID >= len(app.players) - 1:
            app.currentPlayerID = 0
            self.takeNextTurn(app)
            print('Next Turn')
        else: 
            app.currentPlayerID +=1

        print('Player Turn Ended')

        # print(app.players[app.currentPlayerID])
        # if len(app.players[app.currentPlayerID].settlements) > 0:
        #     print(f'PlayerID: {app.currentPlayerID}, harvestedTile: {app.players[app.currentPlayerID].settlements[0].harvestedTiles}')
        self.changePlayer(app, app.players[app.currentPlayerID])

    def takeNextTurn(self, app):
        for civilization in app.players:
            civilization.updateAllYields()        
        # print(f"Civilization - production:{app.players[0].yieldsByType[ResourceStack.ResourceTypes['production']]}, \
        #         food: {app.players[0].yieldsByType[ResourceStack.ResourceTypes['food']]}")
        for player in app.players:
            player.useProduction()

    def changePlayer(self, app, civilization):
        app.currentViewRow = civilization.startRow
        app.currentViewCol = civilization.startCol
        
        app.currentViewRow += 1
        self.clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, (app.tileWidth,app.tileHeight))
        app.hasMoved = set()

    def clearScreen(self, app):
        app.img = self.loadScreen(app, None)

    def loadScreen(self, app, img):
        if img == None:
            img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
        img.save(f'{app.imgName}.jpg')

        return img
    
    def getTile(self, app, mouseX, mouseY, screenSize, map, onlyRendered = False):
        if map == None: return None
        if map.tileList.size == 0: return None

        loc = self.getRelativeTile(mouseX, mouseY, screenSize, map)
        if loc == None: return None
        row, col = loc

        renderedMap = map.getRenderedMap()
        if renderedMap == None: renderedMap = map

        relativeRow,relativeCol = self.getRelativeTile(mouseX, mouseY, screenSize, map)

        if 0<=relativeRow<len(renderedMap.tileList) and 0 <= relativeCol < len(renderedMap.tileList[0]):
            tile = renderedMap.tileList[relativeRow, relativeCol]
            return tile.row, tile.col

        else: return None

    def getRelativeTile(self, mouseX, mouseY, screenSize, map):
        if map == None: return None
        if map.tileList.size == 0: return None
        else:
            renderedMap = map.getRenderedMap()
            if renderedMap == None: renderedMap = map
            tile0 = map.tileList[0,0]
            tileWidth, tileHeight = tile0.getSize()

            startX,startY = MapRenderer.getMapStartLocation(screenSize, tile0.getSize(), len(renderedMap.tileList), len(renderedMap.tileList[0]))

            startX += tileWidth
            startY -= (-1 * tileHeight)//2
            row = math.floor((mouseX - startX)/tileWidth + (mouseY - startY)/tileHeight) + 1
            col = math.floor((mouseY - startY)/tileHeight - (mouseX - startX)/tileWidth)

            x = col
            y = row
        
            return x,y