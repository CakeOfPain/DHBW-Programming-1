import pygame
import math
import time
from collections import OrderedDict

width = 200
height = 200
pixel_size = 3
buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]
currentColor = (0, 0, 0)

# camera settings
camera_x = 0
camera_y = 0
camera_z = 0
camera_rx = 0
camera_ry = 0
camera_rz = 0
fov = 600

def drawPixel(x, y, z):
    x = int(x)
    y = int(y)
    if x < 0 or y < 0 or x >= width or y >= height:
        return
    if z >= buffer[y][x][1]:
        fog = 100
        d = 1 - (min(abs(z), fog) / fog)
        buffer[y][x] = ((int(currentColor[0] * d), int(currentColor[1] * d), int(currentColor[2] * d)), z)

def drawLine(x1, y1, z1, x2, y2, z2):

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    interpolation = int(math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)) + 10
    if interpolation == 0: interpolation = 1
    steps = (dx / interpolation, dy / interpolation, dz / interpolation)
    for i in range(0, interpolation+1):
        drawPixel(x1 + steps[0] * i, y1 + steps[1] * i, z1 + steps[2] * i)


def drawTriangle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    
    sx = (x1 + x2 + x3) / 3
    sy = (y1 + y2 + y3) / 3
    sz = (z1 + z2 + z3) / 3

    interpolation1 = math.sqrt((x1 - sx)**2 + (y1 - sy)**2 + (z1 - sz)**2)
    interpolation2 = math.sqrt((x2 - sx)**2 + (y2 - sy)**2 + (z2 - sz)**2)
    interpolation3 = math.sqrt((x3 - sx)**2 + (y3 - sy)**2 + (z3 - sz)**2)
    interpolation = int(max(interpolation1, interpolation2, interpolation3)) + 10
    # interpolation = 2
    steps1 = ((x1 - sx) / interpolation, (y1 - sy) / interpolation, (z1 - sz) / interpolation)
    steps2 = ((x2 - sx) / interpolation, (y2 - sy) / interpolation, (z2 - sz) / interpolation)
    steps3 = ((x3 - sx) / interpolation, (y3 - sy) / interpolation, (z3 - sz) / interpolation)


    for i in range(0, interpolation+1):
        a = (x1 - steps1[0] * i, y1 - steps1[1] * i, z1 - steps1[2] * i)
        b = (x2 - steps2[0] * i, y2 - steps2[1] * i, z2 - steps2[2] * i)
        c = (x3 - steps3[0] * i, y3 - steps3[1] * i, z3 - steps3[2] * i)

        drawLine(a[0], a[1], a[2], b[0], b[1], b[2])
        drawLine(b[0], b[1], b[2], c[0], c[1], c[2])
        drawLine(c[0], c[1], c[2], a[0], a[1], a[2])


class Cube(object):
    def __init__(self, x, y, z, scale) -> None:
        self.lineMode = False
        self.scale = scale
        self.rotation = [0, 0, 0]
        self.x = x
        self.y = y
        self.z = z
        self.resetPoints(scale)
        self.polygons = [
            (0, 2, 4),
            (6, 2, 4),
            (1, 3, 5),
            (7, 3, 5),
            (1, 0, 5),
            (0, 4, 5),
            (2, 3, 7),
            (6, 2, 7),
            (1, 0, 3),
            (2, 0, 3),
            (5, 4, 6),
            (7, 6, 5),
        ]
    def resetPoints(self, scale):
        self.points = [
            (-1 * scale, -1 * scale, -1 * scale), # 0
            (-1 * scale, -1 * scale, 1 * scale), # 1
            (-1 * scale, 1 * scale, -1 * scale), # 2
            (-1 * scale, 1 * scale, 1 * scale), # 3
            (1 * scale, -1 * scale, -1 * scale), # 4
            (1 * scale, -1 * scale, 1 * scale), # 5
            (1 * scale, 1 * scale, -1 * scale), # 6
            (1 * scale, 1 * scale, 1 * scale), # 7
        ]

    def draw(self):
        self.resetPoints(self.scale)

        for i in range(len(self.points)):
            rx, ry, rz = self.rotation
            point = self.points[i]
            x, y, z = point

            x, y = (
                x * math.cos(rz + camera_rz) + y * -math.sin(rz + camera_rz),
                x * math.sin(rz + camera_rz) + y * math.cos(rz + camera_rz),
            )

            # y
            x, z = (
                x * math.cos(ry + camera_ry) + z * -math.sin(ry + camera_ry),
                x * math.sin(ry + camera_ry) + z * math.cos(ry + camera_ry),
            )

            # x
            y, z = (
                y * math.cos(rx + camera_rx) + z * -math.sin(rx + camera_rx),
                y * math.sin(rx + camera_rx) + z * math.cos(rx + camera_rx),
            )

            self.points[i] = (x, y, z)

        for i in range(len(self.polygons)):
            a = self.points[self.polygons[i][0]]
            b = self.points[self.polygons[i][1]]
            c = self.points[self.polygons[i][2]]

            x = self.x + camera_x
            y = self.y + camera_y
            z = self.z + camera_z
            
            # z
            x, y = (
                x * math.cos(camera_rz) + y * -math.sin(camera_rz),
                x * math.sin(camera_rz) + y * math.cos(camera_rz),
            )

            # y
            x, z = (
                x * math.cos(camera_ry) + z * -math.sin(camera_ry),
                x * math.sin(camera_ry) + z * math.cos(camera_ry),
            )

            # x
            y, z = (
                y * math.cos(camera_rx) + z * -math.sin(camera_rx),
                y * math.sin(camera_rx) + z * math.cos(camera_rx),
            )

            ax = (fov * (x + a[0])) / (z + a[2]) + width/2
            ay = (fov * (y + a[1])) / (z + a[2]) + height/2
            bx = (fov * (x + b[0])) / (z + b[2]) + width/2
            by = (fov * (y + b[1])) / (z + b[2]) + height/2
            cx = (fov * (x + c[0])) / (z + c[2]) + width/2
            cy = (fov * (y + c[1])) / (z + c[2]) + height/2
            
            # Out of View
            # if z + a[2] >= 0: continue
            # max_limit = 800;
            # min_limit = -200;
            # if start_x > max_limit || start_y > max_limit || end_x > max_limit || end_y > max_limit) continue;
            # if start_x < min_limit || start_y < min_limit || end_x < min_limit || end_y < min_limit) continue;
            # if start_x == Infinity || start_y === Infinity || end_x === Infinity || end_y === Infinity) continue;
            
            if self.lineMode:
                drawLine(ax,ay,z + a[2],bx,by,z + b[2])
                drawLine(cx,cy,z + c[2],bx,by,z + b[2])
                drawLine(ax,ay,z + a[2],cx,cy,z + c[2],)
                continue
            
            global currentColor
            currentColor = (int(255 * (self.polygons[i][1] / 7)), int(255 * (self.polygons[i][0] / 7)), int(255 * (self.polygons[i][2] / 7)))

            drawTriangle(
                ax,
                ay,
                z + a[2],
                bx,
                by,
                z + b[2],
                cx,
                cy,
                z + c[2]
            )

    def rotateZ(self, phi):
        self.rotation[2] += phi

    def rotateX(self, phi):
        self.rotation[0] += phi

    def rotateY(self, phi):
        self.rotation[1] += phi

pygame.init();

screen = pygame.display.set_mode((width * pixel_size, height * pixel_size))
clock = pygame.time.Clock()
running = True

screen.fill('black')

cube1 = Cube(0, 0, -50, 1)
cube2 = Cube(0, 0, -50, 1)

while running:
    cube2.x = math.cos(time.time()) * 2 - 2
    cube2.y = math.sin(time.time()) * 5
    cube2.z = math.cos(time.time()) * 30 - 50
    cube1.z = math.cos(time.time()-1.5) * 30 - 50
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    currentColor = (255, 255, 255);

    # cube.lineMode = True
    cube1.draw()
    cube1.rotateX(0.01)
    cube1.rotateY(0.01)
    cube1.rotateZ(0.01)
    
    cube2.draw()
    cube2.rotateX(0.05)
    cube2.rotateY(0.02)
    cube2.rotateZ(0.03)
        
    
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP]:
    #     cube.rotateX(0.01)
    # if keys[pygame.K_DOWN]:
    #     cube.rotateX(-0.01)
    # if keys[pygame.K_LEFT]:
    #     cube.rotateY(0.01)
    # if keys[pygame.K_RIGHT]:
    #     cube.rotateY(-0.01)


    for y, row in enumerate(buffer):
        for x, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel[0], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    pygame.display.flip()
    # clear buffer
    buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]

    clock.tick(60)
    # print(clock.get_fps())


pygame.quit();