from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics import Color, Rectangle
from Viewport import Viewport

class MyScatter(Viewport):
    pass

class ScatterApp(App):
    def build(self):
        s = MyScatter(size=(800, 600), size_hint=(None, None))
        s.top = 500
        return s

ScatterApp().run()
