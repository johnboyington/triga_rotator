'''
This program will calculate the theta and r values of the fuel element
positions in the TRIGA reactor, then rotate them by a give value.

Output: Two text files to replace the cells and surface cards in the 
original triga model.
'''

import numpy as np

#read in positions from file
F = open('pos.txt', 'r').readlines()
surf = [line for line in F]
positions = np.array([(j[17:26], j[28:37]) for j in surf]).astype(float)

#read in positions from file
G = open('pos_cell.txt', 'r').readlines()
cell = [line for line in G]

#calculate r and theta
radii = np.sqrt(np.sum((positions**2), axis=1))
theta = np.arctan(positions[:,1] / positions[:,0]) * (180 / np.pi)

#input value to rotate fuel elements by
theta_rotated = 30  #degrees counterclockwise

#calculate new positions
new_theta = theta + theta_rotated
new_positions = (np.array([np.cos(new_theta), np.sin(new_theta)]) * radii).T


#replace positions values in surface cards with new positions
s = ''
for pos in range(len(new_positions)):
    new_surf = '{}{:.6f}  {:.6f}{}'.format(surf[pos][0:17], new_positions[pos,0], new_positions[pos,1], surf[pos][37:])
    s += new_surf

#write new_surfaces
with open('output/new_surfaces.txt', 'w') as F:
    F.write(s)


#replace positions values in cell cards with new positions
s = ''
for pos in range(len(new_positions)):
    new_cell = '{}{:.6f}  {:.6f}{}'.format(cell[pos][0:37], new_positions[pos,0], new_positions[pos,1], cell[pos][58:])
    s += new_cell

#write new_cells
with open('output/new_cells.txt', 'w') as F:
    F.write(s)
