#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:29:01 2020

@author: selcukkuram
"""
from random import choice 
class RandomWalk:
    def __init__ (self, num_points=10000): 
   
#  Initialize attributes of a walk
        self.num_points = num_points
# All walks start at (0, 0). 􏰂 
        self.x_values = [0]
        self.y_values = [0]

    def get_step(self):
        step = choice([1, -1]) * choice(range(0,5))
        return step
    
    def fill_walk(self):
        while len(self.x_values) < self.num_points:
            x_step = self.get_step() 
            y_step = self.get_step()
            # Calculate the new position.
            x = self.x_values[-1] + x_step 
            y = self.y_values[-1] + y_step
            
            self.x_values.append(x) 
            self.y_values.append(y)