# -*- coding: utf-8 -*-
'''
Created on 19 jul 2012

@author: Marco Baxemyr
'''
from math import sqrt
import os
import datetime

import pygame
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


def load_image(file_name, convert_alpha=True, colorkey=False):
    """inspired by http://www.linuxjournal.com/article/7694"""
    full_name = os.path.join('images', file_name)
    
    try:
        image = pygame.image.load(full_name)
    except pygame.error, message:
        print "Couldn't load image:", full_name
        raise SystemExit, message
    
    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    
    if colorkey:
        colorkey = image.get_at((0,7))
        image.set_colorkey(colorkey, RLEACCEL)
    
    return image

def load_sound(file_name):
    """inspired by http://www.linuxjournal.com/article/7694"""
    class No_Sound:
        def play(self):
            pass
        def set_volume(self, volume):
            pass
    
    if not mixer:
        return No_Sound()
    
    full_name = os.path.join('audio', file_name)
    if os.path.exists(full_name):
        sound = mixer.Sound(full_name)
        return sound
    else:
        print 'File not found', full_name
        return No_Sound()

def load_font(file_name, font_size):
    full_name = os.path.join('fonts', file_name)
    if os.path.exists(full_name):
        return pygame.font.Font(full_name, font_size)

def get_Percentage(Max, Value):
    fraction = float(Value) / Max
    return fraction
def get_Distance(v1, v2):
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]
    return sqrt(x**2 + y**2)

class Timer(object):
    """ A Timer that can periodically call a given callback
        function.

        After creation, you should call update() with the
        amount of time passed since the last call to update()
        in milliseconds.

        The callback calls will result synchronously during these
        calls to update()
    """
    def __init__(self, interval, callback, oneshot=False):
        """ Create a new Timer.

            interval: The timer interval in milliseconds
            callback: Callable, to call when each interval expires
            oneshot: True for a timer that only acts once
        """
        self.interval = interval
        self.callback = callback
        self.oneshot = oneshot
        self.time = 0
        self.alive = True

    def update(self, time_passed):
        if not self.alive:
            return

        self.time += time_passed
        if self.time > self.interval:
            self.time -= self.interval
            self.callback()

            if self.oneshot:
                self.alive = False



#!/usr/bin/env python2.3
#
#  Automatic Game Scaling Library for pygame
#
#  Allows resize of a Window while scaling the game, keeping the aspect ratio.
#
#  Created by Matthew Mitchell on 13/09/2009.
#  Copyright (c) 2009 Matthew Mitchell. All rights reserved.
#
#Import modules
import sys
import pygame
from pygame.locals import *
def get_resolution(screen,ss,gs): 
        gap = float(gs[0]) / float(gs[1])
        sap = float(ss[0]) / float(ss[1])
        if gap > sap:
                #Game aspect ratio is greater than screen (wider) so scale width
                factor = float(gs[0]) /float(ss[0])
                new_h = gs[1]/factor #Divides the height by the factor which the width changes so the aspect ratio remians the same.
                game_scaled = (ss[0],new_h)
        elif gap < sap:
                #Game aspect ratio is less than the screens.
                factor = float(gs[1]) /float(ss[1])
                new_w = gs[0]/factor #Divides the width by the factor which the height changes so the aspect ratio remians the same.
                game_scaled = (new_w,ss[1])
        else:
                game_scaled = screen.get_size()
        return game_scaled              
class ScaledGame(pygame.Surface):
        game_size = None
        first_screen = None
        screen = None
        fs = False #Fullscreen false to start
        clock = None
        resize = True
        game_gap = None
        game_scaled = None
        title = None
        fps = False
        def __init__(self,title,game_size):
                pygame.init()
                self.title = title
                self.game_size = game_size
                screen_info = pygame.display.Info() #Required to set a good resolution for the game screen
                self.first_screen = (screen_info.current_w, screen_info.current_h - 120) #Take 120 pixels from the height because the menu bar, window bar and dock takes space
                self.screen = pygame.display.set_mode(self.first_screen,RESIZABLE) 
                pygame.display.set_caption(self.title)
                pygame.Surface.__init__(self,self.game_size) #Sets up the Surface for the game.
                self.clock = pygame.time.Clock()
                self.game_gap = (0,0)
        def update(self):
                #Updates screen properly
                win_size_done = False #Changes to True if the window size is got by the VIDEORESIZE event below
                for event in pygame.event.get():
                        if event.type == QUIT:
                                sys.exit()
                        if event.type == VIDEORESIZE:
                                ss = [event.w,event.h]
                                self.resize = True
                                win_size_done = True
                keys = pygame.key.get_pressed() #Get the pressed keys
                if pygame.key.get_mods() == 1024:
                        if(keys[K_q] or keys[K_w]):
                                sys.exit()
                        if keys[K_f]:
                                self.screen = pygame.display.set_mode(self.first_screen,RESIZABLE)
                                if self.fs == False:
                                        self.game_scaled = get_resolution(self.screen,[self.screen.get_width(),self.screen.get_height()],self.game_size)
                                        self.game_gap = [(self.screen.get_width() - self.game_scaled[0])/2,(self.screen.get_height() - self.game_scaled[1])/2]
                                        self.screen = pygame.display.set_mode((0,0), FULLSCREEN | HWSURFACE  | DOUBLEBUF)
                                        self.fs = True
                                else:
                                        self.fs = False
                                        self.resize = True
                                        self.game_gap = (0,0)
                #Scale game to screen resolution, keeping aspect ratio
                if self.resize == True:
                        if(win_size_done == False): #Sizes not gotten by resize event
                                ss = [self.screen.get_width(),self.screen.get_height()]
                        self.game_scaled = get_resolution(self.screen,ss,self.game_size)
                        self.screen = pygame.display.set_mode(self.game_scaled,RESIZABLE)
                self.resize = False #Next time do not scale unless resize or fullscreen events occur
                self.screen.blit(pygame.transform.scale(self,self.game_scaled),self.game_gap) #Add game to screen with the scaled size and gap required.
                pygame.display.flip()
                self.clock.tick(60)
                if self.fps == True:
                        pygame.display.set_caption(self.title + " - " + str(int(self.clock.get_fps())) + "fps")
