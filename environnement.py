# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:23:41 2023

@author: Charles-Alexis
"""
import pygame
import sys

import car_dynamics
import screen_text as st
import controlers as cont
import reward_function

# INIT GAME
pygame.init()
screen = pygame.display.set_mode((1920, 1080))#, pygame.FULLSCREEN)
clock = pygame.time.Clock()
game_map = pygame.image.load('map.png').convert()

# INIT CAR AND CONTROLER
car_length = 50 #px
car_width = 20 #px

model = 'Kinematics'

if model == 'Dynamics':
    car = car_dynamics.CarFullDynamicBicycleModel(car_length,car_width)
    car_controler = cont.baseline_controler_dynamics(car)
    # INIT SCREEN TEXT UPDATER
    screen_text_updater = st.screen_text_dynamics(screen, car)
if model == 'Kinematics':
    car = car_dynamics.CarSimpleKinematicBicycleModel(car_length,car_width)
    car_controler = cont.baseline_controler_kinematics(car)
    # INIT SCREEN TEXT UPDATER
    screen_text_updater = st.screen_text_kinematics(screen, car)

car.game_map = game_map

# INIT REWARD FUNCTION
rf = reward_function.reward_function(car)


while True:
    # Exit On Quit Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    still_alive = 0
    if car.is_alive() != True:
        break

    # CONTROLER INPUT
    car.create_radars()
    car_controler.c()
    car.radars.clear()
    
    # UPDATE CAR DYNAMICS
    car.update(game_map, car_controler.u)
    
    # CREATE NEW RADARS FOR K+1 AND PRINT
    car.create_radars()
    
    # BLIT SCREEN AND ROTATE + RADARS PRINTING
    screen.blit(game_map, (0, 0))
    car.blitRotateCenter(screen, draw_extra=False)
    car.draw_radar(screen)
    
    # UPDATE SCREEN TEXT
    screen_text_updater.show_debug_corner()
    screen_text_updater.update_inputs_text()
    screen_text_updater.update_states_text()
    screen_text_updater.update_data_text()
    car.radars.clear()
    
    pygame.display.flip()
    clock.tick(60) # 60 FPS
    
pygame.quit()