'''
This program will calculate the theta and r values of the fuel element
positions in the TRIGA reactor, then rotate them by a give value.

Output: Two text files to replace the cells and surface cards in the 
original triga model.
'''

import numpy as np

#read in positions from file
F = open('pos.txt', 'r').readlines()
read = [i[:-1] for i in F]
positions = np.array([(j[17:26], j[28:37]) for j in read]).astype(float)

#calculate r and theta
radii = np.sqrt(np.sum((positions**2), axis=1))
theta = np.arctan(positions[:,1] / positions[:,0]) * (180 / np.pi)

#input value to rotate fuel elements by
theta_rotated = 30  #degrees counterclockwise

#calculate new positions
new_theta = theta + theta_rotated
new_positions = (np.array([np.cos(new_theta), np.sin(new_theta)]) * radii).T

