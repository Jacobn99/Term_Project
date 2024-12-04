from typing import List
from cmu_graphics import *
import PIL as pil
import numpy as np
from sprite import SpriteDrawer, Sprite
from map_render import MapRenderer, Map
from settlement import Settlement
from player_civilization import Civilization
from tiles import Tile
import math
from resources import ResourceIcon, ResourceStack
from buildable_units import *
from game_management import *
from ui import *


# Go in numpy and make it so only the part of the map you can see if being rendered at one time 
# (edit the map being used with numpy to include only what you can see)

def onAppStart(app):
    app.gameManager = GameManager()

    app.width = 600
    app.height = 600
    app.counter = 0
    app.imageColor = (255,255,255)
    app.imgName = "screen"
    app.img = app.gameManager.loadScreen(app, None)
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
    app.tileImage = pil.Image.open("sprites/TileShape.png")
    app.spriteDrawer = SpriteDrawer(app, (app.width,app.height), app.imgName)
    app.currentTile = None
    app.resourceIcons = set()
    app.tileSize = (100,50)
    app.isMoving = False
    app.drawableUnits = []
    app.prevClickTile = None
    app.tileHeight,app.tileWidth = app.tileImage.size
    app.renderedUI = []

    app.players = [Civilization(), Civilization()]
    app.currentPlayerID = 0

    app.gameManager.startGame(app)

def redrawAll(app):
    drawImage("screen.jpg", 0, 0)
    drawUnits(app)
    drawResourceIcons(app)
    drawUI(app)
    


def drawUI(app):
    for ui in app.renderedUI:
        print('got here')
        ui.drawAll(app)

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
    mapLoc = app.gameManager.getTile(app, mouseX, mouseY, (app.width,app.height), app.map, True)

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

    currentPlayer = app.players[app.currentPlayerID]
    if app.currentTile != None:
        print('clicked tile')
        tile = app.map.tileList[app.currentTile[0], app.currentTile[1]]
        if tile.movableUnit != None:
            app.isMoving = True
            app.prevClickTile = tile
        elif app.isMoving and app.prevClickTile!=None:
            unit = app.prevClickTile.movableUnit
            unit.move(app.currentTile)
            app.isMoving = False
            app.prevClickTile = None
        
        if tile.settlement != None and tile.settlement in currentPlayer.settlements:
            ui = SettlementUI(app, app.gameManager)
            ui.instantiate(app)
            

            
        # unit.move()
 
def onKeyPress(app,key):
    currentPlayer = app.players[app.currentPlayerID]

    if key == 's':
        if app.currentTile != None:
            row,col = app.currentTile
            settlement = Settlement(app, app.map.tileList[row,col], currentPlayer, app.mapRenderer)
            settlement.instantiate()
            print(len(currentPlayer.settlements))
    elif key == 'a':
        if app.currentTile != None:
            row,col = app.currentTile
            tile = app.map.tileList[row,col]
            print(tile.getType())
            print(tile.getRelativeLoc(app.map))
            
    elif key == 'd':
        currentPlayer.settlements[0].builder.setUnit(Warrior(currentPlayer, app))

    elif key == 'n':
        app.gameManager.endPlayerTurn(app)
    elif key == 'p':
        if app.currentTile != None:
            row,col = app.currentTile
            tile = app.map.tileList[row,col]
            if tile.civilization == currentPlayer:
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
        app.gameManager.clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'down' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewRow -=1
        app.gameManager.clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'right' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewCol += 1
        app.gameManager.clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'left' and app.map.tileList.size !=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewCol -= 1
        app.gameManager.clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    
runApp()