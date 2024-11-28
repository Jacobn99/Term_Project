from cmu_graphics import *
from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from map_render import MapRenderer, Map
from tiles import Tile
import math


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
    app.mapRows = 15
    app.mapCols = 15
    app.prevHoveredTileLoc = None
    app.mapRenderer = MapRenderer()
    app.currentViewCol = None # From top left cornerer
    app.currentViewRow = None # From top left cornerer
    app.renderedMap = None
    app.viewRowSize = 8
    app.viewColSize = 8

    app.ignorableColor = (255,255,255)
    app.tileImage = Image.open("sprites/TileShape.png")
    app.spriteDrawer = SpriteDrawer(app.img, (app.width,app.height), app.imgName)
    
def redrawAll(app):
    drawImage("screen.jpg", 0, 0)

def onMouseMove(app, mouseX,mouseY):
    mapLoc = getTile(app, mouseX, mouseY, (app.width,app.height), app.map, True)
    # print(mapLoc)

    if mapLoc != app.prevHoveredTileLoc and app.prevHoveredTileLoc != None: 
        prevRow, prevCol = app.prevHoveredTileLoc
        Tile.changeHighlight(app.map.tileList[prevRow, prevCol], (app.currentViewRow, app.currentViewCol), 
                             app.map, app.mapRenderer, (app.width,app.height), app.spriteDrawer)
        app.prevHoveredTileLoc = None
    if mapLoc != None and mapLoc != app.prevHoveredTileLoc:
        row, col = mapLoc
        app.prevHoveredTileLoc = (row,col)
        Tile.changeHighlight(app.map.tileList[row, col], (app.currentViewRow, app.currentViewCol), 
                             app.map, app.mapRenderer, (app.width,app.height), app.spriteDrawer)
        

def loadScreen(app, img):
    if img == None:
        img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
    img.save(f'{app.imgName}.jpg')

    return img

def getTile(app, mouseX, mouseY, screenSize, map, onlyRendered = False):
    if map == None: return None
    if map.tileList.size == 0: return None

    tileList = map.tileList
    rows, cols = len(tileList), len(tileList[0])

    loc = getRelativeTile(app, mouseX, mouseY, screenSize, map, onlyRendered)
    if loc == None: return None
    # print('got here')

    # print(f'original: {loc}')

    row, col = loc

    renderedMap = map.getRenderedMap()
    if renderedMap == None: renderedMap = map

    row,col = getRelativeTile(app, mouseX, mouseY, screenSize, map, onlyRendered)
    relativeRow = row
    relativeCol = col
    if(app.currentViewCol != None and app.currentViewRow != None):
        row += app.currentViewRow
        col += app.currentViewCol
       
    if onlyRendered and ((0 > relativeRow or relativeRow>=len(renderedMap.tileList)) or 
                         (0 > relativeCol or relativeCol>=len(renderedMap.tileList[0]))): return None
    # return renderedMap.tileList[relativeRow,relativeCol].row, renderedMap.tileList[relativeRow,relativeCol].col
    return row, col

def getRelativeTile(app, mouseX, mouseY, screenSize, map, onlyRendered = False):
    if map == None: return None
    if map.tileList.size == 0: return None
    else:
        renderedMap = map.getRenderedMap()
        if renderedMap == None: renderedMap = map
        # tileList = map.tileList
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
    
def onKeyPress(app,key):
    if key.isdigit() and 1 <=int(key) <= 3:
        tileSprite = Sprite(app.tileImage)
        app.map = MapRenderer.generateRepeatMap(app.mapRenderer, tileSprite, (app.mapRows,app.mapCols))
        app.map.tileList[0,0].changeSprite(Tile.defaultSprites['green_tile'])
        app.currentViewRow, app.currentViewCol = getTile(app, app.width//2, app.height//2,(app.width,app.height), app.map)


        app.rendereredMap = MapRenderer.render(app.map, app, (app.currentViewCol, app.currentViewRow), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'h':
        if app.map.size != 0:
            t = app.map[5,5]
            Tile.changeTileBorder(t, [255,0,0])
            Tile.redrawTile(t, (app.currentViewRow, app.currentViewCol), app.spriteDrawer, (app.width,app.height), app.map, app.mapRender)

    elif key == 'up' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewRow -= 1
        clearScreen(app)
        MapRenderer.render(app.map, app, (app.currentViewRow, app.currentViewCol), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'down' and app.map.tileList.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewRow +=1
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

