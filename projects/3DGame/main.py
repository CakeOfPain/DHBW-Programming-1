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

    drawPixel(random.randint(0, width), random.randint(0, height), 0)

    for y, row in enumerate(buffer):
        for x, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel[0], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    pygame.display.flip()
    # clear buffer
    # buffer = [[((0, 0, 0), -99999)] * width for _ in range(height)]

    clock.tick(60)


pygame.quit();