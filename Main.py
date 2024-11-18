from cmu_graphics import *
from PIL import Image
import numpy as np

def onAppStart(app):
    app.counter = 0
    app.imageColor = (0,0,0)
    app.imgName = "screen"
    app.img = loadScreen(app)
    app.colors = [(100,0,0), (0,100,0), (0,0,100)]


def redrawAll(app):
    drawImage("screen.jpg", 0, 0)

def updateScreen(app, img):
    loadScreen(app,img = img)

def loadScreen(app, img = None):
    if img == None:
        img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
    img.save(f'{app.imgName}.jpg')

    return img

def onKeyPress(app,key):
    if key.isdigit() and 1 <=int(key) <= 3:
        app.imageColor = app.colors[int(key)-1]
        app.img = Image.new(mode = "RGB", size = (app.width,app.height), color = app.imageColor)
        updateScreen(app,app.img)
        
    #drawPolygon(100, 100, 200, 100, 200, 200, 100, 200)
    # startX = 0
    # startY = 0
    # for row in range(app.rows):
    #     for col in range(app.cols):
    #         drawRect(startX + app.pixelSize * row, + startY + app.pixelSize * col, app.pixelSize, app.pixelSize, 
    #         fill = 'red' if col % 2 == app.num else 'black')

# def onStep(app):
    # app.counter +=1

    # if app.counter % 60: app.num = (app.num + 1)%2
    

runApp()

