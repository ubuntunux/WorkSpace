import kivy
kivy.require('1.0.9')

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, OptionProperty, ListProperty, ReferenceListProperty
from random import random
from kivy.vector import Vector


class Ball(Widget):
    color = ListProperty([random(), 1, 1])
    radius = NumericProperty(Window.height * .05)
    state = OptionProperty('right', options=('right', 'left'))

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y) 

    def collide_widget(self, widget):
        distance = Vector(self.pos).distance(Vector(widget.pos))
        return distance <= self.radius + widget.radius

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos
        if (self.x - self.radius <= 0) or (self.x + self.radius >= Window.width):
            self.velocity_x *= -1
            if (self.y - self.radius >= Window.height * 0.25) and (self.y - self.radius <= Window.height * 0.75):
                if (self.x - self.radius <= 0):
                    return False
                if (self.x + self.radius >= Window.width):
                    return True
        if (self.y - self.radius <= 0) or (self.y + self.radius >= Window.height):
            self.velocity_y *= -1
