import re
from os.path import isfile, splitext

from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.settings import SettingSpacer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from globals import *
import improc


class NumInput(TextInput):
    pat = re.compile('[^0-9]')

    def __init__(self, **kwargs):
        TextInput.__init__(self, text_size=26, **kwargs)

        self.input_type = 'number'

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(NumInput, self).insert_text(s, from_undo=from_undo)


class OpenDialog(FloatLayout):
    load = ObjectProperty(None)
    get_texture = ObjectProperty(None)
    filters = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def_path = StringProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    get_texture = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    filters = ObjectProperty(None)
    formats = ObjectProperty(None)
    set_format = ObjectProperty(None)


class NewDialog(FloatLayout):
    ok = ObjectProperty(None)
    cancel = ObjectProperty(None)
    text_input = ObjectProperty(None)


class NewImage():
    def __init__(self, callback):
        self.title = "New Image: "
        self.callback = callback
        self.content = NewDialog(ok=self._ok, cancel=self._dismiss)
        self._popup = Popup(title=self.title, content=self.content, pos_hint={'center': 1, 'top': 1},
                            size_hint=(0.3, 0.3))

    def open(self):
        self._popup.open()

    def _ok(self, wtext, htext):
        Window.release_all_keyboards()
        try:
            w = int(wtext)
            h = int(htext)
        except:
            PopupMessage("Notification", "Width and height should be greater than zero")
            return
        if w == 0 or h == 0:
            PopupMessage("Notification", "Width and height should be greater than zero")
            return
        self.callback((w, h))
        self._popup.dismiss()

    def _dismiss(self):
        Window.release_all_keyboards()
        self._popup.dismiss()


class OpenImage():
    def __init__(self, callback):
        self.filters = ["*.pixelmate", "*.bmp", "*.png", "*.jpg", "*.gif"]
        self.title = "Open Image: "
        self.callback = callback
        self.app = App.get_running_app()
        # self.def_path = self.app.config.get('filechooser', 'open_path')
        self.def_path = self.app.config.getdefault('filechooser', 'open_path', DEF_PATH)
        if self.def_path == '':
            self.def_path = DEF_PATH
        self.content = OpenDialog(load=self._load, filters=self.filters, cancel=self._dismiss,
                                  get_texture=self._get_texture)
        self.content.chooser.path = os.path.abspath(self.def_path)
        self.content.chooser.bind(path=self._set_title)
        self._popup = Popup(title=self.title, content=self.content, size_hint=(1, 1))
        self._set_title(self.content.chooser, self.def_path)

    def open(self):
        self._popup.open()

    def _load(self, path, filename):
        self.callback(path, filename)
        self._dismiss()

    def _set_title(self, chooser, path):
        self._popup.title = self.title + os.path.abspath(path)

    def _dismiss(self):
        self._popup.dismiss()

    def _get_texture(self, filename):
        ext = '*' + splitext(filename)[1]
        # print filename
        if ext in self.filters:
            if ext == '*.pixelmate':
                return improc.merged_texture_from_zip(filename)
            else:
                return Image(source=filename).texture


class SaveBase():
    def __init__(self, callback):
        self.callback = callback
        self.app = App.get_running_app()
        self.def_path = self.app.config.getdefault('filechooser', 'save_path', DEF_PATH)
        if self.def_path == '':
            self.def_path = DEF_PATH
        self.content = SaveDialog(save=self._save, cancel=self._dismiss, filters=self.filters, formats=self.formats,
                                  set_format=self._set_format, get_texture=self._get_texture)
        self.content.chooser.path = self.def_path
        self.content.spinner.bind(text=self._set_format)
        self.content.chooser.bind(path=self._set_title)
        self._popup = Popup(title=self.title, content=self.content, size_hint=(1, 1))
        self._set_title(self.content.chooser, self.def_path)

    def open(self):
        self._popup.open()

    def _set_format(self, spinner, format):
        self.format = format

    def _set_title(self, chooser, path):
        self._popup.title = self.title + os.path.normpath(path)

    def _dismiss(self):
        self._popup.dismiss()

    def _save(self, path, filename):
        fullpath = os.path.join(path, filename) + '.' + self.format.lower()

        def save(answer):
            if answer == 'yes':
                pass
            else:
                self.open()

        filename = os.path.split(filename)[1]
        if len(filename) == 0:
            PopupMessage(title='Information',
                         text='Filename can\'t be is empty.', callback=save)
            return
        if set(filename).intersection('\\/:*?"<>|'):
            PopupMessage(title='Information', text='Filename can\'t contain any of \\/:*?"<>| characters.',
                         callback=save)
            return
        if isfile(fullpath):
            ConfirmDialog(title='Confirmation', text='File already exist. Overwrite?', callback=save)
            return

        self.callback(path, filename, self.format)
        self._popup.dismiss()

    def _get_texture(self, filename):
        ext = '*' + splitext(filename)[1]
        if ext in self.filters:
            if ext == '*.pixelmate':
                return improc.merged_texture_from_zip(filename)
            else:
                return Image(source=filename).texture


class SaveImage(SaveBase):
    def __init__(self, callback):
        self.filters = ["*.png", "*.jpg", "*.bmp"]
        self.formats = ["png", "jpg", "bmp"]
        self.format = self.formats[0]
        self.title = "Save Image: "
        SaveBase.__init__(self, callback)


class SaveProject(SaveBase):
    def __init__(self, callback):
        self.filters = ["*.pixelmate"]
        self.formats = ["pixelmate"]
        self.format = self.formats[0]
        self.title = "Save Project: "
        SaveBase.__init__(self, callback)


Factory.register('OpenDialog', cls=OpenDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('NewDialog', cls=NewDialog)

Builder.load_file("dialog.kv")

Builder.load_string('''
<AskPopupContent>:
    cols: 1
    Label:
        text: root.text
    GridLayout:
        cols: 2
        size_hint_y: None
        height: '44sp'
        Button:
            text: 'Yes'
            on_release: root.dispatch('on_answer', 'yes')
        Button:
            text: 'No'
            on_release: root.dispatch('on_answer', 'no')
''')

Builder.load_string('''
<MessPopupContent>:
    cols: 1
    Label:
        text: root.text
    GridLayout:
        cols: 2
        size_hint_y: None
        height: '44sp'
        Button:
            text: 'Ok'
            on_release: root.dispatch('on_answer', 'ok')
''')


class AskPopupContent(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(AskPopupContent, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class MessPopupContent(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(MessPopupContent, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class ConfirmDialog():
    def __init__(self, title, text, callback):
        self.callback = callback
        content = AskPopupContent(text=text)

        content.on_answer = self._on_answer
        self.popup = Popup(title=title,
                           content=content,
                           size_hint=(0.4, 0.3),
                           auto_dismiss=False)
        self.popup.open()

    def _on_answer(self, answer):
        self.callback(answer)
        self.popup.dismiss()


class ConfirmDialog2():
    def __init__(self, title, text, callback):
        self.callback = callback
        content = AskPopupContent(text=text)

        content.on_answer = self._on_answer
        self.popup = Popup(title=title,
                           content=content,
                           size_hint=(0.4, 0.3),
                           auto_dismiss=False)

    def _on_answer(self, answer):
        self.callback(answer)
        self.popup.dismiss()

    def close(self):
        self.popup.dismiss()

    def show(self):
        self.popup.open()


class PopupMessage():
    def __init__(self, title, text, callback=None):
        self.callback = callback
        content = MessPopupContent(text=text)

        content.on_answer = self._on_answer
        self.popup = Popup(title=title,
                           content=content,
                           size_hint=(0.75, 0.35),
                           auto_dismiss=False)
        self.popup.open()

    def _on_answer(self, answer):
        if callable(self.callback):
            self.callback(answer)
        self.popup.dismiss()


class ColorPickerDialog:
    def __init__(self, app, size, on_close=None):
        self.app = app
        cp_pos = [(Window.size[0] - size[0]) / 2, (Window.size[1] - size[1]) / 2]
        self.colorPicker = ColorPicker(pos=cp_pos, size_hint=(1, 1))
        self.btn_colorPicker = Button(text='Ok')
        self.btn_cancel = Button(text='Cancel', on_press=self.dismiss)
        layout = BoxLayout(orientation='vertical')
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        btn_layout.add_widget(self.btn_colorPicker)
        btn_layout.add_widget(self.btn_cancel)
        layout.add_widget(SettingSpacer())
        layout.add_widget(self.colorPicker)
        layout.add_widget(SettingSpacer())
        layout.add_widget(btn_layout)
        self.popup_picker = Popup(title="Color Picker", content=layout, size_hint=(0.6, 0.8))
        self.popup_picker.on_dismiss = self.on_dismiss
        self.on_close_clbk = on_close
        self.btn_colorPicker.bind(on_release=self.close)

    def open(self, color=None, on_close=None):
        if color is not None:
            self.colorPicker.color = color
        if callable(on_close):
            self.on_close_clbk = on_close
        self.app.dialog_state = STATE_DIALOG_COLOR
        self.popup_picker.open()

    def on_dismiss(self, *args):
        self.app.dialog_state = STATE_ROOT

    def close(self, *args):
        self.on_close()
        self.popup_picker.dismiss()
        self.app.dialog_state = STATE_ROOT

    def on_close(self, *args):
        if callable(self.on_close_clbk):
            self.on_close_clbk()

    def dismiss(self, *args):
        self.popup_picker.dismiss()
        self.on_dismiss()