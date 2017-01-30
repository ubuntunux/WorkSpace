# -*- coding: utf-8 -*-

'''
Created originally for PyTowerDefense (http://sourceforge.net/projects/pytowerdefense, an earlier project of mine)

TextWidgets class borrowed from http://www.learningpython.com/2006/12/13/textwidget-a-simple-text-class-for-pygame/

The render_textrect function is borrowed from http://www.pygame.org/pcr/text_rect/index.php

ImageButton and TextMessage are also my own (albeit old) creations.
'''

import os
import sys
import random
import math

import pygame
from pygame import Rect, Color
from pygame.locals import *
from itertools import chain

from utils import load_image, load_font
class WidgetError(Exception): pass
class LayoutError(WidgetError): pass


def UserConfirm(screen, message="Are You Sure?", backgroundclass=None):
    """Written originally for PyTowerDefense (http://sourceforge.net/projects/pytowerdefense/), an earlier project of mine""" 
    global confirmed, rejected
    confirmed, rejected = False, False
    def confirm():
        global confirmed
        confirmed = True
        return
    def reject():
        global rejected
        rejected = True
        return
    text_widgets = []
    if backgroundclass:
        overlay_sf = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay_sf.fill(Color(10, 10, 10))
        overlay_sf.set_alpha(220)
        screen.blit(overlay_sf, (0,0))
    else: screen.fill((0,0,0))
    message_text = TextWidget(message, (130, 40, 0), size=32, highlight_increase=0, font_filename='audiowide.ttf', show_highlight_cursor=False, event=None)
    message_text.rect.center = screen.get_rect().center
    message_text.rect.top -= 50
    text_widgets.append(message_text)

    image_buttons = []

    confirmrect = Rect(screen.get_rect().center[0]-96-60, screen.get_rect().center[1]+50, 100, 100)
    confirm_button = ImageButton(screen, ['confirm.png', 'confirm_full.png'], confirmrect, callback=confirm)
    image_buttons.append(confirm_button)

    rejectrect = Rect(screen.get_rect().center[0]+60, screen.get_rect().center[1]+50, 100, 100)
    reject_button = ImageButton(screen, ['reject.png', 'reject_full.png'], rejectrect, callback=reject)
    image_buttons.append(reject_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in image_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    confirm()
                elif event.key == pygame.K_ESCAPE:
                    reject()

        if confirmed:
            return True
        elif rejected:
            return False

        for button in image_buttons:
            if button.dirty == True:
                if backgroundclass:
                    backgroundclass.draw(update=False)
                    screen.blit(overlay_sf, (0,0))
                    for text in text_widgets:
                        text.dirty = True
                    break
                else:
                    pygame.draw.rect(screen, (0,0,0), button.maxrect)

        for button in image_buttons:
            button.update()

        """Draw everything"""
        for text in text_widgets:
            text.draw(screen)
        pygame.display.update()


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, screen, image, rect, callback, hover_increase=12):
        """
        Takes 5 arguments:
        screen: pygame surface to blit on.
        image: image of the button. Either path to one, or a list of two paths. If a list, the second item will be shown when hovered by the mouse.
        rect: rect to blit on
        callback: Function to call when clicked
        hover_increase: Only applicable if there is only one image. Defaults to 12, which makes the button 12 pixels larger in both directions when hovered by the mouse.
        """
        self.screen = screen
        self.hover_increase = hover_increase
        self.imageset = []
        if image.__class__ == "".__class__:
            self.imageset = [load_image(image), self.generate_hover_pic(load_image(image))] #self.generate_hover_pic(pygame.image.load(image)).convert_alpha()]
        elif image.__class__ == self.imageset.__class__ and image[0].__class__ == "".__class__ and image[1].__class__ == "".__class__:
            self.imageset = [load_image(image[0]), load_image(image[1])]
        else:
            print "ImageButton image has to be either the path to one image or a list of two paths."
        self.maxrect = Rect(rect.left, rect.top, self.imageset[1].get_size()[0], self.imageset[1].get_size()[1])
        self.rect = rect
        self.callback = callback
        self.clicked = False
        self.dirty = False
        self.lastsize = None

    def smoothscale_to_half(self, image):
        return pygame.transform.smoothscale(image, (image.get_size()[0]/ 2, image.get_size()[1] / 2))

    def generate_hover_pic(self, image):
        return pygame.transform.scale(image, (int(image.get_size()[0]+self.hover_increase), int(image.get_size()[1]+self.hover_increase)))

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.imageset[1], self.rect)
            if self.lastsize != "hover":
                self.dirty = True
                self.lastsize = "hover"
        else:
            self.screen.blit(self.imageset[0], self.rect)
            if self.lastsize != "normal":
                self.dirty = True
                self.lastsize = "normal"
        if self.clicked:
            self.callback()
            self.clicked = False

class TextMessage(object):
    def __init__(self, screen, text, pos, duration=1000, size=12, flashy=True, initialdelay=200, color=(130, 40, 0)):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.color = color
        self.font = load_font("audiowide.ttf", self.size)
        self.font.set_bold(True)
        self.textstring = text
        self.text = self.font.render(text, True, color)
        self.duration = duration
        self.initialdelay = initialdelay
        self.flashy = flashy
        self.timealive = 0 #ms
        self.lastactiontime = 0 #ms
        if duration > 0:
            self.sizereductionperaction = ((size / 1.9) / duration) * 50.
            if self.sizereductionperaction >= 0.5 or self.sizereductionperaction <= 1:
                self.sizereductionperaction = 1
            else:
                self.sizereductionperaction = round(self.sizereductionperaction)

        self.xdirection = random.choice([-1, 1])
    def update(self, time_passed):
        self.timealive += time_passed
        if self.timealive - 200 > self.lastactiontime and self.flashy and self.timealive > self.initialdelay:
            self.pos.y -= 4
            self.pos.x += 2 * self.xdirection
            self.size -= self.sizereductionperaction
            self.font = load_font("audiowide.ttf", self.size)
            self.font.set_bold(True)
            self.text = self.font.render(self.textstring, True, self.color)
    def draw(self):
        self.screen.blit(self.text, (self.pos.get_x() - (self.text.get_width() / 2) , self.pos.get_y() - (self.text.get_height() / 2)))
        return Rect(self.pos.get_x() - (self.text.get_width() / 2 + 50) , self.pos.get_y() - (self.text.get_height() / 2 + 40), self.text.get_width() + 100, self.text.get_height() + 80)

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color=(0,0,0), justification=0, background=None): #From http://www.pygame.org/pcr/text_rect/index.php, modified to allow for custom background
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified
    background - override background_color with a custom background surface
    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    
    if not background:
        surface.fill(background_color)
    else:
        surface.blit(background, (0,0), rect)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface



class TextWidget(object): #Courtesy of Mark Mruss, released under the LGPL License.
    """This is a helper class for handling text in PyGame.  It performs
    some basic highlighting and tells you when the text has been clicked.
    This is just one of the many ways to handle your text.
    This is a new-style class and I am somewhat new to them so hopefully it
    all works.
    """
    #Event
    TEXT_WIDGET_CLICK = pygame.locals.USEREVENT
    #Hand Cursor
    __hand_cursor_string = (
    "     XX         ",
    "    X..X        ",
    "    X..X        ",
    "    X..X        ",
    "    X..XXXXX    ",
    "    X..X..X.XX  ",
    " XX X..X..X.X.X ",
    "X..XX.........X ",
    "X...X.........X ",
    " X.....X.X.X..X ",
    "  X....X.X.X..X ",
    "  X....X.X.X.X  ",
    "   X...X.X.X.X  ",
    "    X.......X   ",
    "     X....X.X   ",
    "     XXXXX XX   ")
    __hcurs, __hmask = pygame.cursors.compile(__hand_cursor_string, ".", "X")
    __hand = ((16, 16), (5, 1), __hcurs, __hmask)
    #Text
    def __get_text(self):
        return self.__m_text
    def __set_text(self, text):
        if (self.__m_text != text):
            self.__m_text = text
            self.update_surface()
    def __del_text(self):
        del self.__m_text
    def __doc_text(self):
        return "The text to be displayed by the text widget"
    text = property(__get_text, __set_text, __del_text, __doc_text)
    #Colour
    def __get_colour(self):
        return self.__m_colour
    def __set_colour(self, colour):
        if (self.__m_colour != colour):
            self.__m_colour = colour
            self.update_surface()
    colour = property(__get_colour, __set_colour)
    #Size
    def __get_size(self):
        return self.__m_size
    def __set_size(self, size):
        if (self.__m_size != size):
            self.__m_size = size
            self.create_font()
    size = property(__get_size, __set_size)
    #Font Filename
    def __get_font_filename(self):
        return self.__m_font_filename
    def __set_font_filename(self, font_filename):
        if (self.__m_font_filename != font_filename):
            self.__m_font_filename = font_filename
            self.create_font()
    font_filename = property(__get_font_filename, __set_font_filename)
    #Highlight
    def __get_highlight(self):
        return self.__m_highlight
    def __set_highlight(self, highlight):
        if (not(self.__m_highlight == highlight)):
            #Save the bold_rect
            if (self.__m_highlight):
                self.bold_rect = self.rect
            self.__m_highlight = highlight
            #update the cursor
            self.update_cursor()
            if (highlight):
                self.size += self.highlight_increase
            else:
                self.size -= self.highlight_increase
            if (self.highlight_increase == 0):
                self.create_font()
    highlight = property(__get_highlight, __set_highlight)
    #Show Highlight Cursor
    def __get_highlight_cursor(self):
        return self.__m_highlight_cursor
    def __set_highlight_cursor(self, highlight_cursor):
        if (self.__m_highlight_cursor != highlight_cursor):
            self.__m_highlight_cursor = highlight_cursor
            self.update_cursor()
    highlight_cursor = property(__get_highlight_cursor, __set_highlight_cursor)

    def __init__(self, text="", colour=(0,0,0), size=32
                , highlight_increase = 10, font_filename=None
                , show_highlight_cursor = True, event=TEXT_WIDGET_CLICK, bold=False):
        """Initialize the TextWidget
        @param text = "" - string - The text for the text widget
        @param colour = (0,0,0) - The colour of the text
        @param size = 32 - number - The size of the text
        @param highlight_increase - number - How large do we want the
        text to grow when it is highlighted?
        @param font_filename = None - string the patht to the font file
        to use, None to use the default pygame font.
        @param show_highlight_cursor = True - boolean - Whether or not to change
        the cursor when the text is highlighted.  The cursor will turn into
        a hand if this is true.
        """

        #inits
        self.dirty = False
        self.bold_rect = None
        self.highlight_increase = highlight_increase
        self.tracking = False
        self.rect = None
        self.event = event
        self.bold = bold

        #Get the local path
        self.__local_path = os.path.realpath(os.path.dirname(__file__))

        #property inits
        self.__m_text = None
        self.__m_colour = None
        self.__m_size = None
        self.__m_font_filename = None
        self.__m_highlight = False
        self.__m_font = None
        self.__m_highlight_cursor = False
        self.__m_rect = None

        self.text = text
        self.colour = colour
        self.font_filename = font_filename
        self.size = size
        self.highlight = False
        self.highlight_cursor = show_highlight_cursor

        self.create_font()

    def __str__(self):
        return "TextWidget: %s at %s" % (self.text, self.rect)

    def update_cursor(self):
        if (self.highlight_cursor):
            if (self.highlight):
                pygame.mouse.set_cursor(*self.__hand)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def create_font(self):
        """Create the internal font, using the current settings
        """
        if (self.size):
            try:
                self.__m_font = load_font(self.font_filename, self.size)
            except Exception, e:
                print("Error creating font: '%s' using file: '%s'" % (str(e), self.font_filename))
                print("Trying with default font")
                self.__m_font = pygame.font.Font(None, self.size)

            self.update_surface()

    def update_surface(self):
        """Update the current surface, basically render the
        text using the current settings.
        """
        if (self.__m_font):
            if self.bold: self.__m_font.set_bold(self.highlight)
            self.image = self.__m_font.render(self.text
                , True
                , self.colour)
            self.dirty = True
            if (self.rect):
                # Used the current rects center point
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.rect = self.image.get_rect()

    def draw(self, screen):
        """Draw yourself text widget
        @param screen - pygame.Surface - The surface that we will draw to
        @returns - pygame.rect - If drawing has occurred this is the
        rect that we drew to.  None if no drawing has occurerd."""

        rect_return = None
        if ((self.image)  and  (self.rect) and (self.dirty)):
            if (self.bold_rect):
                """We may need to overwrite the bold text size
                This gets rid of leftover text when moving from
                bold text to non-bold text.
                """
                rect_return = pygame.Rect(self.bold_rect)
                """Set to None, since we only need to do this
                once."""
                self.bold_rect = None
            else:
                rect_return = self.rect
            #Draw the text
            screen.blit(self.image, self.rect)
            #Dirty no more
            self.dirty = False
            return rect_return

    def on_mouse_button_down(self, event):
        """Called by the main application when the
        MOUSEBUTTONDOWN event fires.
        @param event - Pygame Event object
        MOUSEBUTTONDOWN  pos, button
        """
        #Check for collision
        self.tracking = False
        if (self.rect.collidepoint(event.pos)):
            self.tracking = True

    def on_mouse_button_up(self, event):
        """Called by the main application when the
        MOUSEBUTTONDOWN event fires.
        @param event - Pygame Event object
        MOUSEBUTTONDOWN  pos, button
        """
        #Check for collision
        if ((self.tracking) and (self.rect.collidepoint(event.pos))):
            #Not Tracking anymore
            self.tracking = False
            self.on_mouse_click(event)

    def on_mouse_click(self, event):
        """Called by the main application when the
        MOUSEBUTTONDOWN event fires, and the text widget
        has been clicked on.  You can either let
        this post the event (default) or you can override this
        function call in your app.
        ie. myTextWidget.on_mouse_click = my_click_handler
        @param event - Pygame Event object
        MOUSEBUTTONDOWN  pos, button
        """
        #Create the TEXT_WIDGET_CLICK event
        event_attrib = {}
        event_attrib["button"] = event.button
        event_attrib["pos"] = event.pos
        event_attrib["text_widget"] = self
        e = pygame.event.Event(self.event, event_attrib)
        pygame.event.post(e)


def truncline(text, font, maxwidth):
        real=len(text)
        stext=text
        l=font.size(text)[0]
        cut=0
        a=0
        done=1
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)
            done=0
        return real, done, stext

def wrapline(text, font, maxwidth):
    done=0
    wrapped=[]

    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text=text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)