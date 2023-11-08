import pygame
from utils import *

RED_CAR = scale_image(pygame.image.load("imgs\\red-car.png"), 0.55)
TRACK = scale_image(pygame.image.load("imgs\\racetrack.png"), 1)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("AI Racing")

BLACK = (0, 0, 0)
FPS = 60

MAX_VEL = 4
ROTATION_VEL = 4

PLAYER_INITIAL_POS_X = 350
PLAYER_INITIAL_POS_Y = 200

PLAYER_ANGLE = 0