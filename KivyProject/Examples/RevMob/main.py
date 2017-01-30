__version__ = '0.2'

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.utils import platform
from kivy.logger import Logger
from kivy.ext import load
from kivy.utils import platform

from revmob import RevMob as revmob

if platform() == 'android':
    REVMOB_APP_ID = '5106bea78e5bd71500000098'
elif platform() == 'ios':
    REVMOB_APP_ID = '5106be9d0639b41100000052'
else:
    REVMOB_APP_ID = 'unknown platform for RevMob'


class MenuScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.cols = 1

        def start_session(instance):
            revmob.start_session(REVMOB_APP_ID)
        button = Button(text='Start session')
        button.bind(on_press=start_session)
        self.add_widget(button)

        def show_fullscreen(instance):
            revmob.show_fullscreen()
        button = Button(text='Show fullscreen')
        button.bind(on_press=show_fullscreen)
        self.add_widget(button)

        def show_popup(instance):
            revmob.show_popup()
        button = Button(text='Show popup')
        button.bind(on_press=show_popup)
        self.add_widget(button)

        def open_link(instance):
            revmob.open_link()
        button = Button(text='Open link')
        button.bind(on_press=open_link)
        self.add_widget(button)

        def set_testing_mode_with_ads(instance):
            revmob.set_testing_mode(revmob.TESTING_MODE_WITH_ADS)
        button = Button(text='Testing mode with ads')
        button.bind(on_press=set_testing_mode_with_ads)
        self.add_widget(button)

        def set_testing_mode_without_ads(instance):
            revmob.set_testing_mode(revmob.TESTING_MODE_WITHOUT_ADS)
        button = Button(text='Testing mode without ads')
        button.bind(on_press=set_testing_mode_without_ads)
        self.add_widget(button)

        def disable_testing_mode(instance):
            revmob.set_testing_mode(revmob.TESTING_MODE_DISABLED)
        button = Button(text='Disable testing mode')
        button.bind(on_press=disable_testing_mode)
        self.add_widget(button)

        def print_environment_information(instance):
            revmob.print_environment_information()
        button = Button(text='Print environment information')
        button.bind(on_press=print_environment_information)
        self.add_widget(button)


class RevMobSample(App):
    def build(self):
        return MenuScreen()


if __name__ == '__main__':
    RevMobSample().run()
