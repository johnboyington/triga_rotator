'''
This program will calculate the theta and r values of the fuel element
positions in the TRIGA reactor, then rotate them by a give value.

Output: Two text files to replace the cells and surface cards in the 
original triga model.
'''

import numpy as np
import math

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

#read in positions from file
F = open('input/pos_surf.txt', 'r').readlines()
surf = [line for line in F]
surf_positions = np.array([(j[16:26], j[27:37]) for j in surf]).astype(float)

#read in positions from file
G = open('input/pos_cell.txt', 'r').readlines()
cell = [line for line in G]
cell_positions = np.array([(j[37:47], j[48:58]) for j in cell]).astype(float)

#calculate r and theta
cell_radii = np.sqrt(np.sum((cell_positions**2), axis=1))
cell_theta = np.arctan(cell_positions[:,1] / cell_positions[:,0]) * (180 / np.pi)
#for num in range(len(cell_radii)):
#    if cell_positions[num, 1] < 0 or cell_positions[num, 1] == 0 and cell_positions[num, 0] < 0:
#        cell_theta[num] += 180

for angle in cell_theta:
    print angle
#input value to rotate fuel elements by
theta_rotated = 0  #degrees counterclockwise

#calculate new positions
cell_new_theta = (cell_theta + theta_rotated) * (np.pi / 180)
cell_new_positions = (np.array([np.cos(cell_new_theta), np.sin(cell_new_theta)]) * cell_radii).T

#calculate r and theta for surf
surf_radii = np.sqrt(np.sum((surf_positions**2), axis=1))
surf_theta = np.arctan(surf_positions[:,1] / surf_positions[:,0]) * (180 / np.pi)
for num in range(len(surf_radii)):
    if surf_positions[num, 1] < 0 or surf_positions[num, 1] == 0 and surf_positions[num, 0] < 0:
        surf_theta[num] += 180


#calculate new positions
surf_new_theta = (surf_theta + theta_rotated) * (np.pi / 180)
surf_new_positions = (np.array([np.cos(surf_new_theta), np.sin(surf_new_theta)]) * surf_radii).T


#replace positions values in surface cards with new positions
s = ''
for pos in range(len(surf_new_positions)):
    new_surf = '{}{:.6f}  {:.6f}{}'.format(surf[pos][0:16], surf_new_positions[pos,0], surf_new_positions[pos,1], surf[pos][37:])
    s += new_surf

#write new_surfaces
with open('output/new_surfaces.txt', 'w') as F:
    F.write(s)


#replace positions values in cell cards with new positions
s = ' 1100     0         -203   fill=4   (  0.000000   0.000000  0.00)  u=7 $ A1\n'
for pos in range(len(cell_new_positions) - 1):
    new_cell = '{}{:.6f}  {:.6f}{}'.format(cell[pos + 1][0:37], cell_new_positions[pos + 1,0], cell_new_positions[pos + 1,1], cell[pos + 1][58:])
    s += new_cell

#write new_cells
with open('output/new_cells.txt', 'w') as F:
    F.write(s)
