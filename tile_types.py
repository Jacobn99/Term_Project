from abc import ABC, abstractmethod
from PIL import Image
from sprite import Sprite


class TileType(ABC):
    # emptyTile = Image.open("sprites/TileShape.png")
    # greenTile = Image.open("sprites/green_tile.png")
    # brownTile = Image.open("sprites/brown_tile.png")
    # treeTile = Image.open("sprites/tree_tile.png")
    # defaultSprites = {'empty' : Sprite(emptyTile), 'green_tile': Sprite(greenTile), 'brown_tile' : Sprite(brownTile), 
    #                   'tree_tile' : Sprite(treeTile)}

    @abstractmethod
    def getDefaultSprite(self):
        pass

    @abstractmethod
    def getResourceTable(self):
        pass

class ForestTile(TileType):
    def __init__(self):
        pass

    def getDefaultSprite(self):
        treeTile = Image.open("sprites/tree_tile.png")
        return Sprite(treeTile)
    
    def getResourceTable(self):
        return None
    
class SettlementCenter(TileType):
    def __init__(self):
        pass

    def getDefaultSprite(self):
        brownTile = Image.open("sprites/brown_tile.png")
        return Sprite(brownTile)
    
    def getResourceTable(self):
        return None