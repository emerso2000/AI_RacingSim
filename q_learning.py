import pygame
import math
import numpy as np
from PIL import Image

from settings import *
from utils import *
from car import *

class Q_learning:
    def __init__(self, game, car):
        self.game = game
        self.car = car
        self.num_states = 4
        self.num_actions = 3

        self.q_table = np.zeros((self.num_states, self.num_actions))
    
    def update(self):
        x, y, velocity, angle = self.car.get_state()
        # print(x)
        self.termination_condition()
        
    def termination_condition(self):
        if self.car.check_collision_racetrack() == True:
            print("terminate")
            self.car.reset_position()
