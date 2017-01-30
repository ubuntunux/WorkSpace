import kivy
kivy.require('1.0.9')

from kivy.uix.widget import Widget
from widget.ball import Ball
from kivy.properties import ObjectProperty, NumericProperty
from kivy.vector import Vector
from kivy.core.window import Window

class Game(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    angle = NumericProperty(0.)

    def update(self, dt):
        result = self.ball.update()
        if result is not None:
            if result:
                self.player1.score += 1
                self.ball.pos = (Window.width * .5 + Window.height * .25, Window.height * .5)
                self.ball.velocity = (0, 0)
            else:
                self.player2.score += 1
                self.ball.pos = (Window.width * .5 - Window.height * .25, Window.height * .5)
                self.ball.velocity = (0, 0)
            if (self.player1.score == 10) or (self.player2.score == 10):
                if self.parent != None:
                    self.parent.remove_widget(self)
        for player in self.player1, self.player2:
            if self.ball.collide_widget(player):
                self.update_trajectory()

    def update_trajectory(self):
        for player in self.player1, self.player2:
            if self.ball.collide_widget(player):
                if self.player1.list_points != []:
                    list_points = self.player1.list_points
                if self.player2.list_points != []:
                    list_points = self.player2.list_points
                a, b = self.linreg(list_points)
                #print a, b
                self.ball.velocity = a / 100., b / 100.


    def linreg(self, list_of_points):
        if ((len(list_of_points) % 2) != 0 or len(list_of_points) == 0):
            a = 100
            b = 100
        else:
            Sx = Sy = Sxx = Syy = Sxy = 0.0
            N = len(list_of_points) / 2
            i = 0
            x = 0
            for elmt in list_of_points:
                if ((i % 2) == 0):
                    Sx = Sx + elmt
                    Sxx = Sxx + elmt * elmt
                    x = elmt
                else:
                    Sy = Sy + elmt
                    Syy = Syy + elmt * elmt
                    Sxy = Sxy + elmt * x
                i += 1
                det = Sxx * N - Sx * Sx
                if (det == 0):
				    a, b = 100, 100
                else:
			        a, b = (Sxy * N - Sy * Sx) / det, (Sxx * Sy - Sx * Sxy) / det
        x = 1
        if(a < 0.2 and a > 0):
            a = 0.2
        if(a > -0.2 and a < 0):
            a = -0.2
        y = a * x
        if(y == 0):
            y = 1
        y = x / y * 200
        x = 200
        return y, x
