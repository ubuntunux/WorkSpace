#!/usr/bin/kivy
__version__ = '0.1'
import kivy
from core.mainLayout import MainLayout

kivy.require('1.7.0')
import os
from kivy.app import App

CATALOG_ROOT = os.path.dirname(__file__)


class KivyPhysicsSandboxApp(App):
    title = 'Kivy Physics Sandbox'
    icon = 'data/icon.png'
    kv_file = 'data/app.kv'

    def build(self):
        return MainLayout()


if __name__ == "__main__":
    KivyPhysicsSandboxApp().run()
