# -*- coding: utf-8 -*-
'''
Created on 14 July 2012

@author: Marco Baxemyr
'''

import random
from copy import deepcopy

from pygame import sprite
from pygame import Rect

from utils import *

class Block(sprite.Sprite):
    images = None
    def __init__(self, position, health, create_powerup_method, invulnerable=False, invisible=False):
        sprite.Sprite.__init__(self)
        if Block.images is None:
            #First time the class is instantiated, so load all block images into memory for this and all other instances
            Block.images = [self.load_block_image("lightblue.png"), self.load_block_image("babyblue.png"), self.load_block_image("blue.png"), self.load_block_image("pink.png"), self.load_block_image("purple.png"), self.load_block_image("orange.png"), self.load_block_image("red.png"), self.load_block_image("lightgreen.png"), self.load_block_image("green.png"), self.load_block_image("yellow.png")]
            Block.invulnerable_image = self.load_block_image("invulnerable.png")
            Block.invisible_image = self.load_block_image("invulnerable.png", convert_alpha=False)
            Block.invisible_image.set_alpha(0)
            Block.shattered_image = self.load_block_image("shattered.png", convert_alpha=False, colorkey=True)
        self.orig_health = health
        self.health = health
        self.invulnerable = invulnerable
        self.invisible = invisible
        self.shatter_image = Block.shattered_image.copy()
        self.select_image()
        self.rect = Rect((position[0], position[1]), (self.image.get_width(), self.image.get_height()))
        self.create_powerup = create_powerup_method
        
        
    
    def damage(self, damage=1):
        self.invisible = False
        score_for_hit = self.calculate_score_for_hit(damage)
        if not self.invulnerable:
            self.health -= damage
            if self.health <= 0:
                if self.powerup_dropped():
                    self.create_powerup(self.rect.center) #actually located in game.py
                self.kill() 
            else:
                self.select_image()
        else:
            self.select_image()
        return score_for_hit
    
    def calculate_score_for_hit(self, damage):
        score = 0
        if self.invulnerable:
            return score
        for i in range(damage):
            score += max((self.health - i)*10, 0)
        return score
    
    def powerup_dropped(self):
        """Whether or not a powerup drop occurs"""
        return 4 + self.orig_health * 1.2 >= random.randint(1, 100)
    
    def select_image(self):
        if self.invisible:
            self.image = Block.invisible_image
        elif self.invulnerable:
            self.image = Block.invulnerable_image
        else:
            if self.health <= len(Block.images):
                self.image = Block.images[self.orig_health - 1]
            else:
                self.image = Block.images[-1]
        self.shatter_image.set_alpha(140 - (float(self.health) / self.orig_health) * 140)
        
    def load_block_image(self, block_name, convert_alpha=True, colorkey=False):
        return load_image(os.path.join('blocks', block_name), convert_alpha=convert_alpha, colorkey=colorkey)
    
    def set_invulnerable(self):
        self.invulnerable = True
        self.select_image()
    
    def undo_invulnerable(self):
        self.invulnerable = False
        self.select_image()
        
