from PIL import Image
import numpy as np
from sprite import SpriteDrawer, Sprite

class MapRenderer:
    # TO-DO: Add map 2d list with data on the tiles
    @staticmethod
    def render(tile, screenSize, mapSize):
        rows, cols = mapSize
        tileWidth, tileHeight = tile.getSize()

        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        middleX = screenWidth//2
        middleY = screenHeight//2

        xEdgeTilesToCenter = middleX//tileWidth
        yEdgeTilesToCenter = middleY//tileHeight

        # Adding tileWidth//2 and tileHeight//2 because programs draws tiles from edge, not center
        startX = middleX-((xEdgeTilesToCenter//2)*tileWidth) + tileWidth//2
        startY = middleY-((yEdgeTilesToCenter//2)*tileHeight) - tileHeight//2

        for row in range(rows):
            # if row*tileHeight>= screenHeight: continue
            for col in range(cols):
                screenX = (row - col) * tileWidth//2;
                screenY = (row + col) * tileHeight//2;
                if 0<=startX + screenX<=screenWidth and 0<=startY + screenY<=screenHeight:
                    tile.drawSprite(startX + screenX, startY + screenY)


        # sprite = Sprite(app.tileImage, app.spriteDrawer)
        # sprite.drawSprite(defaultX + screenX, defaultY + screenY)
