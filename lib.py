'''
@author Pedro Pablo Arriola Jimenez (20188)
@filename bmp_renderer.py
@description: BMP file renderer that works using concepts related
to framebuffers and low level code such as bytes.
'''
import random
import struct
from Vector import V3


# Functions that will be needed to create low level structures.
def char(c):
    # 1 byte character
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes character
    return struct.pack('=h', w)


def dword(dw):
    # 4 bytes character
    return struct.pack('=l', dw)   
    

def color_select(r, g, b):
    '''
    Here we have the rgb spectrum transformed to byte code.
    The order of the inputs are not the way is used to due to difference
    in how Windows OS works with this type of data.
    '''
    return bytes([b, g, r])

# Part of SR4: Flat Shading
def cross(v1, v2):
    return (
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )

def bounding_box(A, B, C):
    coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

    xmin = 999999
    xmax = -999999
    ymin = 999999
    ymax = -999999

    for (x, y) in coords:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    return V3(xmin, ymin), V3(xmax, ymax)

def barycentric(A, B, C, P):
    
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    if abs(cz) < 1:
        return -1, -1, -1
    
    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz 

    return (w, v, u)

def writeBMP( filename, width, height, framebuffer):
        with open(filename, 'bw') as file:
            # Header
            file.write(char('B'))
            file.write(char('M'))

            # file size
            file.write(dword(14 + 40 + height * width * 3))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(width))
            file.write(dword(height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(width * height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(height):
                for x in range(width):
                    file.write(framebuffer[y][x])
            file.close()