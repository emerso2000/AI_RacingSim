import pygame
import time
import math
import numpy as np
from PIL import Image


def getIntersection(x, y, end_x, end_y):
    line_points = []
    for t in range(line_length):
        t /= line_length
        point_x = round(x + t * (end_x - x))
        point_y = round(y + t * (end_y - y))
        line_points.append((point_x, point_y))

    for point in line_points:
        if 0 <= point[0] < WIDTH and 0 <= point[1] < HEIGHT:
            pixel_color = TRACK.get_at(point)
            if pixel_color == BLACK:
                break
    return point

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
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Racing")
BLACK = (0, 0, 0)
FPS = 60

MAX_VEL = 4
ROTATION_VEL = 4

vel = 0
angle = 0
x, y = 400, 200

racetrack_image = Image.open('imgs\\racetrack.png')
racetrack_array = np.array(racetrack_image)
racetrack_binary = (racetrack_array != 0).all(axis=2)  # white is 1, black is 0

black_points = np.argwhere(racetrack_binary == False)

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
    car_rect = rotated_car.get_rect(center=(x, y))

    racetrack_mask = pygame.mask.from_threshold(TRACK, BLACK, (1, 1, 1, 255))
    rotated_car_mask = pygame.mask.from_surface(rotated_car)
    offset = (car_rect.x, car_rect.y)  # basically current pos and displacement

    if racetrack_mask.overlap(rotated_car_mask, offset):
        print("Car hit the black racetrack!")
    else:
        print("Car is ok")

    # draw car and track
    WIN.blit(TRACK, (0, 0))
    WIN.blit(rotated_car, car_rect.topleft)

    line_length = 3000
    end_x = x + line_length * -math.cos(math.radians(angle) - math.pi / 2)
    end_y = y - line_length * -math.sin(math.radians(angle) - math.pi / 2)

    end_x2 = x + line_length * -math.cos(math.radians(angle) - math.pi)
    end_y2 = y - line_length * -math.sin(math.radians(angle) - math.pi)

    end_x3 = x + line_length * -math.cos(math.radians(angle))
    end_y3 = y - line_length * -math.sin(math.radians(angle))

    end_x4 = x + line_length * -math.cos(math.radians(angle) - math.pi / 4)
    end_y4 = y - line_length * -math.sin(math.radians(angle) - math.pi / 4)
    end_x5 = x + line_length * -math.cos(math.radians(angle) - 3 * math.pi / 4)
    end_y5 = y - line_length * -math.sin(math.radians(angle) - 3 * math.pi / 4)

    line_points = []



    pygame.draw.line(WIN, (0, 0, 0), (x, y), getIntersection(x, y, end_x, end_y), 2)
    pygame.draw.line(WIN, (0, 0, 0), (x, y), getIntersection(x, y, end_x2, end_y2), 2)
    pygame.draw.line(WIN, (0, 0, 0), (x, y), getIntersection(x, y, end_x3, end_y3), 2)
    pygame.draw.line(WIN, (0, 0, 0), (x, y), getIntersection(x, y, end_x4, end_y4), 2)
    pygame.draw.line(WIN, (0, 0, 0), (x, y), getIntersection(x, y, end_x5, end_y5), 2)

    pygame.display.update()

pygame.quit()
