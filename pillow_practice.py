from PIL import Image
import numpy as np

img = Image.new(mode = "RGB", size = (400,300), color = (0,0,100))
a = np.asarray(img).copy()

print(a[4,50])
a[10:50,:] = (0,100,0)
img = Image.fromarray(a, mode = "RGB")
img.show()
