from cmu_graphics import *
from PIL import Image
import numpy as np

class Sprite():
    def __init__(self, img, spriteDrawer):
        self.img = img
        self.width, self.height, self.data = Sprite.getSpriteData(self.img)
        self.spriteDrawer = spriteDrawer

    def updateSprite(self, newSprite):
        self.width, self.height, self.data = Sprite.getSpriteData(newSprite)

    def getSize(self):
        return (self.width, self.height)

    def getData(self):
        return self.data
    
    def drawSprite(self, x, y):
        self.spriteDrawer.drawSprite(self, x,y)
    
    @staticmethod
    def getSpriteData(img):
        data = np.asarray(img)
        return len(data), len(data[0]), data

class SpriteDrawer:
    ignorableColor = [255,255,255]
    
    def __init__(self, screen, screenSize, screenName):
        self.screen = screen
        self.width = screenSize[0]
        self.height = screenSize
        self.screenName = screenName

    def drawSprite(self, sprite, x, y):
        screenData = np.asarray(self.screen).copy()
        spriteData = sprite.getData()
        
        rows, cols = sprite.getSize()

        for row in range(rows):
            for col in range(cols):
                if spriteData[row,col][:-1].tolist() != SpriteDrawer.ignorableColor:
                    screenData[y + row, x + col] = spriteData[row,col][:-1]
        newScreen = Image.fromarray(screenData, mode = "RGB")
        self.updateScreen(newScreen)

    def updateScreen(self, newScreen):
        if(newScreen != None): self.screen = newScreen
        self.loadScreen(newScreen)

    def loadScreen(self, img):
        if img == None:
            img = Image.new(mode = "RGB", size = (self.width,self.height), color = (255,255,255))
        img.save(f'{self.screenName}.jpg')
        
