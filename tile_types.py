from abc import ABC, abstractmethod
from PIL import Image
from sprite import Sprite

class TileType(ABC):
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
        return {'production' : [1,2,2,2,3], 'food' : [0,1,1,1,2,2]}
    
class GrassTile(TileType):
    def __init__(self):
        pass

    def getDefaultSprite(self):
        treeTile = Image.open("sprites/grass_tile.png")
        return Sprite(treeTile)
    
    def getResourceTable(self):
        return {'production' : [1,1,0,0], 'food' : [1,2,2,2,3]}
    
class RockTile(TileType):
    def __init__(self):
        pass

    def getDefaultSprite(self):
        treeTile = Image.open("sprites/rock_tile.png")
        return Sprite(treeTile)
    
    def getResourceTable(self):
        return {'production' : [1,2,2,3,3], 'food' : [0,0,1,1,2]}
    
class SettlementCenter(TileType):
    def __init__(self):
        pass

    def getDefaultSprite(self):
        brownTile = Image.open("sprites/brown_tile.png")
        return Sprite(brownTile)
    
    def getResourceTable(self):
        return None