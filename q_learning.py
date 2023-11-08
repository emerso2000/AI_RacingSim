import pygame
import math
import numpy as np
from PIL import Image

from settings import *
from utils import *
from car import *

class Q_learning:
    def __init__(self, game):
        self.game = game
        self.car = Car(self)

        self.num_states = 4
        self.num_actions = 3

        self.q_table = np.zeros((self.num_states, self.num_actions))
    
    def update(self):
        car_state = self.car.get_state()
        x_pos, y_pos, velocity, angle = car_state
        print(x_pos)
        self.termination_condition()

    def termination_condition(self):
        if self.car.check_collision_racetrack() == False:
            print("terminate")
            self.car.reset_position()
        
