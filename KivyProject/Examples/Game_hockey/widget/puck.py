import kivy
kivy.require('1.0.9')

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import OptionProperty, NumericProperty, ListProperty
from kivy.vector import Vector


class Puck(Widget):
    radius = NumericProperty(Window.height * .08)
    score = NumericProperty(0)
    state = OptionProperty('right', options=('right', 'left'))
    list_points = ListProperty([])

    def collide_point(self, x, y):
        distance = Vector(self.pos).distance(Vector(x, y))
        return distance <= self.radius

    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        touch.ud['movable.dx'] = touch.x - self.x
        touch.ud['movable.dy'] = touch.y - self.y
        self.list_points = []
        return True

    def on_touch_move(self, touch):
        if self not in touch.ud:
            return
        if touch.y - touch.ud['movable.dy'] <= 0 + self.radius:
            return
        if touch.y - touch.ud['movable.dy'] >= Window.height - self.radius:
            return
        if self.state == 'right':
            if touch.x - touch.ud['movable.dx'] >= Window.width * 0.5 - self.radius:
                return
            if touch.x - touch.ud['movable.dx'] <= 0 + self.radius:
                return
        else:
            if touch.x - touch.ud['movable.dx'] <= Window.width * 0.5 + self.radius:
                return
            if touch.x - touch.ud['movable.dx'] >= Window.width - self.radius:
                return
        self.x = touch.x - touch.ud['movable.dx']
        self.y = touch.y - touch.ud['movable.dy']
        self.list_points = self.list_points + [touch.x, touch.y]
        return True
