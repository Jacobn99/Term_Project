from cmu_graphics import *
from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from map_render import MapRenderer
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
    app.map = np.array([])
    app.prevHoveredTileLoc = None
    app.mapRenderer = MapRenderer()
    app.currentViewX = None
    app.currentViewY = None

    app.ignorableColor = (255,255,255)
    app.tileImage = Image.open("sprites/TileShape.png")
    app.spriteDrawer = SpriteDrawer(app.img, (app.width,app.height), app.imgName)
    
def redrawAll(app):
    drawImage("screen.jpg", 0, 0)

def onMouseMove(app, mouseX,mouseY):
    mapLoc = getTile(mouseX, mouseY, (app.width,app.height), app.map, True)

    if mapLoc != app.prevHoveredTileLoc and app.prevHoveredTileLoc != None: 
        Tile.changeHighlight(app.map[app.prevHoveredTileLoc[0], app.prevHoveredTileLoc[1]], app.map, 
                             app.mapRenderer, (app.width,app.height),app.spriteDrawer)
        app.prevHoveredTileLoc = None
    if mapLoc != None and mapLoc != app.prevHoveredTileLoc:
        app.prevHoveredTileLoc = mapLoc
        Tile.changeHighlight(app.map[app.prevHoveredTileLoc[0], app.prevHoveredTileLoc[1]], app.map, 
                             app.mapRenderer, (app.width,app.height), app.spriteDrawer)


def loadScreen(app, img):
    if img == None:
        img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
    img.save(f'{app.imgName}.jpg')

    return img

def getTile(mouseX, mouseY, screenSize, map, onlyRendered = False):
    if map.size == 0: return None
    else:
        tile0 = map[0,0]
        tileWidth, tileHeight = tile0.getSize()
        startX,startY = MapRenderer.getMapStartLocation(screenSize, tile0.getSize(), len(map))

        startX += tileWidth
        startY -= (-1 * tileHeight)//2
        row = math.floor((mouseX - startX)/tileWidth + (mouseY - startY)/tileHeight) + 1
        col = math.floor((mouseY - startY)/tileHeight - (mouseX - startX)/tileWidth)

        if onlyRendered and (row, col) not in Tile.renderedTilesSet: return None
        if 0<=row<len(map) and 0<=col<len(map[0]): return row,col
        else: return None
    
def onKeyPress(app,key):
    if key.isdigit() and 1 <=int(key) <= 3:
        tileSprite = Sprite(app.tileImage)
        app.map = MapRenderer.generateRepeatMap(app.mapRenderer, tileSprite, (20,20))
        app.map[0,0].changeSprite(Tile.defaultSprites['green_tile'])
        app.currentViewX, app.currentViewY = getTile(app.width//2, app.height//2,(app.width,app.height), app.map)

        MapRenderer.render(app.map, (app.currentViewX, app.currentViewY), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'h':
        if app.map.size != 0:
            t = app.map[5,5]
            Tile.changeTileBorder(t, [255,0,0])
            Tile.redrawTile(t, app.spriteDrawer, (app.width,app.height), app.map, app.mapRenderer)

    elif key == 'up' and app.map.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewY += 1
        clearScreen(app)
        MapRenderer.render(app.map, (app.currentViewX, app.currentViewY), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'down' and app.map.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewY -=1
        clearScreen(app)
        MapRenderer.render(app.map, (app.currentViewX, app.currentViewY), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'right' and app.map.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewX += 1
        clearScreen(app)
        MapRenderer.render(app.map, (app.currentViewX, app.currentViewY), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    elif key == 'left' and app.map.size!=0:
        tileSprite = Sprite(app.tileImage)
        app.currentViewY -= 1
        clearScreen(app)
        MapRenderer.render(app.map, (app.currentViewX, app.currentViewY), (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    
def clearScreen(app):
    app.img = loadScreen(app, None)

runApp()

