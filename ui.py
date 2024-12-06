from cmu_graphics import *
from abc import ABC, abstractmethod
import PIL as pl


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
        if self in app.renderedUI:
            app.renderedUI.remove(self)
        if self in app.interactableUI:
            app.interactableUI.remove(self)
        
        if exitMethod != None: app.exitMethodsToSet[exitMethod].remove(self)
    
    def display(self,app):
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
    

class CustomLabel():
    def __init__(self, text,size, screenLocation, color = 'black', time = None, bold=False):
        self.text = text
        self.size = size
        self.time = time
        self.x,self.y = screenLocation
        self.color = color
        self.bold = bold

    def __repr__(self):
        return f'CustomLabel({self.text})'
    
    def __eq__(self,other):
        return isinstance(other,CustomLabel) and other.text == self.text and other.time == self.time
    
    def __hash__(self):
        return hash(str(self))

    def display(self, app):
        app.renderedUI.append(self)
        if self.time!=None:
            app.timedUI[self] = self.time

    def removeAll(self,app):
        if self in app.renderedUI: app.renderedUI.remove(self)

    def setText(self, newText):
        self.text = newText

    def getTime(self):
        return self.time
    
    def getSize(self):
        return self.size
    
    def getText(self):
        return self.text
    
    def drawAll(self, app):
        drawLabel(self.text, self.x,self.y, fill = self.color, size = self.size, bold = self.bold) 

class Button(drawableUI):
    def __init__(self, gameManager, location, size, color, parentUI, function, text = None, textSize = None):
        self.parentUI = parentUI
        self.gameManager = gameManager
        self.x, self.y = location
        self.function = function
        self.width, self.height = size
        self.color = color
        self.interactable = True
        self.elements = set()
        self.text = text
        self.exitMethod = 'click off'
        self.textSize = textSize

        if self.parentUI != None:
            parentUI.elements.add(self)

        app.exitMethodsToSet[self.exitMethod].add(self)

    def execute(self, app):
        if self.function != None: 
            self.function(app)

        self.removeAll(app)
    
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
        drawRect(self.x, self.y, self.width, self.height, fill = self.color, border = 'black', borderWidth = self.height*0.1)
        if self.text != None and self.textSize != None: 
            drawLabel(self.text, self.x + self.width//2, self.y + self.height//2, size = self.textSize, bold = True)

    def setFunction(self, function):
        self.function = function

class PopulationButton(Button):
    def __init__(self, gameManager, location, size, color, parentUI, tile, text = None, textSize = None):
        self.parentUI = parentUI
        self.gameManager = gameManager
        self.x, self.y = location
        self.width, self.height = size
        self.color = color
        self.interactable = True
        self.elements = set()
        self.text = text
        self.exitMethod = 'click off'
        self.textSize = textSize
        self.tile = tile
        self.label = CustomLabel('Population Placed', 30, (app.width//2, 50), color = 'gold', time = 30, bold = True)

        if self.parentUI != None:
            parentUI.elements.add(self)

        app.exitMethodsToSet[self.exitMethod].add(self)
    
    def execute(self, app):
        if self.tile.civilization == app.players[app.currentPlayerID]:
            settlement = self.tile.settlement
            settlement.placePopulation(self.tile, app, ui = self)

        self.removeAll(app)

class SettlementButton(Button):
    def __init__(self, gameManager, location, size, color, parentUI, settler, text = None, textSize = None):
        self.parentUI = parentUI
        self.gameManager = gameManager
        self.x, self.y = location
        self.width, self.height = size
        self.color = color
        self.interactable = True
        self.elements = set()
        self.text = text
        self.exitMethod = 'click off'
        self.textSize = textSize
        self.settler = settler
        self.label = CustomLabel('Created Settlement!', 30, (app.width//2, 50), color = 'gold', time = 30, bold = True)

        if self.parentUI != None:
            parentUI.elements.add(self)

        app.exitMethodsToSet[self.exitMethod].add(self)
    
    def execute(self, app):
        self.settler.createSettlement()
        self.removeAll(app)


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
        self.productionButton = Button(self.gameManager, (self.leftBorder + self.backWidth//2 - 75, self.topBorder - 50), 
                             (150,50), 'brown', self, self.displayProductionMenu, text="Production Menu", textSize = 15)
        self.interactable = False
        self.productionMenu = ProductionMenu(app, self.settlement, self.gameManager)

        app.exitMethodsToSet[self.exitMethod].add(self)
        self.initializeLabelVariables(app)

    def displayProductionMenu(self,app):
        self.productionMenu.display(app)

    def initializeLabelVariables(self, app):
        # Label variables
        self.resourceLabelXFromEdge = app.width//2
        self.resourceLabelYSpacing = 75

    def drawLabels(self):
        i = 0
        for resource in self.settlement.yieldsByType:
            drawLabel(f'{resource.getName()}: {self.settlement.yieldsByType[resource]}', 
                      self.resourceLabelXFromEdge, self.topBorder + (i+1)*self.resourceLabelYSpacing, size = 30)
            i+=1
        if self.settlement.builder.unit!=None:
            drawLabel(f'Production Remaining Until Unit Made: {self.settlement.builder.getCostRemaining()}', self.resourceLabelXFromEdge, self.topBorder + (i+1)*self.resourceLabelYSpacing, size = 15)

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
        self.text = None
        self.textSize = None

        if self.parentUI != None:
            parentUI.elements.add(self)

    def __repr__(self):
        return 'ProductionOptionButton'
    
    def execute(self, app):
        unitClass = app.unitTypes[self.unitStr]
        unit = unitClass(self.parentUI.settlement.civilization, app)
        self.parentUI.startMakingUnit(app, unit)


class ProductionMenu(drawableUI):
    unitIcons = {'warrior' : pl.Image.open('sprites/warrior.png'), 'settler': pl.Image.open('sprites/settler.png'), 
                 'spearman' : pl.Image.open('sprites/spearman.png')}

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
        self.currentUnit = None

        self.iconSpacing = 75
        self.heading = 50

        self.intitializeButtons(app)


        app.exitMethodsToSet[self.exitMethod].add(self)

    def intitializeButtons(self, app):
        i = 0
        for name in ProductionMenu.unitIcons:
            image = ProductionMenu.unitIcons[name]
            button = ProductionOptionButton(self.gameManager, (self.leftBorder + self.backWidth//2 - image.size[0]//2, 
                      self.topBorder + self.heading + self.iconSpacing * i), image.size, None, self, name)
            i+=1
            
    def startMakingUnit(self, app, unit):
        self.settlement.builder.setUnit(unit)

    def drawUnitOptions(self, app):
        i = 0
        for icon in ProductionMenu.unitIcons:
            image = ProductionMenu.unitIcons[icon]
            drawImage(ProductionMenu.unitIcons[icon].filename, self.leftBorder + self.backWidth//2 - image.size[0]//2, 
                      self.topBorder + self.heading + self.iconSpacing * i)
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
        self.drawUnitOptions(app)
        drawLabel('Pick A Unit', self.leftBorder + self.backWidth//2, self.topBorder + 15, size = 20)

        
    def drawBackground(self, app):
        drawRect(self.leftBorder, app.height//2 - self.backHeight//2, self.backWidth, self.backHeight, fill = 'gray')

    def execute(self):
        pass


