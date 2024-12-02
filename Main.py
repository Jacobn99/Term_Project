from typing import List
from cmu_graphics import *
from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from map_render import MapRenderer, Map
from settlement import Settlement
from player_civilization import Civilization
from tiles import Tile
import math
from resources import ResourceIcon, ResourceStack
from buildable_units import *


# Go in numpy and make it so only the part of the map you can see if being rendered at one time 
# (edit the map being used with numpy to include only what you can see)

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.counter = 0
    app.imageColor = (255,255,255)
    app.imgName = "screen"
    app.img = loadScreen(app, None)
    app.colors = [(100,0,0), (0,100,0), (0,0,100)]
    app.map = None
    app.mapRows = 30
    app.mapCols = 30
    app.prevHoveredTileLoc = None
    app.mapRenderer = MapRenderer()
    app.currentViewCol = None # From top left corner
    app.currentViewRow = None # From top left corner
    app.renderedMap = None
    app.viewRowSize = 8
    app.viewColSize = 8

    app.ignorableColor = (255,255,255)
    app.tileImage = Image.open("sprites/TileShape.png")
    app.spriteDrawer = SpriteDrawer(app, (app.width,app.height), app.imgName)
    app.currentTile = None
    app.resourceIcons = set()
    app.tileSize = (100,50)
    app.isMoving = False
    app.drawableUnits = []
    app.prevClickTile = None

    app.players = [Civilization()]

def redrawAll(app):
    drawImage("screen.jpg", 0, 0)
    drawUnits(app)

    drawResourceIcons(app)


def drawUnits(app):
    for unit in app.drawableUnits:
        width, height = app.tileSize
        realLocation = unit.getLocation()
        relativeMapLocation = Tile.getRelativeLoc(realLocation[0], realLocation[1], app.map)
        renderedMap = app.map.getRenderedMap()
        if relativeMapLocation != None and renderedMap != None:
            sprite = unit.getSprite() 
            spriteSize = sprite.getSize()
            row, col = relativeMapLocation
            x,y = Tile.mapToScreenCords((row,col), app.tileSize, (app.width,app.height), renderedMap, app.mapRenderer)
            drawImage(sprite.getFileName(), x + width//2 - spriteSize[0]//2,y + height//2 - (2*spriteSize[1])//3)

def drawResourceIcons(app):
    for icon in app.resourceIcons:
        i = 0
        imageLocs = icon.getImageLocs()
        if imageLocs == None: continue
        for loc in imageLocs:
            imgX, imgY = loc
            drawImage(icon.getResources()[i].getType().getImagePath(), imgX, imgY)
            i+=1

        i = 0
        for loc in icon.getLabelLocs(imageLocs):
            drawLabel(icon.getResources()[i].getAmount(), loc[0], loc[1])
            i+=1
                
def onMouseMove(app, mouseX,mouseY):
    mapLoc = getTile(app, mouseX, mouseY, (app.width,app.height), app.map, True)

    if mapLoc != app.prevHoveredTileLoc and app.prevHoveredTileLoc != None: 
        prevRow, prevCol = app.prevHoveredTileLoc
        Tile.changeHighlight(app.map.tileList[prevRow, prevCol], (app.currentViewRow, app.currentViewCol), 
                             app.map, app.mapRenderer, (app.width,app.height), app.spriteDrawer)
        app.prevHoveredTileLoc = None
    if mapLoc != None and mapLoc != app.prevHoveredTileLoc:
        row, col = mapLoc
        app.currentTile = (row,col)
        app.prevHoveredTileLoc = (row,col)
        t = app.map.tileList[row,col]
        print(t, (t.row,t.col))
        Tile.changeHighlight(app.map.tileList[row, col], (app.currentViewRow, app.currentViewCol), 
                             app.map, app.mapRenderer, (app.width,app.height), app.spriteDrawer)
        
def onMousePress(app, mouseX,mouseY):

    if app.currentTile != None:
        print('clicked tile')
        tile = app.map.tileList[app.currentTile[0], app.currentTile[1]]
        if tile.movableUnit != None:
            print('not none')
            app.isMoving = True
            app.prevClickTile = tile
        elif app.isMoving and app.prevClickTile!=None:
            unit = app.prevClickTile.movableUnit
            unit.move(app.currentTile)
            app.isMoving = False
            app.prevClickTile = None
            
        # unit.move()
    

def loadScreen(app, img):
    if img == None:
        img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
    img.save(f'{app.imgName}.jpg')

    return img

def getTile(app, mouseX, mouseY, screenSize, map, onlyRendered = False):
    if map == None: return None
    if map.tileList.size == 0: return None

    loc = getRelativeTile(mouseX, mouseY, screenSize, map)
    if loc == None: return None
    row, col = loc

    renderedMap = map.getRenderedMap()
    if renderedMap == None: renderedMap = map

    relativeRow,relativeCol = getRelativeTile(mouseX, mouseY, screenSize, map)

    if 0<=relativeRow<len(renderedMap.tileList) and 0 <= relativeCol < len(renderedMap.tileList[0]):
        tile = renderedMap.tileList[relativeRow, relativeCol]
        return tile.row, tile.col

    else: return None

def getRelativeTile(mouseX, mouseY, screenSize, map):
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
    
def takeNextTurn(app):
    for civilization in app.players:
        civilization.updateAllYields()        
    # app.players[0].settlements[0].harvestResources()
    print(f"Civilization - production:{app.players[0].yieldsByType[ResourceStack.ResourceTypes['production']]}, \
            food: {app.players[0].yieldsByType[ResourceStack.ResourceTypes['food']]}")
    app.players[0].useProduction()

def onKeyPress(app,key):
    if key == 'r':
        tileSprite = Sprite(app.tileImage)
        # app.map = MapRenderer.generateRepeatMap(app.mapRenderer, (app.mapRows,app.mapCols), None)
        app.map = MapRenderer.generateRandomMap(app.mapRenderer, app, (app.mapRows,app.mapCols))

        app.map.tileList[0,0].changeSprite(Tile.defaultSprites['green_tile'])
        app.currentViewRow, app.currentViewCol = getTile(app, app.width//2, app.height//2,(app.width,app.height), app.map)
        app.rendereredMap = MapRenderer.render(app.map, app, (app.currentViewRow,app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 's':
        if app.currentTile != None:
            row,col = app.currentTile
            settlement = Settlement(app, app.map.tileList[row,col], app.players[0], app.mapRenderer)
            settlement.instantiate()
            print(len(app.players[0].settlements))
    elif key == 'a':
        if app.currentTile != None:
            row,col = app.currentTile
            tile = app.map.tileList[row,col]
            print(tile.getType())
            print(tile.getRelativeLoc(app.map))
            
    elif key == 'd':
        app.players[0].settlements[0].builder.setUnit(Warrior(app.players[0], app))

    elif key == 'n':
        takeNextTurn(app)
    elif key == 'p':
        if app.currentTile != None:
            row,col = app.currentTile
            tile = app.map.tileList[row,col]
            # if app.map.tileList[row,col] in app.players[0].getCivilizationTiles():
            if tile.civilization == app.players[0]:
               settlement = tile.settlement
               if tile not in settlement.harvestedTiles: settlement.harvestedTiles.add(tile)
               else: settlement.harvestedTiles.remove(tile)
            
            # tile = app.map.tileList[row,col]

    elif key.isdigit() and 1 <=int(key) <= 3:
        if app.currentTile != None:
            types = List(Tile.tileTypes)    
            row,col = app.currentTile
            tile = app.map.tileList[row,col]
            # tile.setType(types[int(key) - 1])
    elif key == 'up' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewRow += 1
        clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'down' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewRow -=1
        clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'right' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewCol += 1
        clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'left' and app.map.tileList.size !=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewCol -= 1
        clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    
def clearScreen(app):
    app.img = loadScreen(app, None)

runApp()

