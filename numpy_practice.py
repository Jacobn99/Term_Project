import numpy as np

a = np.zeros((5,5))
a[:,-1] = 1
a[:, 0] = 1
a[0, :] = 1
a[-1, :] = 1
a[2,2] = 9

b = np.ones((5,5))
b[1:-1, 1:-1] = 0
b[2,2] = 9

print(a)
print(b)