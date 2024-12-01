from PIL import Image
from abc import ABC, abstractmethod


class ResourceIcon:
    # iconImgSize = 25
    labelImgSpacing = 5
    ImgSpacing = 28
    def __init__(self,tile, app):
        self.tile = tile
        self.app = app
        self.imgSize = self.tile.getResources()[0].getType().getImage().size
        app.resourceIcons.add(self)
        # self.resources = tile.getResources()

    def getResources(self):
        return self.tile.resources

    def getImageLocs(self):
        result = []
        resources = self.getResources()
        numOfResources = len(resources)
        tileWidth, tileHeight = self.tile.getSize()
        relativeRow,relativeCol = self.tile.realToRelativeLoc(self.tile.row, self.tile.col, self.app.map,
                                                              self.app.currentViewRow, self.app.currentViewCol)
        
        centerX,y = self.tile.mapToScreenCords((relativeRow, relativeCol), self.tile.getSize(), 
                                                    (self.app.width, self.app.height), self.app.map.getRenderedMap(), 
                                                    self.app.mapRenderer)
        centerX = centerX + tileWidth//2 - self.imgSize[0]//2
        y = y + tileHeight//2 - 1*self.imgSize[1]//4

        for i in range(numOfResources):
            correction = i * ResourceIcon.ImgSpacing - (ResourceIcon.ImgSpacing * (numOfResources))//4
            result.append((centerX + correction, y))

        return result
    
    def getLabelLocs(self, imageLocs):
        result = []
        
        for i in range(len(imageLocs)):
            x = imageLocs[i][0] - ResourceIcon.labelImgSpacing
            y = imageLocs[i][1] + self.imgSize[i]//2
            result.append((x,y))
        return result
    
    def deleteIcon(self):
        self.app.resourceIcons.remove(self)
        self.tile.resoruceIcon = None
        
class ResourceType(ABC):
    @abstractmethod
    def getName(self):
        pass

    def getImagePath(self):
        pass

    def getImage(self):
        pass

class Production(ResourceType):
    def __init__(self):
        self.name = 'production'
        self.imagePath = 'sprites/small_gear.png'
        self.image = Image.open(self.imagePath)

    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self,other):
        return isinstance(other, Production)

    def getName(self):
        return self.name
    
    def getImagePath(self):
        return self.imagePath
    
    def getImage(self):
        return self.image
    
class Food(ResourceType):
    def __init__(self):
        self.name = 'food'
        self.imagePath = 'sprites/small_apple.png'
        self.image = Image.open(self.imagePath)

    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self,other):
        return isinstance(other, Food)

    def getName(self):
        return self.name
    
    def getImagePath(self):
        return self.imagePath
    
    def getImage(self):
        return self.image

class ResourceStack:
    ResourceTypes = {'production' : Production(), 'food' : Food()}
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount

    def __repr__(self):
        return f'({self.type.getName()}, {self.amount})'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self,other):
        return isinstance(other, ResourceStack) and self.getType() == other.getType() and self.getAmount == other.getAmount
    
    def getType(self):
        return self.type
    
    def getAmount(self):
        return self.amount
    
    def setAmount(self, amount):
        self.amount = amount