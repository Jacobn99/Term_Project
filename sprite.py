from cmu_graphics import *
from PIL import Image
import numpy as np

class Sprite():
    def __init__(self, img):
        self.img = img
        self.data = np.asarray(img)[:,:,:3].copy()
        self.width, self.height, self.data = Sprite.getSpriteData(self.img)

    def updateSprite(self, newImg):
        self.width, self.height, self.data = Sprite.getSpriteData(newImg)
        self.img = newImg

    def getSize(self):
        return (self.width, self.height)

    def getData(self):
        return self.data[:,:,:3].copy()
    
    def getImage(self):
        return Image.open(self.img.filename)
    
    def __eq__(self,other):
        return isinstance(other, Sprite) and self.img == other.img
    
    def __repr__(self):
        return f'Sprite({self.img.filename})'

    def __hash__(self):
        return hash(str(self))
    
    @staticmethod
    def getSpriteData(img):
        data = np.asarray(img)
        return len(data[0]), len(data), data

class SpriteDrawer:
    ignorableColor = [255,255,255]
    
    def __init__(self, app, screenSize, screenName):
        self.app = app
        self.width = screenSize[0]
        self.height = screenSize
        self.screenName = screenName

    def drawSprite(self,sprite, x, y):
        screenData = np.asarray(self.app.img)[:,:,:3].copy()
        screenWidth = len(screenData[0])
        screenHeight = len(screenData)
        spriteData = sprite.getData()
        x = int(x)
        y = int(y)        
        cols, rows = sprite.getSize()

        for row in range(rows):
            if(0<=y+row<screenHeight):
                for col in range(cols):
                    if (0<=x+col<screenWidth and
                        spriteData[row,col][:3].tolist() != SpriteDrawer.ignorableColor):
                        # print(row,col)
                        # print("bonga")
                        screenData[y + row, x + col][:3] = spriteData[row,col][:3]

                        # try:
                        #     screenData[y + row, x + col][:3] = spriteData[row,col][:3]
                        # except:
                        #     print(row,col)
                        #     print(f"Data is set to None: screenDataSize = {(len(screenData), len(screenData[0]))}, spriteDataSize = {(len(spriteData), len(spriteData[0]))}")

        newScreen = Image.fromarray(screenData, mode = "RGB")
        self.updateScreen(newScreen)

    def updateScreen(self, newScreen):
        # screen = self.app.img
        if(newScreen != None): self.app.img = newScreen
        self.loadScreen(newScreen)

    def loadScreen(self, img):
        if img == None:
            img = Image.new(mode = "RGB", size = (self.width,self.height), color = (255,255,255))
        img.save(f'{self.screenName}.jpg')
        
