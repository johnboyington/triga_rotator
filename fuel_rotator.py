

import numpy as np

F = open('pos.txt', 'r').readlines()
read = [i[:-1] for i in F]
positions = np.array([(j[17:26], j[28:37]) for j in read]).astype(float)
radius = np.sum((positions**2), axis=1)

