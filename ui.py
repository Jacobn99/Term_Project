from cmu_graphics import *
from abc import ABC, abstractmethod


class drawableUI(ABC):
    @abstractmethod
    def drawAll(self, app):
        pass

class Button(drawableUI):
    def __init__(self, gameManager, location, size, color, function = None):
        self.gameManager = gameManager
        self.x, self.y = location
        self.function = function
        self.width, self.height = size
        self.color = color
    
    # def execute(self):
    #     self.function(self.gameManager)

    def instantiate(self, app):
        app.renderedUI.append(self)

    def drawAll(self, app):
        drawRect(self.x, self.y, self.width, self.height, fill = self.color)
    

class SettlementUI(drawableUI):
    def __init__(self, app, gameManager):
        self.gameManager = gameManager
        self.backWidth = 400
        self.backHeight = 300
        self.leftBorder = app.width//2 - self.backWidth//2
        self.topBorder = app.height//2 - self.backHeight//2
        self.button = Button(self.gameManager, (self.leftBorder + self.backWidth//3, self.topBorder + self.backHeight//2), 
                             (100,100), 'brown')

    def instantiate(self, app):
        app.renderedUI.append(self)
        self.button.instantiate(app)

    def drawAll(self, app):
        self.drawBackground(app)

    def drawBackground(self, app):
        drawRect(self.leftBorder, app.height//2 - self.backHeight//2, self.backWidth, self.backHeight, fill = 'gray')

    
    
