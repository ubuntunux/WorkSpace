from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar, SettingsPanel

from globals import APP_VERSION


class Options():
    def __init__(self, config=None, settings=None):
        if settings is None:
            self.settings_panel = SettingsWithSidebar()
        else:
            self.settings_panel = settings
        self.config = config
        self.settings_panel.add_json_panel('Interface', self.config, 'option.json')
        panel = SettingsPanel(title="PixelMate v" + str(
            APP_VERSION) + "\n\nPixel art editor program\nDeveloped by Anton Plyaskin (werton)\nPowered by Python & Kivy",
                              settings=self)
        if self.settings_panel.interface is not None:
            self.settings_panel.interface.add_panel(panel, "About", panel.uid)


class SettingsApp(App):
    def build(self):
        opt = Options()
        return opt.settings_panel


if __name__ in ('__android__', '__main__'):
    SettingsApp().run()