from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

class BrowserUI(RelativeLayout):
    pass

class BrowserApp(App):

    def build(self):
        return BrowserUI()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    BrowserApp().run()
