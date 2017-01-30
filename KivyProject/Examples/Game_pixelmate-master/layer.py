from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.graphics.fbo import Fbo
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, BooleanProperty

from hold import TapAndHoldWidget
import improc
from globals import *


class Layer(Widget):
    layer_bg_texture = None
    layer_bg_rect = None

    @staticmethod
    def _create_texture(size):
        texture = Texture.create(size=size, colorfmt='rgba', bufferfmt='ubyte')
        texture.mag_filter = 'nearest'
        texture.min_filter = 'nearest'
        return texture

    @staticmethod
    def create_bg_rect(size):
        if not Layer.layer_bg_texture:
            path = data_path('bg3.png')
            Layer.layer_bg_texture = Image(path).texture
            Layer.layer_bg_texture.mag_filter = 'nearest'
            Layer.layer_bg_texture.min_filter = 'nearest'
            Layer.layer_bg_texture.wrap = 'repeat'
        Layer.layer_bg_rect = Rectangle(texture=Layer.layer_bg_texture, pos=(0, 0), size=size)
        nb_repeat_x = size[0] / 4
        nb_repeat_y = size[1] / 4
        Layer.layer_bg_rect.tex_coords = (
            0, 0,
            - nb_repeat_x, 0,
            - nb_repeat_x, -nb_repeat_y,
            0, -nb_repeat_y
        )
        return Layer.layer_bg_rect

    def __init__(self, app, size, **kwargs):
        Widget.__init__(self, **kwargs)
        self.app = app
        self.is_active = False
        Layer.create_bg_rect(size=size)
        self.texture = Layer._create_texture(size=size)
        self.rect = self._create_textured_rect(self.texture)
        self.textures_array = []
        self._textures_array_index = 0
        self.visible = True
        self.preview_rect = None
        self.texture_locked = False

    def new_texture(self, size):
        self.texture = Layer._create_texture(size=size)
        self.put_texture_on_canvas(self.texture)

    def _create_textured_rect(self, texture):
        Layer.create_bg_rect(size=texture.size)
        self.rect = Rectangle(texture=texture, pos=(0, 0), size=texture.size)
        # self.rect.tex_coords = (0, 1, 1, 1, 1, 0, 0, 0)
        return self.rect

    def replace_texture(self, texture):
        self.texture = texture
        self.rect = self._create_textured_rect(texture)
        self.put_texture_on_canvas(texture)

    def recreate_texture(self, texture):
        self.texture = improc.texture_copy(texture, smooth=False)
        self.rect = self._create_textured_rect(self.texture)
        self.put_texture_on_canvas(self.texture)
        return self.texture

    def put_rects_on_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            bg_tex = Layer.layer_bg_texture.get_region(0, 0, self.size[0], self.size[1])
            self.previewRectBG = Rectangle(texture=bg_tex, pos=(self.x, self.y),
                                           size=(self.size[0], self.size[1]))
            self.preview_rect = Rectangle(texture=self.texture, pos=(self.x, self.y),
                                          size=(self.size[0], self.size[1]))
        self.canvas.ask_update()

    def put_texture_on_canvas(self, texture):
        self.put_rects_on_canvas()

    def switch_visible(self):
        self.visible = not self.visible

    def get_texture(self):
        return self.texture

    def backup_texture(self):
        _texture = improc.texture_copy(self.texture)
        self.textures_array = self.textures_array[:self._textures_array_index + 1]
        self.textures_array.append(_texture)
        self._textures_array_index = len(self.textures_array) - 1

    def texture_from_backup(self, direction):
        if direction == -1:
            if self._textures_array_index > 0:
                self._textures_array_index -= 1
                self.texture = improc.texture_copy(self.textures_array[self._textures_array_index])
                self.replace_texture(self.texture)
        else:
            if self._textures_array_index < len(self.textures_array) - 1:
                self._textures_array_index += 1
                self.texture = improc.texture_copy(self.textures_array[self._textures_array_index])
                self.replace_texture(self.texture)


    def clear_texture(self):
        self.texture = Layer._create_texture(size=self.app.aPaint.fbo.texture.size)
        self.rect = Rectangle(texture=self.texture, pos=(0, 0), size=self.texture.size)

    def lock_texture(self):
        self.texture_locked = True

    def switch_lock_texture(self):
        self.texture_locked = not self.texture_locked


class LayerBox(TapAndHoldWidget):
    _hold_length = 0.3
    _sensitivity = 12
    __events__ = ('on_press', 'on_release')
    active = None
    active_id = None
    last_active = None
    dragged_box = None
    boxlist = []
    callbacks = {}
    app = None

    _is_active = BooleanProperty(False)

    @staticmethod
    def select_rect_update():
        for lay in LayerBox.boxlist:
            lay.remove_selrect()
        if LayerBox.active:
            LayerBox.active.add_selrect()

    @staticmethod
    def activate(id):
        LayerBox.last_active = LayerBox.active
        LayerBox.active = LayerBox.boxlist[id]

        for lb in LayerBox.boxlist:
            if lb is not LayerBox.active:
                lb.layer.is_active = False
                lb._is_active = False
                lb.put_rects_on_canvas()
        LayerBox.active.layer.is_active = True
        LayerBox.active._is_active = True
        LayerBox.active.put_rects_on_canvas()

        if callable(LayerBox.active.on_press_callback):
            LayerBox.active.on_press_callback()
            pass


    def __init__(self, app, texture_size, **kwargs):
        self._is_active = False
        self.dragged = False
        self.before_drag_pos = None
        self.drag_shift_y = 0
        self.drag_x = 0
        self._bg_rect = None
        self.size_per = 0.19
        self.selrect_w = 0.003 * Window.size[0]
        TapAndHoldWidget.__init__(self, orientation='horizontal', **kwargs)
        LayerBox.app = self.app = app
        self.on_press_callback = None
        self.add_new_callback = None
        self.size_hint = (None, None)
        self.layout = RelativeLayout(**kwargs)
        self.btn_view = ToggleButton(background_normal=data_path('show.png'),
                                     background_down=data_path('show_down.png'), border=[0, 0, 0, 0],
                                     on_press=self.switch_visible)
        self.btn_menu = ToggleButton(background_normal=data_path('lock.png'),
                                     background_down=data_path('lock_down.png'), border=[0, 0, 0, 0],
                                     on_press=self.switch_lock)
        self.layer = Layer(app, size=texture_size, pos_hint={'x': 0, 'y': 0})
        self.size = [self.size_per * Window.size[0], self.size_per * Window.size[1]]
        self.btn_view.size = [0.36 * self.size[1], 0.36 * self.size[1]]
        self.btn_menu.size = [0.36 * self.size[1], 0.36 * self.size[1]]
        self.btn_view.pos = (0, 0.64 * self.height)
        self.btn_menu.pos = (0, 0)
        self.layer.pos = (0, (self.size[1] - self.layer.size[1]) / 2.0)
        self.layout.add_widget(self.layer)
        self.layout.add_widget(self.btn_view)
        self.layout.add_widget(self.btn_menu)
        self.add_widget(self.layout)
        self._select_line = None
        self.update_size_pos(texture_size)
        LayerBox.boxlist.append(self)
        self.put_rects_on_canvas()
        if len(LayerBox.boxlist) == 1:
            LayerBox.activate(0)

    @property
    def is_active(self):
        return self._is_active

    def get_texture(self):
        return self.layer.get_texture()

    def set_pos(self, (x, y)):
        if x:
            self.x = x
            self.layout.x = x
        if y:
            self.y = y
            self.layout.y = y

    def switch_visible(self, *args):
        self.layer.switch_visible()
        self.app.update()

    def switch_lock(self, *args):
        self.layer.switch_lock_texture()
        self.app.update()

    def calc_layer_size(self, texture_size):
        k1 = float(self.size[0]) / float(self.size[1])
        k2 = float(texture_size[0]) / float(texture_size[1])
        if k2 > k1:
            w = 1.0 * self.width
            h = w / k2
        else:
            h = self.height
            w = h * k2
        return (w, h)

    def update_size_pos(self, texture_size):
        self.layer.size = self.calc_layer_size(texture_size)
        self.layer.pos = ((self.size[0] - self.layer.size[0]) / 2.0,
                          (self.size[1] - self.layer.size[1]) / 2.0)

    def _update_back(self):
        if self._bg_rect:
            self.layout.canvas.before.remove(self._bg_rect)
            self._bg_rect = None

        with self.layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self._bg_rect = Rectangle(pos=(0, 0), size=(self.size[0], self.size[1]))

    def new_texture(self, size):
        self.layer.new_texture(size)

    def put_rects_on_canvas(self):
        self._update_back()
        self.layer.put_rects_on_canvas()

    def put_texture_on_canvas(self, texture):
        self._update_back()
        self.layer.put_texture_on_canvas(texture)

    def on_touch_down(self, touch):
        if super(LayerBox, self).on_touch_down(touch):
            return True

        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        # touch.ud[self] = True
        self.dispatch('on_press')
        self.on_press()

    def on_touch_move(self, touch):
        if super(LayerBox, self).on_touch_move(touch):
            return True
        # if self.collide_point(touch.x, touch.y):
        self.dragging(touch)
        return self in touch.ud

    def on_touch_up(self, touch):
        if super(LayerBox, self).on_touch_up(touch):
            return True
        if self.collide_point(touch.x, touch.y):
            self.drop()
        return self in touch.ud

    def on_hold(self, touch):
        self.dragged = True
        self.catch(touch)

    def drop(self):
        self.dragged = False
        LayerBox.dragged_box = None
        self.x = self.drag_x
        self.set_pos((self.x, None))
        parent = self.parent
        self.parent.remove_widget(self)
        parent.add_widget(self)
        self.redraw_selrect()

    def catch(self, touch):
        if self.dragged:
            LayerBox.dragged_box = self
            self.before_drag_pos = self.pos[:]

            self.drag_shift_y = self.y - touch.y + self.height/6
            self.drag_x = self.x
            x = self.drag_x + 2

            self.set_pos((x, touch.y + self.drag_shift_y))
            self.redraw_selrect()
            parent = self.parent
            self.parent.remove_widget(self)
            parent.add_widget(self)
            # parent.resize_layerbox_layout()

    def dragging(self, touch):
        if self.dragged:
            x = self.drag_x + 2
            self.set_pos((x, touch.y + self.drag_shift_y))
            self.redraw_selrect()

    def on_press(self):
        LayerBox.last_active = LayerBox.active
        LayerBox.activate(LayerBox.boxlist.index(self))
        LayerBox.select_rect_update()

    def set_active(self):
        LayerBox.activate(LayerBox.boxlist.index(self))

    def on__is_active(self, instance, value):
        LayerBox.select_rect_update()

    def on_release(self):
        pass

    def add_selrect(self):
        with self.canvas.before:
            Color(54. / 256, 171. / 256, 214. / 256, 1)
            self._select_line = Rectangle(pos=(self.x - self.selrect_w, self.y - self.selrect_w),
                                          size=(self.size[0] + self.selrect_w * 2, self.size[1] + self.selrect_w * 2))

    def remove_selrect(self):
        if self._select_line is not None:
            self.canvas.before.remove(self._select_line)
            self._select_line = None

    def redraw_selrect(self):
        self.remove_selrect()
        self.add_selrect()


# class LayerBoxLayout(RelativeLayout):
#     def __init__(self, **kwargs):
#         super(LayerBoxLayout, self).__init__(**kwargs)
#
#         FloatLayout(self).bind()
#
#     def do_layout(self, *args):
#         size = self.size
#         super(LayerBoxLayout, self).do_layout(*args)
#         self.size = size


class LayerRibbon(RelativeLayout, EventDispatcher):
    hidden = BooleanProperty(True)
    __events__ = ('on_press', 'on_release')

    layer_box_list = ListProperty([])

    @staticmethod
    def activate(id):
        LayerBox.activate(id)

    @staticmethod
    def bg_texture():
        return Layer.layer_bg_texture

    def __init__(self, app, **kwargs):
        pos = ListProperty([0, 0])
        RelativeLayout.__init__(self, **kwargs)
        self.app = app
        self.padding_y = 1
        self.on_press_callback = None
        self.but_remove = None
        self.but_add = None
        self.but_clone = None
        self.but_merge = None
        self.but_remove = None
        self.button_list = []
        self.offset_y = 0
        self.padding_y_per = 0.01
        self.start_padding = Window.height * LAYER_RIBBON_BUTTON_HEIGHT_HINT + LAYERBOX_PADDING[3]
        self.padding_y = Window.height * self.padding_y_per
        self.size_child_per = 0.19
        self.size_hint = LAYER_RIBBON_SIZE_HINT
        self.index = 0
        self._bg_rect = None
        self._bg_frame = None
        self.size = (Window.width * LAYER_RIBBON_SIZE_HINT[0], Window.height * LAYER_RIBBON_SIZE_HINT[1])
        self.layout = RelativeLayout(pos=(0, 0))
        # self.layout = BoxLayout(pos=(0, 0))
        self.layout.bind(children=self._layerbox_layout_on_children)
        self.layout.size_hint = (None, None)
        self.layout.size = (Window.width * self.size_child_per, Window.height * LAYER_RIBBON_SIZE_HINT[1])
        self.layout.canvas.ask_update()
        self.scroll_view = ScrollView(size=(Window.width * LAYER_RIBBON_SIZE_HINT[0], Window.height * LAYER_RIBBON_SIZE_HINT[1]),
                                      pos_hint={'center_x': .5, 'center_y': .5})
        # self.scroll_view.pos = (0, 0)
        # self.scroll_view.scroll_x = 0.5
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)


        self._create_ribbon_buttons()
        self.in_pos1 = (Window.width * LAYER_RIBBON_POS_HINT_1[0], Window.height * LAYER_RIBBON_POS_HINT_1[1])
        self.out_pos1 = (Window.width + 1, Window.height * LAYER_RIBBON_POS_HINT_1[1])
        self.in_pos2 = (Window.width * LAYER_RIBBON_POS_HINT_2[0], Window.height * LAYER_RIBBON_POS_HINT_2[1])
        self.out_pos2 = (Window.width + 1, Window.height * LAYER_RIBBON_POS_HINT_2[1])
        self.pos = (Window.width + 1, Window.height * LAYER_RIBBON_POS_HINT_1[1])
        self.hidden = True
        self.animation_show1 = Animation(pos=self.in_pos1, transition='in_quad', duration=0.3)
        self.animation_hide1 = Animation(pos=self.out_pos1, transition='in_quad', duration=0.3)
        self.animation_show2 = Animation(pos=self.in_pos2, transition='in_quad', duration=0.3)
        self.animation_hide2 = Animation(pos=self.out_pos2, transition='in_quad', duration=0.3)
        self.add_to_undo_callback = None

        # correct auto resize height to previous value
        self.layout.bind(size=self._on_layerbox_layout_size)

    def _layerbox_layout_on_children(self, *args):
        self.layout.height = self.get_layerbox_layout_height()

    def _create_ribbon_buttons(self):
        self.button_layout = BoxLayout(pos=(0, 0), size_hint=(None, None),
                                       size=(self.width, LAYER_RIBBON_BUTTON_HEIGHT_HINT * WIN_HEIGHT),
                                       orientation="horizontal",
                                       spacing=1, padding=[1, 0, 1, 1])
        self.but_add = Button(background_normal=data_path('add.png'),
                              background_down=data_path('add_down.png'), border=[0, 0, 0, 0])
        self.but_clone = Button(background_normal=data_path('clone.png'),
                                background_down=data_path('clone_down.png'), border=[0, 0, 0, 0])
        self.but_merge = Button(background_normal=data_path('merge.png'),
                                background_down=data_path('merge_down.png'),
                                background_disabled_normal=data_path('merge_disable.png'),
                                border=[0, 0, 0, 0])
        self.but_remove = Button(background_normal=data_path('del.png'),
                                 background_down=data_path('del_down.png'),
                                 background_disabled_normal=data_path('del_disable.png'),
                                 border=[0, 0, 0, 0])
        self.button_list = [self.but_add, self.but_clone, self.but_merge, self.but_remove]

        with self.button_layout.canvas:
            Color(0, 0, 0, 0.7)
            self.button_layout_rect = Rectangle(pos=(0, 0),
                                                size=(self.button_layout.size[0], self.button_layout.size[1] + 1))

        def resize(self):
            self.button_layout_rect.size = self.button_layout.size

        self.button_layout.bind(size=lambda *args: resize(self))

        for but in self.button_list:
            self.button_layout.add_widget(but)
        self.add_widget(self.button_layout)

    def get_layerbox_layout_height(self):
        return self.start_padding + self.offset_y * (len(LayerBox.boxlist))

    def _add_layer(self, texture_size):

        size_hint = (1, self.size_child_per)
        pos = (LAYERBOX_PADDING[0], self.start_padding + self.offset_y * len(LayerBox.boxlist))

        lb = LayerBox(app=self.app, texture_size=texture_size, size_hint=size_hint, pos=pos)
        # lb = LayerBox(app=self.app, texture_size=texture_size, size_hint=size_hint)
        lb.bind(_is_active=self.on_layer_box_activate)
        self.layer_box_list.append(lb)
        lb.on_press_callback = self.on_press_callback
        self.offset_y = lb.size[1] + self.padding_y
        lb.put_rects_on_canvas()
        self.layout.add_widget(lb)

        self._update_layerbox_layout_size()

        # with self.layout.canvas:
        #     Color(1, 0, 0, 0.3)
        #     Rectangle(pos=(0, 0), size=self.size)
        self.canvas.ask_update()
        self.scroll_view.scroll_y = 1
        return lb

    def update(self):
        self.canvas.ask_update()

    def new_layer(self, texture_size):
        return self._add_layer(texture_size=texture_size)

    def clone_layer(self, source_lb):
        new_lb = self._add_layer(texture_size=source_lb.layer.texture.size)
        # if source_lb.active:
        #     tex = self.app.aPaint.fbo_get_texture()
        # else:
        #     tex = source_lb.layer.texture
        tex = source_lb.layer.texture

        # new_lb.layer.texture = improc.texture_copy(tex)
        texture = improc.texture_copy(source_lb.layer.texture)
        new_lb.layer.replace_texture(texture)
        new_lb.put_rects_on_canvas()
        self.canvas.ask_update()

    def merge_layer(self, source_lb):
        texture1 = source_lb.get_texture()
        upper_id = LayerBox.boxlist.index(source_lb)
        if upper_id > 0:
            lower_lb = LayerBox.boxlist[upper_id - 1]
            texture2 = lower_lb.get_texture()
            restex = improc.texture_merge(texture1, texture2)
            if lower_lb.is_active:
                improc.texture_replace_data(self.app.aPaint.fbo.texture, restex)
            else:
                lower_lb.layer.texture = restex
            lower_lb.put_rects_on_canvas()

    def remove_layer(self, laybox):
        self.layout.remove_widget(laybox)
        self.layer_box_list.remove(laybox)
        LayerBox.boxlist.remove(laybox)

        self.canvas.ask_update()
        self.update_pos()

    def remove_all_layers(self):
        for laybox in LayerBox.boxlist:
            self.layout.remove_widget(laybox)
            del laybox
            self.canvas.ask_update()
            self.update_pos()
        LayerBox.boxlist[:] = []
        self.layer_box_list[:] = []

    def on_layer_box_list(self, instance, value):
        self.but_merge.disabled = False
        self.but_remove.disabled = False
        if len(value) <= 1:
            self.but_remove.disabled = True
        else:
            self.but_remove.disabled = False
        if len(value) <= 1:
            self.but_merge.disabled = True
        else:
            self.but_merge.disabled = False
        if self.get_active_layerbox() is self.layer_box_list[0]:
            self.but_merge.disabled = True

    def on_layer_box_activate(self, instance, value):
        if value is True:
            if instance is self.layer_box_list[0]:
                self.but_merge.disabled = True
            elif len(self.layer_box_list) > 1:
                self.but_merge.disabled = False

    def on_layerbox_dragging(self):
        if LayerBox.dragged_box:
            dragged_box = LayerBox.dragged_box
            dragged_index = LayerBox.boxlist.index(dragged_box)
            for layerbox in LayerBox.boxlist:
                if dragged_box is not layerbox:
                    if dragged_box.y > layerbox.y - layerbox.height/2 and dragged_box.y < layerbox.y:
                        y = self.start_padding + self.offset_y * dragged_index
                        layerbox.set_pos((layerbox.x, y))
                        replaced_index = LayerBox.boxlist.index(layerbox)

                        temp_box = LayerBox.boxlist[replaced_index]
                        LayerBox.boxlist[replaced_index] = LayerBox.boxlist[dragged_index]
                        LayerBox.boxlist[dragged_index] = temp_box

    def on_drop(self):
        if LayerBox.dragged_box:
            y = self.start_padding + self.offset_y * LayerBox.boxlist.index(LayerBox.dragged_box)
            LayerBox.dragged_box.set_pos((LayerBox.dragged_box.x, y))
            LayerBox.dragged_box.drop()
            self.on_press_callback()

    def blit_layers_to_texture(self):
        fbo = Fbo(size=LayerBox.active.layer.texture.size)
        fbo.texture.mag_filter = 'nearest'
        fbo.texture.min_filter = 'nearest'
        with fbo:
            Color(1, 1, 1, 1)
            for lb in LayerBox.boxlist:
                Rectangle(pos=(0, 0), size=lb.layer.texture.size, texture=lb.layer.texture)
        fbo.draw()
        return fbo.texture

    def update_pos(self):
        ind = 0
        for lb in LayerBox.boxlist:
            lb.set_pos((LAYERBOX_PADDING[0], self.start_padding + self.offset_y * ind))
            self.canvas.ask_update()
            ind += 1

    def layers_count(self):
        return len(LayerBox.boxlist)

    def _on_layerbox_layout_size(self, instance, value):
        if value[1] != self._calc_layerbox_layout_height():
            self._update_layerbox_layout_size()

    def _update_layerbox_layout_size(self):
        self.layout.size[1] = self._calc_layerbox_layout_height()

    def _calc_layerbox_layout_height(self):
        height = self.start_padding + self.offset_y * len(LayerBox.boxlist)
        if height < Window.height * LAYER_RIBBON_SIZE_HINT[1]:
            height = Window.height * LAYER_RIBBON_SIZE_HINT[1]
        return height

    def on_touch_down(self, touch):

        if super(LayerRibbon, self).on_touch_down(touch):
            return True

        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.ud[self] = True
        self.dispatch('on_press')
        # self.on_press(touch)
        return True

    def on_touch_move(self, touch):

        if super(LayerRibbon, self).on_touch_move(touch):
            self.on_layerbox_dragging()
            return True

        return self in touch.ud

    def on_touch_up(self, touch):
        self.on_drop()
        if super(LayerRibbon, self).on_touch_up(touch):

            return True
        return self in touch.ud

    def redraw_back(self):
        if self._bg_rect:
            self.canvas.before.remove(self._bg_rect)
            self._bg_rect = None
        if self._bg_frame:
            self.canvas.before.remove(self._bg_frame)
            self._bg_frame = None
        with self.canvas.before:
            Color(88. / 256, 88. / 256, 88. / 256, 76. / 256)
            self._bg_rect = Rectangle(pos=(0, 0), size=(self.size[0], WIN_HEIGHT * LAYER_RIBBON_SIZE_HINT[1]))
        with self.canvas.before:
            Color(0, 0, 0, 0.7)
            self._bg_frame = Line(rectangle=(0, 1, self.size[0], WIN_HEIGHT * LAYER_RIBBON_SIZE_HINT[1] - 1))
        # with self.layout.canvas:
        #     Color(1, 0, 0, 0.5)
        #     Rectangle(pos=(0,0), size=self.size)

        self.canvas.ask_update()

    def put_rects_on_canvas(self):
        self.redraw_back()
        LayerBox.active.put_rects_on_canvas()

    def put_texture_on_canvas(self, texture):
        self.redraw_back()
        LayerBox.active.put_texture_on_canvas(texture)

    def get_active_layerbox(self):
        return LayerBox.active

    def get_active_layer_id(self):
        self.active_layer_id = LayerBox.boxlist.index(LayerBox.active)
        return self.active_layer_id

    def get_active_layer(self):
        return LayerBox.active.layer

    def get_last_active_layer(self):
        if LayerBox.last_active is None:
            return LayerBox.active.layer
        return LayerBox.last_active.layer

    def get_textures_list(self):
        return [lbox.layer.texture for lbox in LayerBox.boxlist]

    def on_press(self, touch):
        pass
        # LayerBubble.hide_all()

    def on_release(self):
        RelativeLayout.on_release(self)

    def animate_hide(self, *args):
        if not self.hidden:
            if self.app.palette_hidden():
                self.animation_hide1.start(self)
            else:
                self.animation_hide2.start(self)
            self.hidden = True

    def animate_show(self, *args):
        if self.hidden:
            if self.app.palette_hidden():
                self.animation_show1.start(self)
            else:
                self.animation_show2.start(self)
            self.hidden = False

    def animate_switch(self, *args):
        if not self.hidden:
            self.animate_hide()
        else:
            self.animate_show()

    def animate_move(self, position):
        if position == 1:
            self.animation_show1.start(self)
        elif position == 2:
            self.animation_show2.start(self)

