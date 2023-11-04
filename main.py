import pygame
import time
import math

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

pygame.init()

RED_CAR = scale_image(pygame.image.load("imgs\\red-car.png"), 0.55)
TRACK = scale_image(pygame.image.load("imgs\\racetrack.png"), 1)
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Racing")

FPS = 60

MAX_VEL = 4
ROTATION_VEL = 4

vel = 0
angle = 0
x, y = 180, 200

run = True
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        angle += ROTATION_VEL
    if keys[pygame.K_RIGHT]:
        angle -= ROTATION_VEL
    if keys[pygame.K_UP]:
        vel = MAX_VEL
        moved = True

    radians = math.radians(angle)
    vertical = math.cos(radians) * vel
    horizontal = math.sin(radians) * vel

    y -= vertical
    x -= horizontal
        
    if not moved:
        vel = 0

    if x < 0:
        x = 0
    if x > WIDTH:
        x = WIDTH
    if y < 0:
        y = 0
    if y > HEIGHT:
        y = HEIGHT

    rotated_car = pygame.transform.rotate(RED_CAR, angle)
    new_rect = rotated_car.get_rect(center=(x, y))

    WIN.blit(TRACK, (0, 0))
    WIN.blit(rotated_car, new_rect.topleft)
    pygame.display.update()

pygame.quit()
