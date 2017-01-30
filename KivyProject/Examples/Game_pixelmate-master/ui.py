from functools import partial

from kivy.animation import Animation
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.bubble import Bubble
from kivy.graphics import Color, Line, Rectangle
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

from hold import TapAndHoldWidget
import dialog
from globals import *


def toolbar_on_touch():
    app = APP()
    if app.active_tool == TOOL_LINE:
        if app.aPaint.tool_line.state is not None:
            app.aPaint.tool_line._render_and_reset_state(app.aPaint.fbo, app.aPaint.tool_fbo)
            app.aPaint.fbo.draw()
            app.aPaint.canvas.ask_update()
    if app.active_tool == TOOL_RECT:
        if app.aPaint.tool_rect.state is not None:
            app.aPaint.tool_rect._render_and_reset_state(app.aPaint.fbo, app.aPaint.tool_fbo)
            app.aPaint.fbo.draw()
            app.aPaint.canvas.ask_update()
    if app.active_tool == TOOL_ELLIPSE:
        if app.aPaint.tool_ellipse.state is not None:
            app.aPaint.tool_ellipse._render_and_reset_state(app.aPaint.fbo, app.aPaint.tool_fbo)
            app.aPaint.fbo.draw()
            app.aPaint.canvas.ask_update()
    if app.active_tool == TOOL_SELECT:
        if app.aPaint.tool_select.state is not None:
            app.aPaint.tool_select._reset_state(app.aPaint.tool_fbo)
            app.aPaint.tool_select.context_menu.hide()
            app.aPaint.fbo.draw()
            app.aPaint.canvas.ask_update()

class ToolButton(Button):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if super(ToolButton, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self._do_press()
        self.dispatch('on_press')
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(ToolButton, self).on_touch_up(touch)
        assert (self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch
        self._do_release()
        self.dispatch('on_release')
        return True

    def on_pressed(self, instance, pos):
        pass


class ToolToggleButton(ToggleButton):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if super(ToggleButton, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self._do_press()
        self.dispatch('on_press')
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(ToggleButton, self).on_touch_up(touch)
        assert (self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch
        self._do_release()
        self.dispatch('on_release')
        return True

    def on_pressed(self, instance, pos):
        pass


class MenuButton(ToolToggleButton):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.sub_item = None
        self.callback = None

    def _do_press(self):
        self._release_group(self)
        self.state = 'down'
        # if callable(self.callback):
        #     self.callback()


class PaletteToggleButton(ToolToggleButton, TapAndHoldWidget):
    _hold_length = 0.3
    _sensitivity = 12

    def __init__(self, **kwargs):
        super(PaletteToggleButton, self).__init__(**kwargs)
        self.background_down = ""
        self.group = 'pal'

    def on_state(self, *args):
        if self.state == 'down':
            with self.canvas.after:
                Color(54. / 256, 171. / 256, 214. / 256, 1)
                Line(rectangle=(self.x + 2, self.y + 2, self.width - 4, self.height - 4), width=2, joint='miter')
        elif self.state == 'normal':
            self.canvas.after.clear()

    def on_touch_up(self, touch):
        super(PaletteToggleButton, self).on_touch_up(touch)
        if self.triggered:
            pass

    def _do_press(self):
        self._release_group(self)
        self.state = 'down' if self.state == 'down' else 'down'


class ToolBubble(Bubble):
    callbacks = {}

    @staticmethod
    def set_callback(key, function):
        if callable(function):
            ToolBubble.callbacks[key] = function
        else:
            raise NameError('function not callable')

    def __init__(self, **kwargs):
        Bubble.__init__(self, **kwargs)
        self.app = App.get_running_app()
        self.pressed = None
        self.size_hint = (None, None)
        self.tool = TOOL_LINE
        self.frames = []
        self.buttons = {}

        self.content.bind(size=self.redraw_content_frame)

    def add_button(self, text, background_normal, background_down, border, on_press):
        self.buttons[text] = Button(background_normal=background_normal,
                                    background_down=background_down,
                                    border=border, on_press=on_press)
        self.add_widget(self.buttons[text])
        return self.buttons[text]

    def redraw_content_frame(self, *args):
        if self.frames:
            [self.canvas.remove(frame) for frame in self.frames]
        with self.canvas:
            Color(0, 0, 0, 0.7)
            self.frames = [Line(rectangle=(self.content.x, self.content.y, self.content.width / self.cols * t,
                                           self.content.height)) for t in xrange(1, self.cols + 1)]
        self.canvas.ask_update()

    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            if self in self.parent.children:
                self.parent.remove_widget(self)
        if super(ToolBubble, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.ud[self] = True
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return True

    def on_touch_move(self, touch):
        if super(ToolBubble, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def select(self):
        if self in self._parent.children:
            self.parent.remove_widget(self)
            if str(self.app.active_tool) in self.toolbar.btn_data_background_normal:
                self.toolbar.btn_show_toolbar.background_normal = self.toolbar.btn_data_background_normal[
                    str(self.app.active_tool)]
                self.toolbar.btn_show_toolbar.background_down = self.toolbar.btn_data_background_down[
                    str(self.app.active_tool)]

    def hide(self):
        if self in self._parent.children:
            self.parent.remove_widget(self)

    def show(self, *args):
        if self not in self._parent.children:
            self._parent.add_widget(self)
        else:
            self._parent.remove_widget(self)


class Toolbar(RelativeLayout):
    hidden = BooleanProperty(False)

    def __init__(self, app, **kwargs):
        self.cover_layout = None
        RelativeLayout.__init__(self, **kwargs)
        self.app = app
        self.active_tool = None
        self.prev_tool = None
        self.pos_in = (0, TOOLBAR_LAYOUT_POS_HINT[1] * Window.height + 1)
        self.pos_out = (-Window.width * TOOLBAR_LAYOUT_SIZE_HINT[0] - 1, TOOLBAR_LAYOUT_POS_HINT[1] * Window.height + 1)
        self.hidden = False
        self.animation_show = Animation(pos=self.pos_in, transition='in_quad', duration=0.3)
        self.animation_hide = Animation(pos=self.pos_out, transition='in_quad', duration=0.3)
        self.size_hint = TOOLBAR_LAYOUT_SIZE_HINT
        self.pos = (TOOLBAR_LAYOUT_POS_HINT[0] * Window.width, TOOLBAR_LAYOUT_POS_HINT[1] * Window.height + 1)
        self.add_popup_menus()
        # self.btn_figs.callback = self.tool_menu.show

        self.tool_menu.tool = TOOL_LINE
        self.tool_menu_pen.tool = TOOL_PENCIL1
        self.tool_menu_eraser.tool = TOOL_ERASE1

        self.remove_widget(self.tool_menu)
        self.remove_widget(self.tool_menu_pen)
        self.remove_widget(self.tool_menu_eraser)
        self.btn_show_toolbar = ToggleButton(pos=(0, 0), background_normal=data_path('pencil_tool.png'),
                                             background_down=data_path('pencil_down.png'), border=[0, 0, 0, 0],
                                             size_hint=PALETTE_BTN_SHOW_SIZE_HINT, on_press=self.animate_switch)
        self.btn_data_background_normal = {
            str(TOOL_PENCIL1): data_path('pencil_tool.png'),
            str(TOOL_PENCIL2): data_path('pencil_tool.png'),
            str(TOOL_PENCIL3): data_path('pencil_tool.png'),
            str(TOOL_ERASE1): data_path('eraser_tool.png'),
            str(TOOL_ERASE2): data_path('eraser_tool.png'),
            str(TOOL_ERASE3): data_path('eraser_tool.png'),
            str(TOOL_RECT): data_path('rect_tool.png'),
            str(TOOL_ELLIPSE): data_path('ellipse_tool.png'),
            str(TOOL_LINE): data_path('line_tool.png'),
            str(TOOL_FILL): data_path('buck_tool.png'),
            str(TOOL_PICKER): data_path('picker_tool.png'),
            str(TOOL_MOVE): data_path('move_tool.png'),
            str(TOOL_SELECT): data_path('select_tool.png'),

        }
        self.btn_data_background_down = {
            str(TOOL_PENCIL1): data_path('pencil_1_down.png'),
            str(TOOL_PENCIL2): data_path('pencil_2_down.png'),
            str(TOOL_PENCIL3): data_path('pencil_3_down.png'),
            str(TOOL_ERASE1): data_path('eraser_1_down.png'),
            str(TOOL_ERASE2): data_path('eraser_2_down.png'),
            str(TOOL_ERASE3): data_path('eraser_3_down.png'),
            str(TOOL_RECT): data_path('rect_down.png'),
            str(TOOL_ELLIPSE): data_path('ellipse_down.png'),
            str(TOOL_LINE): data_path('line_down.png'),
            str(TOOL_FILL): data_path('buck_down.png'),
            str(TOOL_PICKER): data_path('picker_down.png'),
            str(TOOL_MOVE): data_path('move_down.png'),
            str(TOOL_SELECT): data_path('select_down.png'),

        }
        self.btn_show_toolbar.state = 'down'


        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            layout_rect = Rectangle(pos=(0, 0), size=(TOOLBAR_LAYOUT_SIZE_HINT[0]*WIN_WIDTH, TOOLBAR_LAYOUT_SIZE_HINT[1]*WIN_HEIGHT))

    def add_popup_menus(self):
        self.tool_menu.add_button(text='line', background_normal=data_path('line.png'),
                                  background_down=data_path('line_down.png'),
                                  border=[0, 0, 0, 0], on_press=self.on_popup_children_press)
        self.tool_menu.add_button(text='rect', background_normal=data_path('rect.png'),
                                  background_down=data_path('rect_down.png'),
                                  border=[0, 0, 0, 0], on_press=self.on_popup_children_press)
        self.tool_menu.add_button(text='ellipse', background_normal=data_path('ellipse.png'),
                                  background_down=data_path('ellipse_down.png'),
                                  border=[0, 0, 0, 0], on_press=self.on_popup_children_press)

        self.tool_menu_pen.add_button(text='pencil_1', background_normal=data_path('pencil_1.png'),
                                      background_down=data_path('pencil_1_down.png'),
                                      border=[0, 0, 0, 0], on_press=self.on_popup_children_press)
        self.tool_menu_pen.add_button(text='pencil_2', background_normal=data_path('pencil_2.png'),
                                      background_down=data_path('pencil_2_down.png'),
                                      border=[0, 0, 0, 0], on_press=self.on_popup_children_press)
        self.tool_menu_pen.add_button(text='pencil_3', background_normal=data_path('pencil_3.png'),
                                      background_down=data_path('pencil_3_down.png'),
                                      border=[0, 0, 0, 0], on_press=self.on_popup_children_press)

        self.tool_menu_eraser.add_button(text='eraser_1', background_normal=data_path('eraser_1.png'),
                                         background_down=data_path('eraser_1_down.png'),
                                         border=[0, 0, 0, 0], on_press=self.on_popup_children_press)
        self.tool_menu_eraser.add_button(text='eraser_2', background_normal=data_path('eraser_2.png'),
                                         background_down=data_path('eraser_2_down.png'),
                                         border=[0, 0, 0, 0], on_press=self.on_popup_children_press)
        self.tool_menu_eraser.add_button(text='eraser_3', background_normal=data_path('eraser_3.png'),
                                         background_down=data_path('eraser_1_down.png'),
                                         border=[0, 0, 0, 0], on_press=self.on_popup_children_press)

    def on_popup_children_press(self, bbutton):
        if bbutton is self.tool_menu.buttons['rect']:
            self.btn_figs.background_normal = data_path('rect.png')
            self.btn_figs.background_down = data_path('rect_down.png')
            self.app.active_tool = TOOL_RECT
            self.tool_menu.tool = TOOL_RECT
            self.tool_menu.select()
        elif bbutton is self.tool_menu.buttons['ellipse']:
            self.btn_figs.background_normal = data_path('ellipse.png')
            self.btn_figs.background_down = data_path('ellipse_down.png')
            self.app.active_tool = TOOL_ELLIPSE
            self.tool_menu.tool = TOOL_ELLIPSE
            self.tool_menu.select()
        elif bbutton is self.tool_menu.buttons['line']:
            self.btn_figs.background_normal = data_path('line.png')
            self.btn_figs.background_down = data_path('line_down.png')
            self.app.active_tool = TOOL_LINE
            self.tool_menu.tool = TOOL_LINE
            self.tool_menu.select()

        if bbutton is self.tool_menu_eraser.buttons['eraser_1']:
            self.btn_eraser.background_normal = data_path('eraser_1.png')
            self.btn_eraser.background_down = data_path('eraser_1_down.png')
            self.app.active_tool = TOOL_ERASE1
            self.tool_menu_eraser.tool = TOOL_ERASE1
            self.tool_menu_eraser.select()
        elif bbutton is self.tool_menu_eraser.buttons['eraser_2']:
            self.btn_eraser.background_normal = data_path('eraser_2.png')
            self.btn_eraser.background_down = data_path('eraser_2_down.png')
            self.app.active_tool = TOOL_ERASE2
            self.tool_menu_eraser.tool = TOOL_ERASE2
            self.tool_menu_eraser.select()
        elif bbutton is self.tool_menu_eraser.buttons['eraser_3']:
            self.btn_eraser.background_normal = data_path('eraser_3.png')
            self.btn_eraser.background_down = data_path('eraser_3_down.png')
            self.app.active_tool = TOOL_ERASE3
            self.tool_menu_eraser.tool = TOOL_ERASE3
            self.tool_menu_eraser.select()

        if bbutton is self.tool_menu_pen.buttons['pencil_1']:
            self.btn_pen.background_normal = data_path('pencil_1.png')
            self.btn_pen.background_down = data_path('pencil_1_down.png')
            self.app.active_tool = TOOL_PENCIL1
            self.tool_menu_pen.tool = TOOL_PENCIL1
            self.tool_menu_pen.select()
        elif bbutton is self.tool_menu_pen.buttons['pencil_2']:
            self.btn_pen.background_normal = data_path('pencil_2.png')
            self.btn_pen.background_down = data_path('pencil_2_down.png')
            self.app.active_tool = TOOL_PENCIL2
            self.tool_menu_pen.tool = TOOL_PENCIL2
            self.tool_menu_pen.select()
        elif bbutton is self.tool_menu_pen.buttons['pencil_3']:
            self.btn_pen.background_normal = data_path('pencil_3.png')
            self.btn_pen.background_down = data_path('pencil_3_down.png')
            self.app.active_tool = TOOL_PENCIL3
            self.tool_menu_pen.tool = TOOL_PENCIL3
            self.tool_menu_pen.select()

    # def on_size(self, *args):
    #     if self.cover_layout:
    #         with self.cover_layout.canvas.after:
    #             Color(0, 0, 0, 0.7)
    #             Line(rectangle=(0, 0, self.width / 2, self.height))
    #             for t in xrange(1, 7):
    #                 Line(rectangle=(0, 0, self.width, self.height * t / 6))
    #         self.canvas.ask_update()

    def on_touch_down(self, touch, *args):
        if self.collide_point(touch.x, touch.y):
            toolbar_on_touch()
        if super(Toolbar, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            if not self.btn_show_toolbar.collide_point(touch.x, touch.y):
                return False
        if self in touch.ud:
            return False
        return True

    def tools_on_button_press(self, button):
        if button.state == 'down':
            self.prev_tool = self.active_tool
            if button.tool == 'pencil':
                # self.app.active_tool = TOOL_PENCIL
                self.tool_menu_pen.show()
                self.app.active_tool = self.tool_menu_pen.tool
            if button.tool == 'erase':
                # self.app.active_tool = TOOL_ERASE
                self.tool_menu_eraser.show()
                self.app.active_tool = self.tool_menu_eraser.tool
            if button.tool == 'picker':
                self.app.active_tool = TOOL_PICKER
            if button.tool == 'fill':
                self.app.active_tool = TOOL_FILL
            if button.tool == 'select':
                self.app.active_tool = TOOL_SELECT
            if button.tool == 'move':
                self.app.active_tool = TOOL_MOVE
            if button.tool == 'zoomin':
                self.app.aPaint.scale_canvas(zoom=1.2)
            if button.tool == 'zoomout':
                self.app.aPaint.scale_canvas(zoom=1.0 / 1.2)
            if button.tool == 'zoomx1':
                self.app.aPaint.scale_canvas(zoom=1 / self.app.aPaint.scale)
            if button.tool == 'figures':
                self.tool_menu.show()
                self.app.active_tool = self.tool_menu.tool
            if button.tool == 'undo':
                self.app.aPaint.do_undo()
            if button.tool == 'redo':
                self.app.aPaint.do_redo()
            if str(self.app.active_tool) in self.btn_data_background_normal:
                self.btn_show_toolbar.background_normal = self.btn_data_background_normal[str(self.app.active_tool)]
                self.btn_show_toolbar.background_down = self.btn_data_background_down[str(self.app.active_tool)]
        else:
            button._do_press()


    def tools_select(self, tool):
        if tool == TOOL_PENCIL1:
            self.btn_pen._do_press()
            self.tools_on_button_press(self.btn_pen)
        if tool == TOOL_PENCIL2:
            self.btn_pen._do_press()
            self.tools_on_button_press(self.btn_pen)
        if tool == TOOL_PENCIL3:
            self.btn_pen._do_press()
            self.tools_on_button_press(self.btn_pen)
        elif tool == TOOL_ERASE1:
            self.btn_erase._do_press()
            self.tools_on_button_press(self.btn_erase)
        elif tool == TOOL_ERASE2:
            self.btn_erase._do_press()
            self.tools_on_button_press(self.btn_erase)
        elif tool == TOOL_ERASE3:
            self.btn_erase._do_press()
            self.tools_on_button_press(self.btn_erase)
        elif tool == TOOL_PICKER:
            self.btn_picker._do_press()
            self.tools_on_button_press(self.btn_picker)
        elif tool == TOOL_FILL:
            self.btn_fill._do_press()
            self.tools_on_button_press(self.btn_fill)
        elif tool == TOOL_SELECT:
            self.tbtn_move._do_press()
            self.tools_on_button_press(self.tbtn_move)
        elif tool == TOOL_MOVE:
            self.btn_move._do_press()
            self.tools_on_button_press(self.btn_move)
        elif tool == TOOL_RECT:
            self.btn_rect._do_press()
            self.tools_on_button_press(self.btn_rect)

    def animate_hide(self, *args):
        if not self.hidden:
            self.animation_hide.start(self)
            self.hidden = True
            self.tool_menu.hide()
            self.tool_menu_pen.hide()
            self.tool_menu_eraser.hide()

    def animate_show(self, *args):
        if self.hidden:
            self.animation_show.start(self)
            self.hidden = False

    def animate_switch(self, *args):
        if not self.hidden:
            self.animate_hide()
        else:
            self.animate_show()

    def on_hidden(self, instance, value):
        if value:
            self.btn_show_toolbar.state = 'normal'
        else:
            self.btn_show_toolbar.state = 'down'


Factory.register('Toolbar', cls=Toolbar)
Builder.load_file("ui.kv")


class Palette(RelativeLayout):
    hidden = BooleanProperty(False)

    def __init__(self, app, **kwargs):
        RelativeLayout.__init__(self, **kwargs)
        self.app = app
        self.hidden = False

        self.layout_color = BoxLayout(orientation='horizontal',
                                      size_hint=(1, 1),
                                      pos=(0, 0))

        with self.layout_color.canvas:
            Color(0.2, 0.2, 0.2, 1)
            layout_rect = Rectangle(pos=self.pos, size=(Window.width * PALETTE_LAYOUT_SIZE_HINT[0],
                                                        Window.height * PALETTE_LAYOUT_SIZE_HINT[1]))

        layout1 = BoxLayout(orientation='vertical', size_hint=PALETTE_LAYOUT_CLMN_SIZE_HINT, spacing=1,
                            padding=[1, 1, 0, 1])
        self.butList1 = [x for x in xrange(0, PALETTE_BTN_COUNT)]
        self.butList2 = [x for x in xrange(0, PALETTE_BTN_COUNT)]
        self.colorpicker_dialog = dialog.ColorPickerDialog(self.app, (Window.width, Window.height))
        for t in xrange(0, len(self.butList1)):
            self.butList1[t] = PaletteToggleButton()
            self.butList1[t].bind(on_press=partial(self.but_select, self.butList1[t]))
            self.butList1[t].on_hold = partial(self.open_colorpicker, self.butList1[t])
            self.butList1[t].background_normal = ""
            layout1.add_widget(self.butList1[t])
            self.butList1[t].background_color = (1, 0.05 * t, 0.05 * t, 1)
        layout2 = BoxLayout(orientation='vertical', size_hint=PALETTE_LAYOUT_CLMN_SIZE_HINT, spacing=1,
                            padding=[1, 1, 0, 1])
        for t in xrange(0, len(self.butList2)):
            self.butList2[t] = PaletteToggleButton()
            self.butList2[t].bind(on_press=partial(self.but_select, self.butList2[t]))
            self.butList2[t].on_hold = partial(self.open_colorpicker, self.butList2[t])
            self.butList2[t].background_normal = ""
            layout2.add_widget(self.butList2[t])
            self.butList2[t].background_color = (1, 0.05 * t, 0.05 * t, 1)

        self.butList1[0].background_color = (1, 1, 1, 1)
        self.butList1[1].background_color = (195 / 255., 195 / 255., 195 / 255., 1)
        self.butList1[2].background_color = (185 / 255., 122 / 255., 87 / 255., 1)
        self.butList1[3].background_color = (255 / 255., 174 / 255., 201 / 255., 1)
        self.butList1[4].background_color = (255 / 255., 201 / 255., 14 / 255., 1)
        self.butList1[5].background_color = (239 / 255., 228 / 255., 176 / 255., 1)
        self.butList1[6].background_color = (181 / 255., 230 / 255., 29 / 255., 1)
        self.butList1[7].background_color = (153 / 255., 217 / 255., 234 / 255., 1)
        self.butList1[8].background_color = (112 / 255., 146 / 255., 190 / 255., 1)
        self.butList1[9].background_color = (200 / 255., 191 / 255., 231 / 255., 1)

        self.butList2[0].background_color = (0, 0, 0, 1)
        self.butList2[1].background_color = (127 / 255., 127 / 255., 127 / 255., 1)
        self.butList2[2].background_color = (136 / 255., 0 / 255., 21 / 255., 1)
        self.butList2[3].background_color = (237 / 255., 28 / 255., 36 / 255., 1)
        self.butList2[4].background_color = (255 / 255., 127 / 255., 39 / 255., 1)
        self.butList2[5].background_color = (255 / 255., 242 / 255., 0 / 255., 1)
        self.butList2[6].background_color = (34 / 255., 177 / 255., 76 / 255., 1)
        self.butList2[7].background_color = (0 / 255., 162 / 255., 232 / 255., 1)
        self.butList2[8].background_color = (63 / 255., 72 / 255., 204 / 255., 1)
        self.butList2[9].background_color = (163 / 255., 73 / 255., 164 / 255., 1)

        self.pos_in = (PALETTE_LAYOUT_POS_HINT[0] * Window.width, PALETTE_LAYOUT_POS_HINT[1] * Window.height)
        self.pos_out = (Window.width + 1, PALETTE_LAYOUT_POS_HINT[1] * Window.height)
        self.animation_show = Animation(pos=self.pos_in, transition='in_quad', duration=0.3)
        self.animation_hide = Animation(pos=self.pos_out, transition='in_quad', duration=0.3)
        self.size_hint = PALETTE_LAYOUT_SIZE_HINT
        self.pos = self.pos_in
        self.layout_color.add_widget(layout1)
        self.layout_color.add_widget(layout2)
        self.add_widget(self.layout_color)
        self.btn_show_palette = ToggleButton(pos=(Window.width - PALETTE_BTN_SHOW_SIZE_HINT[0] * Window.width, 0),
                                             background_normal=data_path('palette.png'),
                                             background_down=data_path('palette_down.png'), border=[0, 0, 0, 0],
                                             size_hint=PALETTE_BTN_SHOW_SIZE_HINT, on_press=self.animate_switch)

        self.btn_show_palette.state = 'down'


    def on_touch_down(self, touch, *args):
        if self.collide_point(touch.x, touch.y):
            toolbar_on_touch()
        if super(Palette, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            if not self.btn_show_palette.collide_point(touch.x, touch.y):
                return False
        if self in touch.ud:
            return False
        return True

    def open_colorpicker(self, button, *args):
        self.colorpicker_dialog.open(color=button.background_color,
                                     on_close=partial(self.set_but_color, button))

    def set_but_color(self, button, *args):
        c = self.colorpicker_dialog.colorPicker.color
        button.background_color = c
        self.app.aColor = Color(c[0], c[1], c[2], c[3])

    def but_select(self, button, *args):
        c = button.background_color
        self.app.aColor = Color(c[0], c[1], c[2], c[3])

    def animate_hide(self, *args):
        if not self.hidden:
            self.animation_hide.start(self)
            self.hidden = True

    def animate_show(self, *args):
        if self.hidden:
            self.animation_show.start(self)
            self.hidden = False

    def animate_switch(self, *args):
        if not self.hidden:
            self.animate_hide()
        else:
            self.animate_show()

    def on_hidden(self, instance, value):
        if value:
            self.btn_show_palette.state = 'normal'
        else:
            self.btn_show_palette.state = 'down'


Builder.load_string('''

<MenuPopup>:

    id: MPopup
    title: "Menu"
    size_hint: .34, .84

    BoxLayout:
        size: root.size
        orientation: 'vertical'

        SettingSpacer:

        GridLayout:
            cols: 1
            spacing: [0, 0]
            padding: [0, 0]
            BubbleButton:
                text: "New project"
                font_size: globals.MAINMENU_BUTTON_TEXT_SIZE
                on_release: root.new_clbk()
            BubbleButton:
                text: "Open project \ Image"
                font_size: globals.MAINMENU_BUTTON_TEXT_SIZE
                on_release: root.open_clbk()
            BubbleButton:
                text: "Save project"
                font_size: globals.MAINMENU_BUTTON_TEXT_SIZE
                on_release: root.save_project_clbk()
            BubbleButton:
                text: "Export to image"
                font_size: globals.MAINMENU_BUTTON_TEXT_SIZE
                on_release: root.save_image_clbk()
            BubbleButton:
                text: "Settings"
                font_size: globals.MAINMENU_BUTTON_TEXT_SIZE
                on_release: root.options_clbk()
            SettingSpacer:
            BubbleButton:
                text: "Exit app"
                font_size: globals.MAINMENU_BUTTON_TEXT_SIZE
                on_release: root.exit_clbk()
''')


class Menu(Widget):
    MButton = ObjectProperty(None)

    def __init__(self, new_clbk, open_clbk, save_project_clbk, save_image_clbk, options_clbk, exit_clbk):
        Widget.__init__(self)
        self.new_clbk = lambda: self.call_and_dismiss(new_clbk)
        self.open_clbk = lambda: self.call_and_dismiss(open_clbk)
        self.save_project_clbk = lambda: self.call_and_dismiss(save_project_clbk)
        self.save_image_clbk = lambda: self.call_and_dismiss(save_image_clbk)
        self.exit_clbk = lambda: self.call_and_dismiss(exit_clbk)
        self.options_clbk = lambda: self.call_and_dismiss(options_clbk)

        self.popup = MenuPopup(new_clbk=self.new_clbk, open_clbk=self.open_clbk,
                               save_project_clbk=self.save_project_clbk,
                               save_image_clbk=self.save_image_clbk, exit_clbk=self.exit_clbk,
                               options_clbk=self.options_clbk)

    def open(self):
        self.popup.open()

    def call_and_dismiss(self, clbk):
        if callable(clbk):
            clbk()
        self.popup.dismiss()


class MenuPopup(Popup):
    new_clbk = ObjectProperty(None)
    open_clbk = ObjectProperty(None)
    save_project_clbk = ObjectProperty(None)
    save_image_clbk = ObjectProperty(None)
    options_clbk = ObjectProperty(None)
    exit_clbk = ObjectProperty(None)

    def __init(self):
        Popup.__init__(self)





