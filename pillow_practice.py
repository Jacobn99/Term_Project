from PIL import Image
import numpy as np

img1 = Image.new(mode = "RGB", size = (400,300), color = (0,0,100))
a = np.asarray(img1).copy()

print(a[4,50])
a[10:50,:] = (0,100,0)
img1 = Image.fromarray(a, mode = "RGB")
img1.show()

img2 = Image.open("download.jpg")
img2 = img2.crop((0,0, 200, 200))
img2.show()

img3 = img2.copy()
img3 = img3.transpose(Image.FLIP_LEFT_RIGHT)
img3.show()

img4 = Image.open("download.jpg")
img4 = img4.resize((400, 600))
img4.show()

img5 = Image.open("download.jpg")
img5.paste(img1.crop((0,0,50,50)))
img5.show()

img6 = Image.open("download.jpg")
img6 = img6.convert('L')
img6.show()