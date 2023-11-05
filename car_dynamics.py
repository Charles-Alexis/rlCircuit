# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 16:11:29 2023

@author: Charles-Alexis
"""

import pygame
import numpy as np
import matplotlib.pyplot as plt
import math

import advanced_vehicles
import reward_function

BORDER_COLOR = (255, 255, 255, 255) # Color To Crash on Hit

class Car:
    def __init__(self,car_size_x = 50, car_size_y = 20):
        # INIT CAR DATA
        self.car_size_x = car_size_x
        self.car_size_y = car_size_y
        self.model = advanced_vehicles.FullDynamicBicycleModelwithVoltInput()
        
        # INIT STATES FOR GAME
        self.center = [830 + self.car_size_x / 2, 920 + self.car_size_y / 2]
        self.angle = 0
        self.speed = 0
        
        # INIT STATES AND INPUTS
        self.x_label = ['v_x','v_y','dtheta','theta','X','Y','omega_f']
        self.x = [0,0,0,0,self.pixel2m(self.center[0]),self.pixel2m(self.center[1]),5/0.3]
        self.u_label = ['delta', 'V',]
        self.u = np.zeros(2)
        
        # INIT SPRITE
        self.sprite = pygame.image.load('car.png').convert() # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (self.car_size_x, self.car_size_y))
        self.rotated_sprite = self.sprite 

        # INIT SIM PARAM        
        self.dt = (1/60) #60 Hz
        self.radars = [] # List For Sensors / Radars
        self.alive = True # Boolean To Check If Car is Crashed
        self.turn_traveled_distance = 0
        self.total_traveled_distance = 0
        self.turn_completed = 0
        

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def create_radars(self):
        self.check_radar(-90, self.game_map)
        self.check_radar(0, self.game_map)
        self.check_radar(90, self.game_map)

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (math.degrees(-self.angle) + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (math.degrees(-self.angle) + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (math.degrees(-self.angle) + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (math.degrees(-self.angle) + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map, u):
        self.game_map = game_map
        self.u = u
        
        self.dx = self.model.f(self.x, self.u)
        self.x  = self.x + self.dx*self.dt
        
        self.angle_correction()
        
        self.angle = self.x[3]
        self.center[0] = self.m2pixel(self.x[4])
        self.center[1] = self.m2pixel(self.x[5])

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * self.car_size_x
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(self.game_map)

        # CALCULATE TRAVELED DISTANCE
        self.calculate_total_distance()
        self.check_turn_completed()
        
    def angle_correction(self):
        if self.x[2] < -math.pi:
            self.x[2] += (2*math.pi)
        if self.x[2] > math.pi:
            self.x[2] -= (2*math.pi)

        if self.x[3] < -math.pi:
            self.x[3] += (2*math.pi)
        if self.x[3] > math.pi:
            self.x[3] -= (2*math.pi)
            
    def is_alive(self):
        # Basic Alive Function
        return self.alive

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, math.degrees(-angle))
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        
        return rotated_image
    
    def pixel2m(self, pixel):
        return pixel/10
        
    def m2pixel(self, m):
        return m*10        
        
    def check_turn_completed(self):
        if self.game_map.get_at((int(self.center[0]), int(self.center[1]))) != (0,0,0,255) and self.turn_traveled_distance > 250:
            self.turn_completed += 1
            self.turn_traveled_distance = 0

    def calculate_total_distance(self):
        instant_dist = self.calculate_instant_distance()
        self.turn_traveled_distance += instant_dist
        self.total_traveled_distance += instant_dist
        
    def calculate_instant_distance(self):
        dx = self.x[0] * self.dt
        dy = self.x[1] * self.dt
        return np.sqrt((dx**2) + (dy**2))
        
    def blitRotateCenter(self, surf, draw_extra = True):
        rotated_image = pygame.transform.rotate(self.sprite, math.degrees(-self.angle))
        new_rect = rotated_image.get_rect(center = self.sprite.get_rect(topleft = self.center).center)
        new_rect = rotated_image.get_rect(center = self.center)
    
        surf.blit(rotated_image, new_rect)
        if draw_extra:
            pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)
        
        if draw_extra:
            opp_x = 100 * math.sin(-self.angle+math.radians(90))
            opp_y = 100 * math.cos(-self.angle+math.radians(90))
            pygame.draw.line(surf, (0, 255, 0), (new_rect.center), (new_rect.center[0] + opp_x, new_rect.center[1] + opp_y), 3)
    
        
        
                
        
        
    