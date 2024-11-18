from cmu_graphics import *
from PIL import Image
import numpy as np


def onAppStart(app):
    app.width = 600
    app.height = 600
    app.counter = 0
    app.imageColor = (0,0,0)
    app.imgName = "screen"
    app.img = loadScreen(app)
    app.colors = [(100,0,0), (0,100,0), (0,0,100)]
    
def redrawAll(app):
    drawImage("screen.jpg", 0, 0)
    drawRect(100, 100, 100, 50)

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
    

runApp()



