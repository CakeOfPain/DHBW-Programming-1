import pygame
import random

screen_w = 600
screen_h = 600

width = 200
height = 200
pixel_size = 3
buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]
currentColor = (0, 0, 0)


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
    # switch_value = 30
    # if (int(x2 - x1)) > -switch_value and (int(x2 - x1)) < switch_value:
    #     drawLineY(y1, x1, z1, y2, x2, z2)
    #     return

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

pygame.init();


screen = pygame.display.set_mode((width * pixel_size, height * pixel_size))
clock = pygame.time.Clock()
running = True

screen.fill('black')
while running:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    currentColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255));

    drawLine(random.randint(0, screen_w), random.randint(0, screen_h), 0, random.randint(0, screen_w), random.randint(0, screen_h), 0)

    for y, row in enumerate(buffer):
        for x, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel[0], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    pygame.display.flip()
    # clear buffer
    # buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]

    clock.tick(60)


pygame.quit();