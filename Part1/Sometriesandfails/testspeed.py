import math as mt
import numpy as np
import time as t

tid = t.time()
for i in range(1, 1000000):
    x = mt.radians(i)

print(t.time()-tid)

tid = t.time()
for i in range(1, 1000000):
    x = i**0.5

print(t.time()-tid)

tid = t.time()

for i in range(1, 1000000):
    x = np.radians(i)

print(t.time()-tid)

