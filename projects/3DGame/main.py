import pygame
import math
import time

width = 100
height = 100
pixel_size = 5
buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]
currentColor = (0, 0, 0)

textures = pygame.image.load('./res/textures.png')

# camera settings
camera_x = 0
camera_y = 0
camera_z = 0
camera_rx = 0
camera_ry = 0
camera_rz = 0
fov = 300

class Vertex(object):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

class Texture(object):
    def __init__(self, image: pygame.Surface, x1, y1, x2, y2, x3, y3):
        self.image: pygame.Surface = image
        self.x1, self.x2, self.x3 = x1, x2, x3
        self.y1, self.y2, self.y3 = y1, y2, y3


time_start = time.time()

class Triangle(object):
    def __init__(self, a: Vertex, b: Vertex, c: Vertex, texture: Texture):
        self.a = a
        self.b = b
        self.c = c
        self.texture = texture
    def draw(self):
        x1, x2, x3 = self.a.x, self.b.x, self.c.x
        y1, y2, y3 = self.a.y, self.b.y, self.c.y
        z1, z2, z3 = self.a.z, self.b.z, self.c.z
        sx, sy, sz = (x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3, (z1 + z2 + z3) / 3
        interpolation1 = math.sqrt((x1 - sx)**2 + (y1 - sy)**2 + (z1 - sz)**2)
        interpolation2 = math.sqrt((x2 - sx)**2 + (y2 - sy)**2 + (z2 - sz)**2)
        interpolation3 = math.sqrt((x3 - sx)**2 + (y3 - sy)**2 + (z3 - sz)**2)
        interpolation = int(max(interpolation1, interpolation2, interpolation3)) + 10
        # interpolation = int((time.time()- time_start) * 0.1  + 1)
        steps1 = ((x1 - sx) / interpolation, (y1 - sy) / interpolation, (z1 - sz) / interpolation)
        steps2 = ((x2 - sx) / interpolation, (y2 - sy) / interpolation, (z2 - sz) / interpolation)
        steps3 = ((x3 - sx) / interpolation, (y3 - sy) / interpolation, (z3 - sz) / interpolation)
        
        tx, ty = (self.texture.x1 + self.texture.x2 + self.texture.x3) / 3, (self.texture.y1 + self.texture.y2 + self.texture.y3) / 3
        tsteps1 = ((self.texture.x1 - tx) / interpolation, (self.texture.y1 - ty) / interpolation)
        tsteps2 = ((self.texture.x2 - tx) / interpolation, (self.texture.y2 - ty) / interpolation)
        tsteps3 = ((self.texture.x3 - tx) / interpolation, (self.texture.y3 - ty) / interpolation)

        for i in range(0, interpolation+1):
            a = (x1 - steps1[0] * i, y1 - steps1[1] * i, z1 - steps1[2] * i)
            b = (x2 - steps2[0] * i, y2 - steps2[1] * i, z2 - steps2[2] * i)
            c = (x3 - steps3[0] * i, y3 - steps3[1] * i, z3 - steps3[2] * i)

            ta = (self.texture.x1 - tsteps1[0] * i, self.texture.y1 - tsteps1[1] * i)
            tb = (self.texture.x2 - tsteps2[0] * i, self.texture.y2 - tsteps2[1] * i)
            tc = (self.texture.x3 - tsteps3[0] * i, self.texture.y3 - tsteps3[1] * i)

            Line(
                a[0], a[1], a[2], b[0], b[1], b[2],
                self.texture, (ta[0], ta[1], tb[0], tb[1])).draw()
            Line(b[0], b[1], b[2], c[0], c[1], c[2],
                self.texture, (tb[0], tb[1], tc[0], tc[1])).draw()
            Line(c[0], c[1], c[2], a[0], a[1], a[2],
                self.texture, (tc[0], tc[1], ta[0], ta[1])).draw()

def drawPixel(x, y, z):
    x = int(x)
    y = int(y)
    if x < 0 or y < 0 or x >= width or y >= height:
        return
    if z >= buffer[y][x][1]:
        fog = 100
        d = 1 - (min(abs(z), fog) / fog)
        buffer[y][x] = ((int(currentColor[0] * d), int(currentColor[1] * d), int(currentColor[2] * d)), z)

class Line(object):
    def __init__(self, x1, y1, z1, x2, y2, z2, texture: Texture = None, texcoords: tuple[float, float, float, float] = None):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.z1, self.z2 = z1, z2
        self.texture = texture
        self.texcoords = texcoords

    def draw(self):
        global currentColor
        x1, y1, z1 = self.x1, self.y1, self.z1
        x2, y2, z2 = self.x2, self.y2, self.z2

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        tx1, ty1, tx2, ty2 = None, None, None, None
        tdx, tdy = None, None
        if self.texture != None:
            tx1, ty1, tx2, ty2 = self.texcoords
            tdx, tdy  = tx2 - tx1, ty2 - ty1

        interpolation = int(math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)) + 10
        # interpolation = int((time.time() - time_start) + 1)
        if interpolation == 0: interpolation = 1

        steps = (dx / interpolation, dy / interpolation, dz / interpolation)
        tsteps = None
        if self.texture != None:
            tsteps = (tdx / interpolation, tdy / interpolation)
        for i in range(0, interpolation+1):
            if self.texture != None:
                coord = (int(tx1 + tsteps[0] * i), int(ty1 + tsteps[1] * i))
                if(coord[0] >= 0 and coord[1] >= 0):
                    currentColor = self.texture.image.get_at(coord)
            drawPixel(x1 + steps[0] * i, y1 + steps[1] * i, z1 + steps[2] * i)

class Cube(object):
    def __init__(self, x, y, z, scale) -> None:
        self.lineMode = False
        self.scale = scale
        self.rotation = [0, 0, 0]
        self.x = x
        self.y = y
        self.z = z
        self.resetPoints(scale)

        self.textures = [
            Texture(textures, 0, 15, 0, 0, 15, 0),
            Texture(textures, 15, 0, 15, 15, 0, 15),
            Texture(textures, 16, 15, 16, 0, 31, 0),
            Texture(textures, 31, 0, 31, 15, 16, 15),
            Texture(textures, 32, 15, 32, 0, 47, 0),
            Texture(textures, 47, 0, 47, 15, 32, 15),
        ]

        self.polygons = [
            (0, 1, 2, 2),
            (2, 3, 0, 3), # front
            (4, 5, 6, 2),
            (6, 7, 4, 3), # back
            (3, 2, 5, 2),
            (5, 4, 3, 3), # right
            (7, 6, 1, 2),
            (1, 0, 7, 3), # left
            (1, 6, 5, 0),
            (5, 2, 1, 1), # top
            (4, 7, 0, 4),
            (0, 3, 4, 5) # bottom
        ]
    def resetPoints(self, scale):
        self.points = [
            (-scale, scale, scale), # 0
            (-scale, -scale, scale), # 1
            (scale, -scale, scale), # 2
            (scale, scale, scale), # 3
            (scale, scale, -scale), # 4
            (scale, -scale, -scale), # 5
            (-scale, -scale, -scale), # 6
            ((-scale, scale, -scale)), # 7
        ]

    def draw(self):
        global currentColor
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
            texture = self.textures[self.polygons[i][3]]

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


            na = (x + a[0], y + a[1], z + a[2])
            nb = (x + b[0], y + b[1], z + b[2])
            nc = (x + c[0], y + c[1], z + c[2])
            line1 = (nb[0] - na[0], nb[1] - na[1], nb[2] - na[2])
            line2 = (nc[0] - na[0], nc[1] - na[1], nc[2] - na[2])
            normal = [line1[1]*line2[2] - line1[2]*line2[1],
                    line1[2]*line2[0] - line1[0]*line2[2],
                    line1[0]*line2[1] - line1[1]*line2[0]]
            length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
            normal[0] /= length
            normal[1] /= length
            normal[2] /= length

            if (normal[0] * (na[0] - camera_x) +
                normal[1] * (na[1] - camera_y) +
                normal[2] * (na[2] - camera_z)) > 0.0:
                continue

            ax = (fov * (x + a[0])) / (z + a[2]) + width/2
            ay = (fov * (y + a[1])) / (z + a[2]) + height/2
            bx = (fov * (x + b[0])) / (z + b[2]) + width/2
            by = (fov * (y + b[1])) / (z + b[2]) + height/2
            cx = (fov * (x + c[0])) / (z + c[2]) + width/2
            cy = (fov * (y + c[1])) / (z + c[2]) + height/2

            if self.lineMode:
                Line(ax,ay,z + a[2],bx,by,z + b[2]).draw()
                Line(cx,cy,z + c[2],bx,by,z + b[2]).draw()
                Line(ax,ay,z + a[2],cx,cy,z + c[2]).draw()
                continue

            currentColor = (int(255 * (self.polygons[i][1] / 7)), int(255 * (self.polygons[i][0] / 7)), int(255 * (self.polygons[i][2] / 7)))
            vertex1 = Vertex(ax,ay,z + a[2])
            vertex2 = Vertex(bx,by,z + b[2])
            vertex3 = Vertex(cx,cy,z + c[2])
            triangle = Triangle(
                vertex1, vertex2, vertex3,
                texture=texture
            )
            triangle.draw()

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    currentColor = (255, 255, 255)

    cube2.x = math.cos(time.time()) * 2 - 2
    cube2.y = math.sin(time.time()) * 5
    cube2.z = math.cos(time.time()) * 30 - 50
    cube1.z = math.cos(time.time()-1.5) * 30 - 50

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
    #     cube2.rotateX(0.01)
    # if keys[pygame.K_DOWN]:
    #     cube2.rotateX(-0.01)
    # if keys[pygame.K_LEFT]:
    #     cube2.rotateY(0.01)
    # if keys[pygame.K_RIGHT]:
    #     cube2.rotateY(-0.01)


    for y, row in enumerate(buffer):
        for x, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel[0], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    pygame.display.flip()
    # clear buffer
    buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]

    clock.tick(60)
    # print(clock.get_fps())


pygame.quit();