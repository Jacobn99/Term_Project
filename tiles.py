from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite


class Tile:
    # Making references to default tileSprites so that they are cached unless they are modified
    img1 = Image.open("sprites/TileShape.png")
    defaultSprites = {'empty' : Sprite(img1)}
    defaultBorderColor = [0,0,0]

    def __init__(self, sprite):
        self.sprite = sprite

    # Changes sprite without making an alias
    def changeSprite(self, newSprite):
        self.sprite = newSprite

    def getSprite(self):
        return self.sprite
    
    def getSize(self):
        print(self.sprite.getSize())
        return self.sprite.getSize()
    
    @staticmethod
    def changeTileBorder(tile, borderColor):
        borderData = Tile.getSpriteByName('empty').getData()
        newSpriteData = tile.getSprite().getData()
        rows, cols = len(borderData), len(borderData[0])

        for row in range(rows):
            for col in range(cols):
                if borderData[row,col].tolist()[:3] == Tile.defaultBorderColor[:3]:
                    newSpriteData[row,col] = borderColor


        img = Image.fromarray(newSpriteData, mode = "RGB")
        tile.changeSprite(Sprite(img))
        
    @staticmethod
    def getSpriteByName(name):
        if name in Tile.defaultSprites:
            return Tile.defaultSprites[name]
        else: return None