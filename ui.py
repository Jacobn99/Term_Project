from cmu_graphics import *
from abc import ABC, abstractmethod
import PIL as pl
from buildable_units import *


# Class has abstract methods for debugging purposes
class drawableUI(ABC):

    @abstractmethod
    def drawAll(self, app):
        pass

    @abstractmethod
    def isInteractable(self):
        pass

    @abstractmethod
    def getSubelements(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def getTopLeftLoc(self):
        pass

    @abstractmethod
    def getSize(self):
        pass

    @abstractmethod
    def getExitMethod(self):
        pass

    def removeAll(self,app):
        self.remove(app)

        for element in self.getSubelements():
            element.removeAll(app)

    def remove(self, app):
        exitMethod = self.getExitMethod()
        print(self in app.renderedUI, self in app.interactableUI)
        if self in app.renderedUI:
            app.renderedUI.remove(self)
        if self in app.interactableUI:
            app.interactableUI.remove(self)
        
        if exitMethod != None: app.exitMethodsToSet[exitMethod].remove(self)
    
    def display(self,app):
        # print('called')
        exitMethod = self.getExitMethod()

        if self not in app.renderedUI:
            app.renderedUI.append(self)
        if self.isInteractable():
            app.interactableUI.add(self)

        for element in self.getSubelements():
            element.display(app)

        if exitMethod != None: app.exitMethodsToSet[exitMethod].add(self)

    def inBounds(self, x, y):
        elementX, elementY = self.getTopLeftLoc()
        width,height = self.getSize()
        return (elementX <= x <= elementX + width and 
                elementY <= y <= elementY + height)
    

class Button(drawableUI):
    def __init__(self, gameManager, location, size, color, parentUI, function):
        self.parentUI = parentUI
        self.gameManager = gameManager
        self.x, self.y = location
        self.function = function
        self.width, self.height = size
        self.color = color
        self.interactable = True
        self.elements = set()

        if self.parentUI != None:
            parentUI.elements.add(self)

    def execute(self, app):
        if self.function != None: self.function(app)
    
    def getExitMethod(self):
        return None

    def getSubelements(self):
        return self.elements
    
    def isInteractable(self):
        return self.interactable
    
    def getTopLeftLoc(self):
        return (self.x,self.y)
    
    def getSize(self):
        return (self.width,self.height)

    def drawAll(self, app):
        drawRect(self.x, self.y, self.width, self.height, fill = self.color)

    def setFunction(self, function):
        self.function = function
    
class SettlementUI(drawableUI):
    def __init__(self, app, settlement, gameManager):
        self.gameManager = gameManager
        self.elements = set()
        self.backWidth = 400
        self.backHeight = 300
        self.leftBorder = app.width//2 - self.backWidth//2
        self.topBorder = app.height//2 - self.backHeight//2
        self.exitMethod = 'click off'
        self.settlement = settlement
        self.productionButton = Button(self.gameManager, (self.leftBorder + self.backWidth//3, self.topBorder + self.backHeight//2), 
                             (100,100), 'brown', self, self.displayProductionMenu)
        self.interactable = False
        self.productionMenu = ProductionMenu(app, self.settlement, self.gameManager)

        app.exitMethodsToSet[self.exitMethod].add(self)
        self.initializeLabelVariables()

    # def button1Function(self, app):
    #     print('bazinga')

    def displayProductionMenu(self,app):
        self.productionMenu.display(app)

    def initializeLabelVariables(self):
        # Label variables
        self.resourceLabelXFromEdge = 10
        self.resourceLabelYSpacing = 10

    def drawLabels(self):
        i = 0
        for resource in self.settlement.yieldsByType:
            drawLabel(f'{resource.getName()}: {self.settlement.yieldsByType[resource]}', 
                      self.leftBorder + self.resourceLabelXFromEdge, self.topBorder + (i+1)*self.resourceLabelYSpacing)
            i+=1

    def getExitMethod(self):
        return self.exitMethod

    def getSize(self):
        return (self.backWidth, self.backHeight)
    
    def getTopLeftLoc(self):
        return (self.leftBorder, self.topBorder)

    def getSubelements(self):
        return self.elements

    def isInteractable(self):
        return self.interactable

    def drawAll(self, app):
        self.drawBackground(app)
        self.drawLabels()
        
    def drawBackground(self, app):
        drawRect(self.leftBorder, app.height//2 - self.backHeight//2, self.backWidth, self.backHeight, fill = 'gray')

    def execute(self):
        pass

class ProductionOptionButton(Button):
    def __init__(self, gameManager, location, size, color, parentUI, unitStr):
        self.parentUI = parentUI
        self.gameManager = gameManager
        self.x, self.y = location
        self.width, self.height = size
        self.color = color
        self.interactable = True
        self.elements = set()
        self.unitStr = unitStr

        if self.parentUI != None:
            parentUI.elements.add(self)

    def __repr__(self):
        return 'ProductionOptionButton'
    
    def execute(self, app):
        # print('here')
        unitClass = self.parentUI.unitTypes[self.unitStr]
        unit = unitClass(self.parentUI.settlement.civilization, app)
        self.parentUI.startMakingUnit(app, unit)


class ProductionMenu(drawableUI):
    def __init__(self, app, settlement, gameManager):
        self.gameManager = gameManager
        self.elements = set()
        self.backWidth = 300
        self.backHeight = 500
        self.leftBorder = app.width//2 - self.backWidth//2
        self.topBorder = app.height//2 - self.backHeight//2
        self.exitMethod = 'click off'
        self.settlement = settlement
        self.interactable = False
        self.unitIcons = {'warrior' : pl.Image.open('sprites\warrior.png')}
        self.unitTypes = {'warrior' : Warrior}
        self.currentUnit = None

        self.iconSpacing = 100
        self.heading = 50

        self.intitializeButtons(app)


        app.exitMethodsToSet[self.exitMethod].add(self)

    def intitializeButtons(self, app):
        for name in self.unitIcons:
            image = self.unitIcons[name]
            button = ProductionOptionButton(self.gameManager, (self.leftBorder + self.backWidth//2 - image.size[0]//2, 
                      self.topBorder + self.heading), image.size, None, self, name)
            
    def startMakingUnit(self, app, unit):
        # unit = unitClass(self.settlement.civilization, app)
        self.settlement.builder.setUnit(unit)

    def drawUnitOptions(self, app):
        for icon in self.unitIcons:
            image = self.unitIcons[icon]
            drawImage(self.unitIcons[icon].filename, self.leftBorder + self.backWidth//2 - image.size[0]//2, 
                      self.topBorder + self.heading)


    def getExitMethod(self):
        return self.exitMethod

    def getSize(self):
        return (self.backWidth, self.backHeight)
    
    def getTopLeftLoc(self):
        return (self.leftBorder, self.topBorder)

    def getSubelements(self):
        return self.elements

    def isInteractable(self):
        return self.interactable

    def drawAll(self, app):
        self.drawBackground(app)
        self.drawUnitOptions(app)
        
    def drawBackground(self, app):
        drawRect(self.leftBorder, app.height//2 - self.backHeight//2, self.backWidth, self.backHeight, fill = 'gray')

    def execute(self):
        pass


