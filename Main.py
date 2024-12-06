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
from tile_types import TileType


def onAppStart(app):
    app.gameManager = GameManager()
    app.win = False


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
    app.viewRowSize = 9
    app.viewColSize = 9

    app.ignorableColor = (255,255,255)
    app.tileImage = pil.Image.open("sprites/TileShape.png")
    app.spriteDrawer = SpriteDrawer(app, (app.width,app.height), app.imgName)
    app.resourceIcons = set()
    app.tileSize = (100,50)
    app.isMoving = False
    app.drawableUnits = []
    app.prevClickTile = None
    app.tileHeight,app.tileWidth = app.tileImage.size
    app.renderedUI = []
    app.players = [Civilization(), Civilization()]
    app.currentPlayerID = 0

    app.currentTile = None
    app.currentUnit = None
    app.lastClickedUnit = None
    app.hasMoved = set()

    app.timedUI = dict()    
    app.interactableUI = set()

    app.unitTypes = {'warrior' : Warrior, 'settler' : Settler, 'spearman' : Spearman}

    app.gameManager.startGame(app)

    initializeExitMethods(app)

def initializeExitMethods(app):
    app.clickOffExitUI = set()

    app.exitMethodsToSet= {'click off': app.clickOffExitUI}

def redrawAll(app):
    drawImage("screen.jpg", 0, 0)
    drawUnits(app)
    drawResourceIcons(app)
    drawUI(app)

    if app.win == True:
        drawLabel("Game Ended", app.width//2, app.height//2, fill = 'gold', size = 50, bold = True)
    
def drawUI(app):
    for ui in app.renderedUI:
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
    if app.win:return
    mapLoc = app.gameManager.getTile(app, mouseX, mouseY, (app.width,app.height), app.map, True)
    hoveredUnit = None

    if mapLoc != app.prevHoveredTileLoc and app.prevHoveredTileLoc != None: 
        prevRow, prevCol = app.prevHoveredTileLoc
        Tile.changeHighlight(app.map.tileList[prevRow, prevCol], app, (app.currentViewRow, app.currentViewCol), 
                             app.map, app.mapRenderer, (app.width,app.height), app.spriteDrawer)
        app.prevHoveredTileLoc = None
    if mapLoc != None:
        row, col = mapLoc

        tile = app.map.tileList[row,col]
        if mapLoc != app.prevHoveredTileLoc:
            app.prevHoveredTileLoc = (row,col)
            t = app.map.tileList[row,col]
            Tile.changeHighlight(app.map.tileList[row, col], app, (app.currentViewRow, app.currentViewCol), 
                                app.map, app.mapRenderer, (app.width,app.height), app.spriteDrawer)
        
        if tile.movableUnit != None:
            hoveredUnit = tile.movableUnit

    if app.currentUnit != None and hoveredUnit != app.currentUnit and app.currentUnit.isAlive:
        app.currentUnit.hideHPDisplay(app)

    elif hoveredUnit != None and mapLoc!=app.currentTile:
        hoveredUnit.displayHP(app)


    app.currentUnit = hoveredUnit
    
    if mapLoc == None: app.currentTile = None
    else: app.currentTile = (row,col)
        
def onMousePress(app, mouseX,mouseY):
    if app.win: return
    pauseInteractables = False
    currentPlayer = app.players[app.currentPlayerID]

    for ui in app.interactableUI.copy():
        if ui.inBounds(mouseX,mouseY): ui.execute(app)
        pauseInteractables = True

    for ui in app.clickOffExitUI.copy():
        if not ui.inBounds(mouseX,mouseY): ui.removeAll(app)

    if app.currentTile != None:
        tile = app.map.tileList[app.currentTile[0], app.currentTile[1]]
        currentUnit = tile.movableUnit
        dontMove = False

        # if currentUnit != None:
        if (app.lastClickedUnit not in app.hasMoved 
            and app.lastClickedUnit != None
            and app.lastClickedUnit
            and app.lastClickedUnit.civilization
            and app.lastClickedUnit.isOffensive):
            
            if (currentUnit != None and currentUnit != app.lastClickedUnit 
                and currentUnit.civilization != currentPlayer):
                app.lastClickedUnit.attack(currentUnit)
                dontMove = True
        
            elif (isinstance(tile.getType(),SettlementCenter)):
                app.lastClickedUnit.attack(tile.settlement)
                dontMove = True

        if app.isMoving and app.prevClickTile != None and not dontMove:
            unit = app.prevClickTile.movableUnit
            if unit != None and unit.civilization == currentPlayer:
                unit.move(app, app.currentTile)
                app.isMoving = False
                app.prevClickTile = None
        
        if tile.getType() == app.gameManager.getTileType('settlement_center') and tile.civilization == currentPlayer:
            tile.settlement.displayUI()
        elif tile.settlement != None and tile.movableUnit == None and not pauseInteractables:
            relativeRow, relativeCol = Tile.getRelativeLoc(tile.row, tile.col, app.map)
            location = Tile.mapToScreenCords((relativeRow,relativeCol), tile.getSize(), (app.width,app.height), app.map.getRenderedMap(), app.mapRenderer)
            
            text = 'Place population?'
            if tile in tile.settlement.harvestedTiles:
                text = 'Remove population?'
            
            populationButton = PopulationButton(app.gameManager, location, (130, 50), 'gray',
                                                None, tile, text = text, textSize=13)
            populationButton.display(app)

        app.isMoving = True
        app.prevClickTile = tile
        app.lastClickedUnit = currentUnit

def onStep(app):
    garbage = set()
    for ui in app.timedUI:
        if app.timedUI[ui] <= 0 and ui in app.renderedUI:
            ui.removeAll(app)
            garbage.add(ui)
        else: app.timedUI[ui] -= 1

    for ui in garbage:
        app.timedUI.pop(ui)

def onKeyPress(app,key):
    currentPlayer = app.players[app.currentPlayerID]
    if app.currentTile!=None: tile = app.map.tileList[app.currentTile[0], app.currentTile[1]]
    else: tile = None


    if key == 's':
        if app.currentTile != None:
            if (isinstance(tile.movableUnit, Settler) and
            tile.movableUnit.civilization == currentPlayer):
                tile.movableUnit.getSettlementButton().display(app)

    if key == 'g':
        if app.currentTile != None:
            app.players[1].createSettlement(tile, app)

    elif key == 'd':
        if app.currentTile != None:
            tile = app.map.tileList[app.currentTile[0], app.currentTile[1]]
            warrior = Warrior(app.players[1], app)
            warrior.instantiate((tile.row,tile.col))

    elif key == 'n':
        app.gameManager.endPlayerTurn(app)
    
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