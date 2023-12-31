import pygame
import time
import math
import numpy as np
from PIL import Image
import pygame as pg

from car import *
from settings import *
from utils import *
from q_learning import *

class Game:
    def __init__(self):
        pg.init()
        self.new_game()
        
    def new_game(self):
        self.car = Car(self)
        self.q_learning = Q_learning(self, self.car)

    def update(self):
        self.car.update()
        self.q_learning.update()
        pg.display.flip()

    def draw(self):
        self.car.draw()

    def run(self):
        run = True
        clock = pygame.time.Clock()

        episode_count = 50

        for episode in range(episode_count):
            self.new_game()

            while run:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                self.update()
                self.draw()
                pygame.display.update()

                if self.car.check_collision_racetrack():
                    break

            self.q_learning.update()

            if episode % 100 == 0:
                print(f"Episode {episode} complete")

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
