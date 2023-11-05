# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 19:34:01 2023

@author: Charles-Alexis
"""

import pygame

class screen_text:
    def __init__(self, screen, car):
        self.car = car
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.screen = screen

    def update_states_text(self):
        text = self.alive_font.render("States:", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("Vx: " + "{:.2f}".format(self.car.x[0]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 550)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("Vy: " + "{:.2f}".format(self.car.x[1]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 530)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("theta: " + "{:.3f}".format(self.car.x[3]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 510)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("X: " + "{:.2f}".format(self.car.x[4]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("Y: " + "{:.2f}".format(self.car.x[5]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 470)
        self.screen.blit(text, text_rect)
        
    def update_inputs_text(self):
        text = self.alive_font.render("Input:", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 450)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("delta: " + "{:.2f}".format(self.car.u[0]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 470)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("Volt: " + "{:.2f}".format(self.car.u[1]), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 490)
        self.screen.blit(text, text_rect)


    def update_data_text(self):
        text = self.alive_font.render("Data:", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1200, 450)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("Total Traveled Distance: " + "{:.2f}".format(self.car.total_traveled_distance), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1200, 470)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("Turn Traveled Distance: " + "{:.2f}".format(self.car.turn_traveled_distance), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1200, 490)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("Turn completed: " + str(self.car.turn_completed), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1200, 510)
        self.screen.blit(text, text_rect)

        
    def show_debug_corner(self):
        text = self.alive_font.render("(0,0)", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (20, 10)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("(0,1080)", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (30, 1065)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("(1920,0)", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1875, 10)
        self.screen.blit(text, text_rect)
        
        text = self.alive_font.render("(1920,1080)", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1865, 1065)
        self.screen.blit(text, text_rect)