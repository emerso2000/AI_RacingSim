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

        self.epsilon = 0.1
        self.learning_rate = 0.1
        self.discount_factor = 0.9

        self.q_table = np.zeros((self.num_states, self.num_actions))
        self.state = np.zeros(self.num_states)
        self.action = np.zeros(self.num_actions)
    
    def calculate_reward(self):
        base_reward = 0.1
        collision_penalty = 0.0

        if self.car.check_collision_racetrack():
            collision_penalty = -1.0
        else:
            collision_penalty = 0.0
        
        total_reward = base_reward + collision_penalty

        return total_reward

    def discretize_state(self, state):
        x_bins = np.linspace(0, 1152, num=1)
        y_bins = np.linspace(0, 648, num=1)
        velocity_bins = np.linspace(0, 4, num=1)
        angle_bins = np.linspace(0, 360, num=1)

        x_discretized = np.digitize(state[0], x_bins)
        y_discretized = np.digitize(state[1], y_bins)
        velocity_discretized = np.digitize(state[2], velocity_bins)
        angle_discretized = np.digitize(state[3], angle_bins)

        return (x_discretized, y_discretized, velocity_discretized, angle_discretized)


    def calculate_action(self, state):
        discretized_state = self.discretize_state(state)
        if np.random.rand() < self.epsilon:
            action = np.random.randint(self.num_actions)
        else:
            action = np.argmax(self.q_table[discretized_state, :])
        return action

    def update(self):
        x, y, velocity, angle = self.car.get_state() #in order of x, y, velocity, angle
        self.state[0], self.state[1], self.state[2], self.state[3] = x, y, velocity, angle

        action = self.calculate_action(self.state)
        self.car.apply_action(action)
        next_x, next_y, next_velocity, next_angle = self.car.get_state()
        reward = self.calculate_reward()

        discretized_state = self.discretize_state(self.state)
        discretized_next_state = self.discretize_state((next_x, next_y, next_velocity, next_angle))
        
        print("Discretized Next State:", discretized_next_state)
        # print("Q-table Shape:", self.q_table.shape)
        print(reward)
        # Calculate the Q-value update
        self.q_table[discretized_state, action] += self.learning_rate * (
            reward + self.discount_factor * np.max(self.q_table[discretized_next_state, :]) - self.q_table[discretized_state, action]
        )
