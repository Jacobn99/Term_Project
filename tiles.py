from PIL import Image
import numpy as np
from sprite import Sprite
from resources import ResourceIcon, ResourceStack
from tile_types import *
import random

class Tile():
    # Making references to default tileSprites so that they are cached unless they are modified
    tileShape = Image.open("sprites/TileShape.png")
    greenTile = Image.open("sprites/green_tile.png")
    brownTile = Image.open("sprites/brown_tile.png")
    defaultSprites = {'empty' : Sprite(tileShape), 'green_tile': Sprite(greenTile), 'brown_tile' : Sprite(brownTile)}
    tileTypes = {'forest' : ForestTile()}
    defaultBorderColor = [0,0,0]
    highlightColor = [255,0,0]

    def __init__(self, mapRenderer, row, col, type, sprite = Sprite(tileShape)):
        self.mapRenderer = mapRenderer
        self.col = col # col in map
        self.row = row # row in map
        self.isHighlighted = False
        self.type = type
        self.sprite = sprite
        self.resources = []
        self.resourceIcon = None
        self.civilization = None
        self.settlement = None
        self.movableUnit = None
        self.settlementColorSprite = None
        self.dSettlementColor = [0,0,-20]

        assert(isinstance(self.sprite, Sprite))


        if type != None:
            self.sprite = type.getDefaultSprite()
        # self.settlementColorSprite = Tile.getRecoloredSprite(self.sprite, self.dSettlementColor)

    def __repr__(self):
        return f'Tile(row:{self.row},col:{self.col})'
    
    def __eq__(self,other):
        return isinstance(other, Tile) and self.col == other.col and self.row == other.row

    def __hash__(self):
        return hash(str(self))
    def __lt__(self,other):
        return ((self.row < other.row) or
                ((self.row == other.row)))
    
    def getResources(self):
        return self.resources            
    
    def addResource(self, resourceStack, app):
        for resource in self.resources:
            if resource.getType() == resourceStack.getType():
                resource.setAmount(resource.getAmount() + resourceStack.getAmount())
                return
        
        # print(f'resourceStack:{resourceStack}')
        self.resources.append(resourceStack)
        self.LoadIcon(app)

    def LoadIcon(self,app):
        if self.resourceIcon == None and self.resources != []:
            self.resourceIcon = ResourceIcon(self, app)

    # Changes sprite without making an alias
    def changeSprite(self, newSprite, app, SchangeSettlementprite = False, redraw = False):
        self.sprite = newSprite
        self.settlementColorSprite = Tile.getRecoloredSprite(self, self.sprite, self.dSettlementColor, True)
        # if changeSettlementSprite == False: self.settlementColorSprite = None
        # self.settlementColorSprite = Tile.getRecoloredSprite(self.sprite, self.dSettlementColor)
        if app.map != None and redraw != False: Tile.redrawTile(self, (app.currentViewRow,app.currentViewCol), app.spriteDrawer, (app.width, app.height),
                            app.map, app.mapRenderer)

    def getSprite(self, recolored = True):
        if self.settlement != None and recolored: return self.getRecoloredSprite(self.sprite,self.dSettlementColor)
        else: return self.sprite
    
    def getUnmodifiedSprite(self):
        return self.sprite
    
    def getSize(self):
        return self.sprite.getSize()
    
    def setType(self,type,app):
        self.type = type
        # self.sprite = type.getDefaultSprite()
        self.changeSprite(type.getDefaultSprite(),app, redraw = True)
        self.settlementColorSprite = None

        Tile.implementTypeResources(self,app)

    def getType(self):
        return self.type

    def getRecoloredSprite(self, sprite, dColor, border = True):
        if self.settlementColorSprite == None:
            data = sprite.getData()
            rows, cols = len(data), len(data[0])
            for row in range(rows):
                for col in range(cols):
                    if data[row,col,:3].tolist() != [255,255,255]:
                        for i in range(3):
                            value = int(data[row,col,i])
                            data[row,col,i] = (value + dColor[i])%255
            
            newSprite = Sprite(Image.fromarray(data[:,:,:3], mode = "RGB"))
            # if border: newSprite = self.changeSpriteBorder(newSprite, [0,0,20])

            self.settlementColorSprite = newSprite
        return self.settlementColorSprite

    @staticmethod
    def getRealLoc(relativeRow, relativeCol, map):
        renderedMap = map.getRenderedMap()
        if renderedMap == None: return None
        else:
            tile = renderedMap.tileList[relativeRow, relativeCol]
            return tile.row, tile.col
        
    @staticmethod
    def implementTypeResources(tile,app):
        resourceTable = tile.getType().getResourceTable()
        if resourceTable == None: 
            tile.resourceIcon.deleteIcon()
            return
        for key in tile.getType().getResourceTable():
            index = random.randrange(len(resourceTable))
            amount = resourceTable[key][index]
            if amount > 0:
                tile.addResource(ResourceStack(ResourceStack.ResourceTypes[key], amount),app)


    @staticmethod
    def changeTileBorder(tile, borderColor, app):
        newSprite = Tile.changeSpriteBorder(tile.getSprite(),borderColor)
        tile.changeSprite(newSprite, app)
   
    @staticmethod
    def changeSpriteBorder(sprite, borderColor):
        borderData = Tile.getSpriteByName('empty').getData()
        newSpriteData = sprite.getData()
        rows, cols = len(borderData), len(borderData[0])

        for row in range(rows):
            for col in range(cols):
                if borderData[row,col].tolist()[:3] == Tile.defaultBorderColor[:3]:
                    newSpriteData[row,col] = borderColor


        img = Image.fromarray(newSpriteData, mode = "RGB")
        return Sprite(img)

    @staticmethod
    def getSpriteByName(name):
        if name in Tile.defaultSprites:
            return Tile.defaultSprites[name]
        else: return None

    @staticmethod
    def redrawTile(tile, viewMapLoc, spriteDrawer, screenSize, map, mapRenderer):
        currentViewMapRow, currentViewMapCol = viewMapLoc
        location = Tile.getRelativeLoc(tile.row, tile.col, map)
        if location == None: return
        
        relativeRow, relativeCol = location
        screenX, screenY = Tile.mapToScreenCords((relativeRow, relativeCol), tile.getSize(),screenSize, map.renderedMap, mapRenderer)
        spriteDrawer.drawSprite(tile.getSprite(), screenX, screenY)

    @staticmethod
    def mapToScreenCords(tileMapLoc, tileSize, screenSize, renderedMap, mapRenderer):
        tileWidthHalf = tileSize[0]/2
        tileHeightHalf = tileSize[1]/2
        mapRow,mapCol = tileMapLoc
        startX, startY = mapRenderer.getMapStartLocation(screenSize, tileSize, len(renderedMap.tileList), len(renderedMap.tileList[0]))
        screenX = (mapCol - mapRow) * tileWidthHalf+ startX
        screenY = (mapCol + mapRow) * tileHeightHalf + startY

        return screenX, screenY
    
    @staticmethod
    def changeHighlight(tile, app, viewMapLoc, map, mapRenderer, screenSize, spriteDrawer):
        color = []
        if tile.isHighlighted: color = Tile.defaultBorderColor
        else: color = Tile.highlightColor    

        tile.isHighlighted = not tile.isHighlighted
        Tile.changeTileBorder(tile, color, app)
        Tile.redrawTile(tile, viewMapLoc, spriteDrawer, screenSize, map, mapRenderer)

    @staticmethod
    def getRelativeLoc(row,col, map):
            renderedMap = map.getRenderedMap()
            # print(renderedMap.lowerY, self.row, renderedMap.upperY)
            # print(renderedMap.lowerX, self.col, renderedMap.upperX)
            if (renderedMap.lowerY<=row<renderedMap.upperY) and (renderedMap.lowerX <=col<renderedMap.upperX):
                return row - renderedMap.lowerY, col - renderedMap.lowerX
            else: return None