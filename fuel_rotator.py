'''
This program rotate the fuel elements of the TRIGA reactor model 
counterclockwise by a given angle.

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


#input value to rotate fuel elements by
theta_rotated = -30  #degrees counterclockwise


theta_rotated *= (np.pi / 180)

#read in positions from file
F = open('input/pos_surf.txt', 'r').readlines()
surf = [line for line in F]
surf_positions = np.array([(j[16:26], j[27:37]) for j in surf]).astype(float)

#read in positions from file
G = open('input/pos_cell.txt', 'r').readlines()
cell = [line for line in G]
cell_positions = np.array([(j[37:47], j[48:58]) for j in cell]).astype(float)


#replace positions values in surface cards with new positions
s = ''
for pos in range(len(surf_positions)):
    surf_new_positions = rotate((0, 0), surf_positions[pos], theta_rotated)
    new_surf = '{}{:.6f}  {:.6f}{}'.format(surf[pos][0:16], surf_new_positions[0], surf_new_positions[1], surf[pos][37:])
    s += new_surf

#write new_surfaces
with open('output/new_surfaces.txt', 'w') as F:
    F.write(s)


#replace positions values in cell cards with new positions
s = ' 1100     0         -203   fill=4   (  0.000000   0.000000  0.00)  u=7 $ A1\n'
for pos in range(len(cell_positions) - 1):
    cell_new_positions = rotate((0, 0), cell_positions[pos + 1], theta_rotated)
    new_cell = '{}{:.6f}  {:.6f}{}'.format(cell[pos + 1][0:37], cell_new_positions[0], cell_new_positions[1], cell[pos + 1][58:])
    s += new_cell

#write new_cells
with open('output/new_cells.txt', 'w') as F:
    F.write(s)
