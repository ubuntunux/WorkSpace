# -*- coding: utf-8 -*-
'''
Created on 14 July 2012

@author: Marco Baxemyr
'''

from pygame import sprite
from pygame import Rect
from constants import *

class Paddle(sprite.Sprite):

    def __init__(self, image_surface, position):
        sprite.Sprite.__init__(self)
        self.image = image_surface
        self.rect = Rect((position[0], position[1]), (self.image.get_width(), self.image.get_height()))
        
        
    def update(self, posX, moveToPos=False):
        image_width_halved = self.image.get_width() / 2
        x = self.rect.centerx
        if moveToPos:
            if posX != 0:
                x = max(LEFT_BOUND+image_width_halved, posX)
        else:
            x = max(LEFT_BOUND+image_width_halved, x + posX)
        x = min(RIGHT_BOUND-image_width_halved, x)
        self.rect.centerx = x