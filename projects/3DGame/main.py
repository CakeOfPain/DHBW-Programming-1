import pygame
import math

screen_w = 600
screen_h = 600

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
    z = int(z)
    if x < 0 or y < 0 or x >= width or y >= height:
        return
    if z >= buffer[y][x][1]:
        d = 1 # -(min(abs(z), 30) / 30)
        buffer[y][x] = ((int(currentColor[0] * d), int(currentColor[1] * d), int(currentColor[2] * d)), z)

def drawLineY(x1, y1, z1, x2, y2, z2):
    x1 = int((x1 / screen_h) * height)
    x2 = int((x2 / screen_h) * height)
    y1 = int((y1 / screen_w) * width)
    y2 = int((y2 / screen_w) * width)

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    ix1 = min(x1, x2)
    ix2 = max(x1, x2)
    if ix1 < 0 and ix2 < 0: return
    if ix1 > height and ix2 > height: return

    ix1 = ix1 if ix1 >= 0 else 0
    ix2 = ix2 if ix2 <= height else height
    for x in range(ix1, ix2):
        if dx == 0: continue
        y = y1 + dy * (x - x1) // dx
        z = z1 + dz * (x - x1) // dx
        drawPixel(y, x, z)

def drawLine(x1, y1, z1, x2, y2, z2):
    # switching
    switch_value = 160
    if (int(x2 - x1)) > -switch_value and (int(x2 - x1)) < switch_value:
        drawLineY(y1, x1, z1, y2, x2, z2)
        return

    x1 = int((x1 / screen_w) * width)
    x2 = int((x2 / screen_w) * width)
    y1 = int((y1 / screen_h) * height)
    y2 = int((y2 / screen_h) * height)

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    ix1 = min(x1, x2)
    ix2 = max(x1, x2)
    if ix1 < 0 and ix2 < 0: return
    if ix1 > width and ix2 > width: return

    ix1 = ix1 if ix1 >= 0 else 0
    ix2 = ix2 if ix2 <= width else width
    for x in range(ix1, ix2):
        if dx == 0: continue
        y = y1 + dy * (x - x1) // dx
        z = z1 + dz * (x - x1) // dx
        drawPixel(x, y, z)


def fillBottomFlatTriangle(x1, y1, x2, y2, x3, y3):
    invslope1 = (x2 - x1) / (y2 - y1)
    invslope2 = (x3 - x1) / (y3 - y1)

    curx1 = x1
    curx2 = x1

    for scanlineY in range(y1, y2):
        drawLine(int(curx1), scanlineY, 0, int(curx2), scanlineY, 0)
        curx1 += invslope1
        curx2 += invslope2

def fillTopFlatTriangle(x1, y1, x2, y2, x3, y3):
    invslope1 = (x3 - x1) / (y3 - y1)
    invslope2 = (x3 - x2) / (y3 - y2)

    curx1 = x3
    curx2 = x3

    for scanlineY in range(y3, y1):
        drawLine(int(curx1), scanlineY, 0, int(curx2), scanlineY, 0)
        curx1 -= invslope1
        curx2 -= invslope2


def drawTriangle(x1, y1, x2, y2, x3, y3):
    if y2 == y3:
        fillBottomFlatTriangle(x1, y1, x2, y2, x3, y3)
    elif y1 == y2:
        fillTopFlatTriangle(x1, y1, x2, y2, x3, y3)
    else:
        x4, y4 = int(x1 + (float(y2 - y1) / float(y3 - y1)) * (x3 - x1)), y2
        fillBottomFlatTriangle(x1, y1, x2, y2, x4, y4)
        fillTopFlatTriangle(x2, y2, x4, y4, x3, y3)

class Cube(object):
    def __init__(self, x, y, z, scale) -> None:
        self.scale = scale
        self.rotation = [0, 0, 0]
        self.x = x
        self.y = y
        self.z = z
        self.resetPoints(scale)
        self.connections = [
            (0, 2),
            (0, 4),
            (4, 6),
            (6, 2),
            (1, 3),
            (1, 5),
            (5, 7),
            (7, 3),
            (0, 1),
            (4, 5),
            (6, 7),
            (2, 3),
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

        for i in range(len(self.connections)):
            a = self.points[self.connections[i][0]]
            b = self.points[self.connections[i][1]]

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

            start_x = (fov * (x + a[0])) / (z + a[2]) + screen_w/2
            start_y = (fov * (y + a[1])) / (z + a[2]) + screen_h/2
            end_x = (fov * (x + b[0])) / (z + b[2]) + screen_w/2
            end_y = (fov * (y + b[1])) / (z + b[2]) + screen_h/2
            
            # Out of View
            # if z + a[2] >= 0: continue
            # max_limit = 800;
            # min_limit = -200;
            # if start_x > max_limit || start_y > max_limit || end_x > max_limit || end_y > max_limit) continue;
            # if start_x < min_limit || start_y < min_limit || end_x < min_limit || end_y < min_limit) continue;
            # if start_x == Infinity || start_y === Infinity || end_x === Infinity || end_y === Infinity) continue;
            
            drawLine(
                start_x,
                start_y,
                z + a[2],
                end_x,
                end_y,
                z + b[2]
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

cube = Cube(0, 0, -20, 5)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    currentColor = (255, 255, 255);

    cube.draw()
    cube.rotateX(0.01)
    cube.rotateY(0.01)
    cube.rotateZ(0.01)

    # drawTriangle(0, 0, 100, 100, 300, 200)

    for y, row in enumerate(buffer):
        for x, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel[0], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    pygame.display.flip()
    # clear buffer
    buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]

    clock.tick(60)


pygame.quit();