# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 19:46:04 2023

@author: Charles-Alexis
"""

import numpy as np

class reward_function:
    def __init__(self, car):
        self.car = car
        
        self.G_speed = 0
        self.G_turn = 0
        self.G_collision = 10000
        
        self.current_lap = 0
        
    def G_speed_calc(self):
        self.G_speed = np.sqrt((self.car.x[0]**2)+(self.car.x[1]**2))/100

    def G_turn_calc(self):
        if self.current_lap != self.car.turn_completed:
            self.G_turn = 60000 # 60000 * 60hz = 1000 reward pts
            self.current_lap = self.car.turn_completed
        else:
            self.G_turn = 0
            
    def G_collision_calc(self):
        if self.car.si_alive() is False:
            self.G_collsion -= 10000