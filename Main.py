from cmu_graphics import *
from PIL import Image
import numpy as np


def onAppStart(app):
    app.width = 600
    app.height = 600
    app.counter = 0
    app.imageColor = (255,255,255)
    app.imgName = "screen"
    app.img = loadScreen(app, None)
    app.colors = [(100,0,0), (0,100,0), (0,0,100)]

    app.ignorableColor = (255,255,255)
    app.tileImage = Image.open("sprites/TileShape.png")
    app.tileData = loadTileData(app, app.tileImage)
    # print(np.asarray(app.img))
    
def redrawAll(app):
    drawImage("screen.jpg", 0, 0)
    drawRect(100, 100, 100, 50)

def addTile(app, x,y):
    newScreenData = np.asarray(app.img).copy()
    rows = len(app.tileData)
    cols = len(app.tileData[0])

    for row in range(rows):
        for col in range(cols):
            # print(f'Row: {row}, Col: {col}')
            # print(newScreenData[x + row, y + col], app.tileData[row,col][:-1])
            # if app.tileData[row,col] != app.ignorableColor:
            newScreenData[y + row, x + col] = app.tileData[row,col][:-1]
    updateScreen(app, Image.fromarray(newScreenData, mode = "RGB"))
        

def loadTileData(app, tileImage):
    tileData = np.asarray(tileImage).copy()
    return tileData

def updateScreen(app, newScreen):
    if(newScreen != None): app.img = newScreen
    loadScreen(app,newScreen)

def loadScreen(app, img):
    if img == None:
        img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
    img.save(f'{app.imgName}.jpg')

    return img

def onKeyPress(app,key):
    if key.isdigit() and 1 <=int(key) <= 3:
        addTile(app, 100*(int(key)-1),0)
        # app.imageColor = app.colors[int(key)-1]
        # app.img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
        # updateScreen(app,app.img)
    

runApp()

