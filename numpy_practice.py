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

c = b[b==1]

d = np.hstack([[[1,1], [3,4]], [[5,5], [5,5]]])

e = d.copy()
e = e.reshape((1,8))

g = np.array([100,50,20], dtype= np.int8)

print(a)
print(b)
print(c)
print(d)
print(e)
print(g)


