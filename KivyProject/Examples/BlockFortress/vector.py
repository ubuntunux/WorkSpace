# -*- coding: utf-8 -*-
'''
Created on 15 jul 2012

@author: Marco Baxemyr
'''
import math
from pygame import Rect

class Vector(object):
    '''
    A class to represent two-dimensional vectors
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_length(self):
        return math.sqrt(self.x*self.x+self.y*self.y)
    
    def get_normalized(self):
        if (self.get_length() != 0):
            return self * (1.0 / self.get_length())
    
    def neg(self):
        return Vector(-self.x, -self.y)
    
    def dot(self, other):
        return self.x * other.get_x() + self.y * other.get_y()
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.get_x(), self.y + other.get_y())
        elif hasattr(other, "__getitem__"):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return Vector(self.x + other, self.y + other)
        
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.get_x(), self.y - other.get_y())
        elif hasattr(other, "__getitem__"):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other, self.y - other)
        
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.get_x(), self.y * other.get_y())
        elif hasattr(other, "__getitem__"):
            return Vector(self.x * other[0], self.y * other[1])
        else:
            return Vector(self.x * other, self.y * other)

    def __str__(self):
        return str(self.x) + ", " + str(self.y)
