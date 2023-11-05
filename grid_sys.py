# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 00:28:59 2023

@author: Charles-Alexis
"""

import math

class grid_sys:
    def __init__(self):
        self.x_lb = [0,0,-math.pi,-math.pi,0,0,0]
        self.x_ub = [ 30, 5, math.pi, math.pi, 192, 108, 1000]
        self.u_lb = [-0.05, -100]
        self.u_ub = [0.05, 200]
        
        self.x_dim = [151, 51, 101, 101, 1920, 1080, 501]
        self.u_dim = [11,11]