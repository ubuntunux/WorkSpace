import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from widget.grid import Grid
from widget.game import Game
from widget.puck import Puck
from widget.ball import Ball

from kivy.factory import Factory

Factory.register("Ball", Ball)
Factory.register("Puck", Puck)


class TouchHockeyApp(App):
    def build(self):
        root = FloatLayout()
        root.add_widget(Grid())
        game = Game()
        root.add_widget(game)
        Clock.schedule_interval(game.update, 1./60.)
        return root

if __name__ in ('__android__', '__main__'):
    TouchHockeyApp().run()
