from cmath import pi, tan
from lib import *
from Vector import *
from Sphere import *

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_color = color_select(252, 96, 143)
        self.current_color = color_select(255, 255, 255)
        self.scene = []
        self.clear()
        
    def clear(self):    
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
            
        ]
        
    def point(self, x, y, color = None): 
        if (y >= 0 and y < self.height and x >= 0 and x < self.width):
            self.framebuffer[y][x] = color or self.current_color
    
    def render(self):
        
        fov = int(pi / 2)
        aspect_ratio = self.width / self.height
        tana = tan(fov / 2)
        
        
        for y in range(self.height):
            for x in range(self.width):
                
                i = (2 * (x + 0.5) / self.width - 1) * aspect_ratio * tana
                j = (1 - (2 * (y + 0.5) / self.height)) * tana
                
                direction = V3(i, j, -1).norm()
                origin = V3(0, 0, 0)
                
                
                c = self.raycast(origin, direction)
                
                self.point(x, y, c)
    
    def write(self, filename):
        writeBMP(filename, self.width, self.height, self.framebuffer)
        
    def raycast(self, origin, direction, o):
        
        for o in self.scene:
        
            if(o.ray_intersect(origin, direction)):
                return o.get_color()
        
        return self.clear_color
    
    def scene_intersect(self, origin, direction):
        for o in self.scene:
            intersect = self.raycast(origin, direction, o)
            
            if(intersect):
                return color_select(255, 0, 0)
            else:
                return self.clear_color
        

BLACK = color_select(0, 0, 0)
WHITE = color_select(255, 255, 255)
ORANGE = color_select(255, 154, 0)

render = Raytracer(600, 600)
render.scene = [
    # Eyes
    Sphere(V3(0.6, -7, -20), 0.4, BLACK),
    Sphere(V3(-0.6, -7, -20), 0.4, BLACK),
    
    # Nose
    Sphere(V3(0, -6, -20), 0.4, ORANGE),
    
    # Mouth
    Sphere(V3(0, -4.7, -20), 0.2, BLACK),
    Sphere(V3(0.6, -4.9, -20), 0.2, BLACK),
    Sphere(V3(-0.6, -4.9, -20), 0.2, BLACK),
    Sphere(V3(1.2, -5.3, -20), 0.2, BLACK),
    Sphere(V3(-1.2, -5.3, -20), 0.2, BLACK),
    
    # Dots
    Sphere(V3(0, -3, -20), 0.4, BLACK),
    Sphere(V3(0, -1.5, -20), 0.4, BLACK),
    Sphere(V3(0, 0, -20), 0.4, BLACK),
    
    # Body
    Sphere(V3(0, -6, -20), 2, WHITE),
    Sphere(V3(0, -1.7, -20), 3, WHITE),
    Sphere(V3(0, 3.5, -20), 4, WHITE)
    
]

render.render()

render.write('snowman.bmp')