import pygame
import math
import numpy as np
from PIL import Image
import time

from settings import *
from utils import *

class Car:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_INITIAL_POS_X, PLAYER_INITIAL_POS_Y
        self.angle = PLAYER_ANGLE
        self.end_x = 0
        self.end_y = 0
        self.line_length = 0
        self.vel = 0
        self.moved = None
        self.rotated_car = None
        self.car_rect = None
    
    def getIntersection(self, start, end):
        line_points = []
        for t in range(self.line_length):
            t /= self.line_length
            point_x = round(start[0] + t * (end[0] - start[0]))
            point_y = round(start[1] + t * (end[1] - start[1]))
            line_points.append((point_x, point_y))

        for point in line_points:
            if 0 <= point[0] < WIDTH and 0 <= point[1] < HEIGHT:
                pixel_color = TRACK.get_at(point)
                if pixel_color == BLACK:
                    break
        return point

    def movement(self):
        keys = pygame.key.get_pressed()

        self.moved = False

        if keys[pygame.K_LEFT]:
            self.angle += ROTATION_VEL
        if keys[pygame.K_RIGHT]:
            self.angle -= ROTATION_VEL
        if keys[pygame.K_UP]:
            self.vel = MAX_VEL
            self.moved = True

        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        if not self.moved:
            self.vel = 0
    
    def check_collision_wall(self):
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH:
            self.x = WIDTH
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT:
            self.y = HEIGHT

    def check_collision_racetrack(self):
        self.rotated_car = pygame.transform.rotate(RED_CAR, self.angle)
        self.car_rect = self.rotated_car.get_rect(center=(self.x, self.y))

        racetrack_mask = pygame.mask.from_threshold(TRACK, BLACK, (1, 1, 1, 255))
        rotated_car_mask = pygame.mask.from_surface(self.rotated_car)
        offset = (self.car_rect.x, self.car_rect.y)  # basically current pos and displacement

        #check for collisions
        if racetrack_mask.overlap(rotated_car_mask, offset):
            # print("Car hit the black racetrack!")
            return True
        else:
            # print("Car is ok")
            return False

    def draw_intersection_circle(self, point):
        pygame.draw.circle(WIN, (255, 0, 0), point, 5)

    def draw_lines(self):
        self.line_length = 3000
        self.end_x = self.x + self.line_length * -math.cos(math.radians(self.angle) - math.pi / 2)
        self.end_y = self.y - self.line_length * -math.sin(math.radians(self.angle) - math.pi / 2)

        self.end_x2 = self.x + self.line_length * -math.cos(math.radians(self.angle) - math.pi)
        self.end_y2 = self.y - self.line_length * -math.sin(math.radians(self.angle) - math.pi)

        self.end_x3 = self.x + self.line_length * -math.cos(math.radians(self.angle))
        self.end_y3 = self.y - self.line_length * -math.sin(math.radians(self.angle))

        self.end_x4 = self.x + self.line_length * -math.cos(math.radians(self.angle) - math.pi / 4)
        self.end_y4 = self.y - self.line_length * -math.sin(math.radians(self.angle) - math.pi / 4)

        self.end_x5 = self.x + self.line_length * -math.cos(math.radians(self.angle) - 3 * math.pi / 4)
        self.end_y5 = self.y - self.line_length * -math.sin(math.radians(self.angle) - 3 * math.pi / 4)
        
        point1 = self.getIntersection((self.x, self.y), (self.end_x, self.end_y))
        point2 = self.getIntersection((self.x, self.y), (self.end_x2, self.end_y2))
        point3 = self.getIntersection((self.x, self.y), (self.end_x3, self.end_y3))
        point4 = self.getIntersection((self.x, self.y), (self.end_x4, self.end_y4))
        point5 = self.getIntersection((self.x, self.y), (self.end_x5, self.end_y5))

        pygame.draw.line(WIN, (0, 0, 0), (self.x, self.y), point1, 2)
        pygame.draw.line(WIN, (0, 0, 0), (self.x, self.y), point2, 2)
        pygame.draw.line(WIN, (0, 0, 0), (self.x, self.y), point3, 2)
        pygame.draw.line(WIN, (0, 0, 0), (self.x, self.y), point4, 2)
        pygame.draw.line(WIN, (0, 0, 0), (self.x, self.y), point5, 2)

        self.draw_intersection_circle(point1)
        self.draw_intersection_circle(point2)
        self.draw_intersection_circle(point3)
        self.draw_intersection_circle(point4)
        self.draw_intersection_circle(point5)

    def get_state(self):
        return (self.x, self.y, self.vel, self.angle)
    
    def reset_position(self):
        self.x, self.y, self.angle = PLAYER_INITIAL_POS_X, PLAYER_INITIAL_POS_Y, PLAYER_ANGLE

    def termination_condition(self):
        if self.check_collision_racetrack() == True:
            # print("terminate")
            self.reset_position()
            # time.sleep(5)

    def apply_action(self, action):
        if action == 0:
            self.vel = MAX_VEL
            self.moved = True
        if action == 1:
            self.angle += ROTATION_VEL
        if action == 2:
            self.angle -= ROTATION_VEL
        
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        if not self.moved:
            self.vel = 0

    def draw(self):
        WIN.blit(TRACK, (0, 0))
        WIN.blit(self.rotated_car, self.car_rect.topleft)
        self.draw_lines()
        
    def update(self):
        self.movement()
        self.check_collision_wall()
        self.check_collision_racetrack()
        self.termination_condition()
