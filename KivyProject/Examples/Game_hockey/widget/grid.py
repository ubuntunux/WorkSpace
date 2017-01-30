import kivy
kivy.require('1.0.9')

from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.core.window import Window


class Grid(Widget):
    color = ListProperty([.6, .6, .8, 1])
    background_color = ListProperty([0, 0, 0, 1])
    color_right = ListProperty([1, .4, .4, 1])
    color_left = ListProperty([.4, .4, 1, 1])

    down_right = ListProperty([0, 0, Window.width * .5, 0])
    top_right = ListProperty([0, Window.height, Window.width * .5, Window.height])
    down_left = ListProperty([Window.width * .5, 0, Window.width, 0])
    top_left = ListProperty([Window.width * .5, Window.height, Window.width, Window.height])
    right_down = ListProperty([0, 0, 0, Window.height * .25])
    right_top = ListProperty([0, Window.height * .75, 0, Window.height])
    left_down = ListProperty([Window.width, 0, Window.width, Window.height * .25])
    left_top = ListProperty([Window.width, Window.height * .75, Window.width, Window.height])
    middle = ListProperty([Window.width * .5, 0, Window.width * .5, Window.height])

    radius = NumericProperty(Window.height * .25)
