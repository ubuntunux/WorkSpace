#!/usr/bin/env python

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

class KvApp(App):
    def _print_fps(self, *largs):
        print 'FPS: %2.4f (real draw: %d)' % (
            Clock.get_fps(), Clock.get_rfps())

    def _reload_keypress(self, instance, code, *largs):
        if code != 286:
            return
        for child in Window.children[:]:
            Window.remove_widget(child)
        root = Builder.load_file(self.options['filename'])
        Window.add_widget(root)

    def build(self):
        Clock.schedule_interval(self._print_fps, 1)
        Window.bind(on_keyboard=self._reload_keypress)
        return Builder.load_file(self.options['filename'])

if __name__ == '__main__':
    import sys
    import os

    #if len(sys.argv) < 2:
        #print 'Usage: %s filename.kv' % os.path.basename(sys.argv[0])
        #sys.exit(1)

    #KvApp(filename=sys.argv[1]).run()
    filenames=["app_button.kv", "app_camera.kv", "app_fbo.kv", "app_layout.kv", "app_logo.kv", "app_scatter.kv", "app_stencil.kv", "app_video.kv"]

    KvApp(filename=filenames[2]).run()