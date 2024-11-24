from cmu_graphics import *
from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite
from map_render import MapRenderer
from tiles import Tile


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

    app.ignorableColor = (255,255,255)
    app.tileImage = Image.open("sprites/TileShape.png")
    app.spriteDrawer = SpriteDrawer(app.img, (app.width,app.height), app.imgName)
    
def redrawAll(app):
    drawImage("screen.jpg", 0, 0)

def loadScreen(app, img):
    if img == None:
        img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
    img.save(f'{app.imgName}.jpg')

    return img

def onKeyPress(app,key):
    if key.isdigit() and 1 <=int(key) <= 3:
        tileSprite = Sprite(app.tileImage)

        app.map = MapRenderer.generateRepeatMap(tileSprite, (15,15)) 
        MapRenderer.render(app.map, (app.width,app.height), app.spriteDrawer, tileSprite.getSize())
    if key == 'h':
        if app.map.size != 0:
            t = app.map[2,2]
            Tile.changeTileBorder(t, [255,0,0])
            Tile.redrawTile(t, app.spriteDrawer)
runApp()

