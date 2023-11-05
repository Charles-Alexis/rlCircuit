# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 20:01:08 2023

@author: Charles-Alexis
"""

class baseline_controler:
    def __init__(self, sys):
        # CAR
        self.sys = sys
        
        # MAX VLUES
        self.max_torque = 150
        self.null_torque = 0
        self.braking_torque = -10
        
        # RADAR DATA
        self.radar_dist_front = 280
        self.radar_dist_lat = 50
        
        # MAX STEER
        self.nascar_steer = -0.03
        self.safe_steer_left = -0.01
        self.safe_steer_right = +0.01
        
        self.u = [0,0]
        
    def c(self):
        self.u = [0,0]
        if self.sys.x[0] < 30:
            self.u[1] = self.max_torque
            
        if self.sys.radars[1][1] < self.radar_dist_front:
            self.u[0] = self.nascar_steer
            self.u[1] = 0
            
        if self.sys.radars[0][1] < self.radar_dist_lat:
            self.u[0] = self.safe_steer_left
            self.u[1] = 0
        
        if self.sys.radars[-1][1] < self.radar_dist_lat:
            self.u[0] = self.safe_steer_right
            self.u[1] = 0
            
            
class random_controler:
    def __init__(self, sys, grid_sys):
        # CAR
        self.sys = sys
        
        # MAX VLUES
        self.max_torque = 1500
        self.null_torque = 0
        self.braking_torque = -1000
        
        # RADAR DATA
        self.radar_dist_front = 280
        self.radar_dist_lat = 50
        
        # MAX STEER
        self.nascar_steer = -0.3
        self.safe_steer_left = -0.1
        self.safe_steer_right = +0.1
        
        self.u = [0,0,0]
        
    def c(self):
        self.u = [0,0,0]
        if self.sys.x[0] < 15:
            self.u[1] = self.max_torque
            self.u[2] = self.max_torque
        if self.sys.radars[1][1] < self.radar_dist_front:
            self.u[1] = self.null_torque
            self.u[2] = self.null_torque
            self.u[0] = self.nascar_steer
        if self.sys.radars[0][1] < self.radar_dist_lat:
            self.u[0] = self.safe_steer_left
            self.u[1] = self.null_torque
            self.u[2] = self.null_torque
        if self.sys.radars[-1][1] < self.radar_dist_lat:
            self.u[0] = self.safe_steer_right
            self.u[1] = self.null_torque
            self.u[2] = self.null_torque            