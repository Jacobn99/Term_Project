from map_render import MapRenderer
from PIL import Image

class MaterialIcon:
    # iconImgSize = 25
    labelImgSpacing = 10
    def __init__(self,tile, app, imagePath,):
        self.tile = tile
        self.app = app
        self.imagePath = imagePath
        self.img = Image.open(self.imagePath)
        self.imgSize = self.img.size

    def getAmount(self):
        return 1

    def getImageLoc(self):
        tileWidth, tileHeight = self.tile.getSize()
        relativeRow,relativeCol = self.tile.realToRelativeLoc(self.tile.row, self.tile.col, self.app.map,
                                                              self.app.currentViewRow, self.app.currentViewCol)
        
        x,y = self.tile.mapToScreenCords((relativeRow, relativeCol), self.tile.getSize(), 
                                                    (self.app.width, self.app.height), self.app.map.getRenderedMap(), 
                                                    self.app.mapRenderer)
        x = x + tileWidth//2 - self.imgSize[0]//2
        y = y + tileHeight//2 - self.imgSize[1]//2
        return x, y
    
    def getLabelLoc(self, imageX, imageY):
        x = imageX - MaterialIcon.labelImgSpacing
        y = imageY + self.imgSize[0]//2
        return x,y
    