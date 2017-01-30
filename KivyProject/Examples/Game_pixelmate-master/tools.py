from math import modf, atan2, sin, cos, pi
from functools import partial

from kivy.graphics import Color, Ellipse, Quad, Rectangle
from kivy.graphics.vertex_instructions import Line
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton

import improc
from globals import *


class ToolBehavior():
    instance_list = []

    @classmethod
    def scale(cls):
        for i in ToolBehavior.instance_list:
            i.on_scale()

    def __init__(self):
        ToolBehavior.instance_list.append(self)

    def on_scale(self):
        pass


class BarBubble(Bubble):
    def __init__(self, layout, **kwargs):
        Bubble.__init__(self, **kwargs)
        self.size_hint = (None, None)
        self.size = (Window.size[0] * 0.13 * 5, Window.size[1] * LAYER_RIBBON_BUTTON_HEIGHT_HINT * 1.3)
        self.orientation = 'horizontal'
        self.show_arrow = False
        self.layout = layout
        self.but_list = []

    def add_button(self, text, callback):
        self.but_list.append(BubbleButton(text=text, on_press=partial(self.button_callback, callback)))
        self.add_widget(self.but_list[-1])

    def disable_button(self, text, state):
        for but in self.but_list:
            if but.text == text:
                but.disabled = state

    def button_callback(self, callback, *args):
        callback()
        self.hide()

    def on_touch_down(self, touch):
        if super(BarBubble, self).on_touch_down(touch):
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
        if super(BarBubble, self).on_touch_move(touch):
            return True
        return self in touch.ud

    def show(self):
        if self not in self.layout.children:
            self.layout.add_widget(self)

    def hide(self):
        if self in self.layout.children:
            self.layout.remove_widget(self)


class VertexTool():
    app = APP()
    item_list = []
    round_width = 40

    @classmethod
    def update_graphics(cls):
        if cls.item_list:
            for line in cls.item_list:
                line._update_graphics()

    @classmethod
    def on_setting_change(cls):
        cls.round_width = APP().config.getint('editor', 'tools_touch_point_size')
        cls.update_graphics()

    def __init__(self, app):
        VertexTool.app = app
        self.catch_point = [0, 0, 0, 0]
        self.point = [0, 0, 0, 0]
        self.poly = None
        self.round = [None, None]
        self.state = None
        self.rect = None
        self.canvas = app.aPaintLayout.canvas
        self.color = None
        self.line = None
        self.catched_round = None
        self.catched_line = False
        self._catch_pos = None
        self.fbo = None
        self.render_fbo = None
        self.on_render_callback = None
        VertexTool.item_list.append(self)

    def on_touch_down(self, touch, render_fbo, fbo):
        if self.state is None:
            self.state = 'draw'
            self._set_point(0, touch)
            self._remove_graphics_rounds()
            self.fbo = fbo
        if self.state == 'edit':
            round_index = self._round_collide(touch.pos)
            if round_index is not None:
                self.catched_round = round_index
            elif self._poly_collide(touch.pos):
                self._catch_line(touch.pos)
            else:
                self._render_and_reset_state(render_fbo, fbo)

    def on_touch_up(self, touch):
        if self.state == 'draw':
            self.state = 'edit'
            self._set_point(1, touch)
            self._add_graphics_rounds()
            self._add_graphics_rect()
        self.catched_round = None
        self.catched_line = False

    def on_touch_move(self, touch, fbo):
        if self.state == 'draw':
            self._remove_graphics_line(fbo)
            self._set_point(1, touch)
            self._add_graphics_line(fbo)
        elif self.state == 'edit':
            if self.catched_round is not None:
                self._remove_graphics_line(fbo)
                self._remove_graphics_rounds(self.catched_round)
                self._remove_graphics_rect()
                self._set_point(self.catched_round, touch)
                self._add_graphics_line(fbo)
                self._add_graphics_rounds(self.catched_round)
                self._add_graphics_rect()
            elif self.catched_line:
                self._remove_graphics_line(fbo)
                self._remove_graphics_rounds()
                self._remove_graphics_rect()
                dx, dy = self._get_point_offset(touch.pos)
                self.point[0], self.point[1] = self.catch_point[0] + dx, self.catch_point[1] + dy
                self.point[2], self.point[3] = self.catch_point[2] + dx, self.catch_point[3] + dy
                self._add_graphics_line(fbo)
                self._add_graphics_rounds()
                self._add_graphics_rect()

    def _round_collide(self, pos):
        for ind in xrange(0, 2):
            if pos[0] > self.round[ind].pos[0]:
                if pos[0] < self.round[ind].pos[0] + VertexTool.round_width:
                    if pos[1] > self.round[ind].pos[1]:
                        if pos[1] < self.round[ind].pos[1] + VertexTool.round_width:
                            return ind
        return None

    def _poly_collide(self, pos):
        x, y = pos
        x1, y1 = self.point[0], self.point[1]
        x2, y2 = self.point[2], self.point[3]
        dx1, dy1 = self._get_pos_by_angle_from_round(pi / 2)
        dx2, dy2 = self._get_pos_by_angle_from_round(-pi / 2)
        self.poly = ((x1 + dx1, y1 + dy1), (x1 + dx2, y1 + dy2), (x2 + dx2, y2 + dy2), (x2 + dx1, y2 + dy1))
        poly = self.poly
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def __get_angle_alpha(self):
        x1, y1 = self.point[0], self.point[1]
        x2, y2 = self.point[2], self.point[3]
        return atan2(y2 - y1, x2 - x1)

    def _get_pos_by_angle_from_round(self, angle):
        alpha = self.__get_angle_alpha()
        return cos(alpha + angle) * VertexTool.round_width / 2, sin(alpha + angle) * VertexTool.round_width / 2

    def _translate_pos(self, pos):
        x, y = pos
        step_x = x // self.app.aPaint.scale
        step_y = y // self.app.aPaint.scale
        ox = modf(self.app.aPaint.fbo_rect.pos[0] / self.app.aPaint.scale)[0]
        oy = modf(self.app.aPaint.fbo_rect.pos[1] / self.app.aPaint.scale)[0]
        return [step_x * self.app.aPaint.scale + ox * self.app.aPaint.scale,
                step_y * self.app.aPaint.scale + oy * self.app.aPaint.scale]

    def _set_point(self, index, touch):
        if index == 0:
            self.point[0] = touch.x
            self.point[1] = touch.y
        elif index == 1:
            self.point[2] = touch.x
            self.point[3] = touch.y

    def _catch_line(self, pos):
        self.catched_line = True
        self.catch_point = self.point[:]
        self._catch_pos = pos

    def _get_point_offset(self, pos):
        return pos[0] - self._catch_pos[0], pos[1] - self._catch_pos[1]

    def __add_graphics_debug_poly(self):
        with self.canvas:
            self.color = Color(0, 1, 1, 1)
            poly = []
            for lst in self.poly:
                poly.extend(lst)
            Quad(points=poly)
        self.canvas.ask_update()

    def _add_graphics_rounds(self, index=None):
        with self.canvas:
            self.color = Color(1, 0, 0, 0.3)
            if index == 0 or index is None:
                self.round[0] = Ellipse(
                    pos=(self.point[0] - VertexTool.round_width / 2, self.point[1] - VertexTool.round_width / 2),
                    size=(VertexTool.round_width, VertexTool.round_width))
            if index == 1 or index is None:
                self.round[1] = Ellipse(
                    pos=(self.point[2] - VertexTool.round_width / 2, self.point[3] - VertexTool.round_width / 2),
                    size=(VertexTool.round_width, VertexTool.round_width))
        self.canvas.ask_update()

    def _add_graphics_line(self, fbo):
        fbo.bind()
        with fbo:
            fbo.add(self.app.aColor)
            fbo_coord = [self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1],
                         self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1]]

            points = map(self._translate_point, self.point, fbo_coord)
            self.line = self._create_body(points=points, width=1)
        fbo.release()
        fbo.draw()

    def _create_body(self, points, width):
        pass

    def _add_graphics_rect(self):
        with self.canvas:
            self.color = Color(1, 0, 0, 0.3)
            self.rect = self._create_drag_body(points=self.point, width=VertexTool.round_width / 2)
        self.canvas.ask_update()

    def _create_drag_body(self, points, width):
        pass

    def _add_graphics(self, fbo):
        self._add_graphics_line(fbo)
        self._add_graphics_rounds()
        self._add_graphics_rect()

    def _remove_graphics_line(self, fbo):
        fbo.bind()
        fbo.clear_buffer()
        if self.line in fbo.children:
            fbo.remove(self.line)
        fbo.release()
        fbo.draw()

    def _remove_graphics_rounds(self, index=None):
        if index is None:
            for round in self.round:
                if round in self.canvas.children:
                    self.canvas.remove(round)
        else:
            if self.round[index] in self.canvas.children:
                self.canvas.remove(self.round[index])
        self.canvas.ask_update()

    def _remove_graphics_rect(self):
        if self.rect in self.canvas.children:
            self.canvas.remove(self.rect)
        self.canvas.ask_update()

    def _remove_graphics(self, fbo):
        self._remove_graphics_line(fbo)
        self._remove_graphics_rounds()
        self._remove_graphics_rect()

    def _update_graphics(self):
        if self.state == 'edit':
            self._remove_graphics(self.fbo)
            self._add_graphics(self.fbo)

    def _render_to(self, fbo):
        fbo.bind()
        with fbo:
            fbo.add(self.app.aColor)
            fbo_coord = [self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1],
                         self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1]]

            points = map(self._translate_point, self.point, fbo_coord)

            self._create_body(points, width=1)
        fbo.release()
        fbo.draw()
        if callable(self.on_render_callback):
            self.on_render_callback()

    def _render_and_reset_state(self, render_fbo, fbo):
        self.state = None
        self._render_to(render_fbo)
        self._remove_graphics_line(fbo)
        self._remove_graphics_rounds()
        self._remove_graphics_rect()

    def reset_state(self, fbo):
        self.state = None

        self._remove_graphics_line(fbo)
        self._remove_graphics_rounds()
        self._remove_graphics_rect()

    def _translate_point(self, mx, fbo_x):
        return int(mx / self.app.aPaint.scale - fbo_x)

    def _on_focus_lost(self):
        pass


class LineTool(VertexTool):
    def _create_body(self, points, width):
        return Line(points=points, width=width)

    def _create_drag_body(self, points, width):
        return Line(points=points, width=width)


class RectTool(VertexTool):
    def _create_body(self, points, width):
        return Line(rectangle=(points[0], points[1], points[2] - points[0], points[3] - points[1]))

    def _create_drag_body(self, points, width):
        return Line(points=points, width=width)


class EllipseTool(VertexTool):
    def _create_body(self, points, width):
        return Line(ellipse=(points[0], points[1], points[2] - points[0], points[3] - points[1]))

    def _create_drag_body(self, points, width):
        return Line(points=points, width=width)


class SelectTool(VertexTool):
    def __init__(self, app):
        VertexTool.__init__(self, app)

        self.layout = self.app.aPaintLayout
        self.context_menu = BarBubble(self.app.aPaintLayout)
        self.context_menu.pos = [Window.width * TOOLBAR_LAYOUT_SIZE_HINT[0], Window.height - self.context_menu.size[1]]
        self.context_menu.width = Window.width - Window.width * (
            TOOLBAR_LAYOUT_SIZE_HINT[0] + PALETTE_LAYOUT_SIZE_HINT[0])
        self.context_menu.add_button('copy', self.selection_copy)
        self.context_menu.add_button('cut', self.selection_cut)
        self.context_menu.add_button('paste', self.selection_paste)
        self.context_menu.add_button('delete', self.selection_del)

    def on_touch_down(self, touch, render_fbo, fbo):
        if self.state is None:
            self.state = 'draw'
            self._set_point(0, touch)
            self._remove_graphics_rounds()
            self.fbo = fbo
        if self.state == 'edit':
            round_index = self._round_collide(touch.pos)
            if round_index is not None:
                self.catched_round = round_index
            elif self._poly_collide(touch.pos):
                self._catch_line(touch.pos)
            else:
                self._reset_state(fbo)
            self.context_menu.hide()

    def on_touch_move(self, touch, fbo):
        if self.state == 'draw':
            self._remove_graphics_line(fbo)
            self._set_point(1, touch)
            self._add_graphics_line(fbo)
        elif self.state == 'edit':
            if self.catched_round is not None:
                self._remove_graphics_line(fbo)
                self._remove_graphics_rounds(self.catched_round)
                self._remove_graphics_rect()
                self._set_point(self.catched_round, touch)
                self._add_graphics_line(fbo)
                self._add_graphics_rounds(self.catched_round)
                self._add_graphics_rect()
            elif self.catched_line:
                self._remove_graphics_line(fbo)
                self._remove_graphics_rounds()
                self._remove_graphics_rect()
                dx, dy = self._get_point_offset(touch.pos)
                self.point[0], self.point[1] = self.catch_point[0] + dx, self.catch_point[1] + dy
                self.point[2], self.point[3] = self.catch_point[2] + dx, self.catch_point[3] + dy
                self._add_graphics_line(fbo)
                self._add_graphics_rounds()
                self._add_graphics_rect()

    def on_touch_up(self, touch):
        if self.state == 'draw':
            self.state = 'edit'
            self._set_point(1, touch)
            self._add_graphics_rounds()
            self._add_graphics_rect()
        if self.state == 'edit':
            if self.app.aPaint.tool_buffer.is_empty():
                self.context_menu.disable_button('paste', True)
            else:
                self.context_menu.disable_button('paste', False)
            self.context_menu.show()
        self.catched_round = None
        self.catched_line = False

    def _poly_collide(self, pos):
        point = self.point[:]
        if self.point[0] > self.point[2]:
            point[0] = self.point[2]
            point[2] = self.point[0]
        if self.point[1] > self.point[3]:
            point[1] = self.point[3]
            point[3] = self.point[1]
        if point[0] < pos[0] < point[2] and point[1] < pos[1] < point[3]:
            return True
        return False

    def _set_point(self, index, touch):
        if index == 0:
            self.point[0], self.point[1] = self._translate_pos(touch.pos)
        elif index == 1:
            self.point[2], self.point[3] = self._translate_pos(touch.pos)

    def _reset_state(self, fbo):
        self.state = None
        self._remove_graphics_line(fbo)
        self._remove_graphics_rounds()
        self._remove_graphics_rect()

    def _create_body(self, points, width):
        return Quad(points=(points[0], points[1], points[0], points[3], points[2], points[3], points[2], points[1]),
                    width=width)

    def _create_drag_body(self, points, width):
        pass

    def _add_graphics_line(self, fbo):
        fbo.bind()
        with fbo:
            Color(1, 0, 0, 0.5)
            fbo_coord = [self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1],
                         self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1]]

            points = map(self._translate_point, self.point, fbo_coord)
            self.line = self._create_body(points=points, width=1)
        fbo.release()
        fbo.draw()

    def get_selection_size(self):
        size = [abs(self.point[2] - self.point[0]), abs(self.point[3] - self.point[1])]
        translated_size = [int(size[0] / self.app.aPaint.scale), int(size[1] / self.app.aPaint.scale)]
        pos1 = self.get_selection_pos()
        pos2 = self.get_selection_reverse_pos()
        rsize = [pos2[0] - pos1[0], pos2[1] - pos1[1]]
        return rsize

    def get_selection_pos(self):
        fbo_coord = [self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1],
                     self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1]]

        point = map(self._translate_point, self.point, fbo_coord)
        if point[0] > point[2]:
            point[0] = point[2]
        if point[1] > point[3]:
            point[1] = point[3]
        pos = [point[0], point[1]]
        if pos[0] < 0:
            pos[0] = 0
        if pos[1] < 0:
            pos[1] = 0
        return pos

    def get_selection_reverse_pos(self):
        fbo_coord = [self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1],
                     self.app.aPaint.fbo_rect.pos[0], self.app.aPaint.fbo_rect.pos[1]]

        point = map(self._translate_point, self.point, fbo_coord)
        if point[0] > point[2]:
            point[2] = point[0]
        if point[1] > point[3]:
            point[3] = point[1]
        pos = [point[2], point[3]]
        if pos[0] > self.app.aPaint.fbo_rect.texture.size[0]:
            pos[0] = self.app.aPaint.fbo_rect.texture.size[0]
        if pos[1] > self.app.aPaint.fbo_rect.texture.size[1]:
            pos[1] = self.app.aPaint.fbo_rect.texture.size[1]
        return pos


    def selection_copy(self):
        tex = self.app.layer_ribbon.blit_layers_to_texture()
        self.app.aPaint.tool_buffer.get_from_texture(tex, self.get_selection_pos(), self.get_selection_size())

    def selection_del(self):
        x, y = self.get_selection_pos()
        w, h = self.get_selection_size()

        self.app.aPaint.fbo.bind()
        improc.texture_replace_color(tex=self.app.aPaint.fbo.texture, pos=(x, y), color=0, size=(w, h))
        self.app.aPaint.fbo.release()
        self.app.aPaint.fbo.clear()
        self.app.aPaint.fbo.draw()
        self.app.aPaint.canvas.ask_update()

    def selection_paste(self):
        self._reset_state(self.fbo)

        self.app.aPaint.tool_buffer.enable(self.app.aPaint.fbo,
                                           pos=(
                                               self.app.aPaint.fbo_rect.size[0] / 2,
                                               self.app.aPaint.fbo_rect.size[1] / 2))
        self.app.aPaint.canvas_put_drawarea()

    def selection_cut(self):
        self.selection_copy()
        self.selection_del()


class BufferTool(ToolBehavior):
    def __init__(self, app, **args):
        ToolBehavior.__init__(self)
        self.rect = None
        self.app = app
        self.parent_layout = app.aPaint
        self.canvas = app.aPaint.canvas
        self.fbo = app.aPaint.fbo
        self.enabled = False
        self.texture = None
        self.pos = [0, 0]
        self.size = [0, 0]
        self.state = None
        self.on_render_callback = None
        self._create_bar_bubble()

    def _create_bar_bubble(self):
        self.menu = BarBubble(self.app.aPaintLayout)
        self.menu.pos = [Window.width * TOOLBAR_LAYOUT_SIZE_HINT[0], Window.height - self.menu.size[1]]
        self.menu.width = Window.width - Window.width * (
            TOOLBAR_LAYOUT_SIZE_HINT[0] + PALETTE_LAYOUT_SIZE_HINT[0])
        self.menu.add_button('ok', self.put_on_fbo)
        self.menu.add_button('cancel', self._cancel_paste)

    def enable(self, fbo, pos):
        self.enabled = True
        self._create_rect(fbo, pos=pos)
        self.menu.show()

    def disable(self):
        self.enabled = False
        self.menu.hide()

    def is_empty(self):
        if self.texture:
            return False
        return True

    def put_on_fbo(self):
        self.enabled = False
        self.menu.hide()
        if callable(self.on_render_callback):
            self.on_render_callback()

    def _create_rect(self, fbo, pos):
        if self.texture:
            with fbo:
                Color(1, 1, 1, 1)
                self.pos = pos
                self.size = self.texture.size
                self.rect = Rectangle(pos=self.pos, texture=self.texture, size=self.texture.size)

    def _add_graphics(self, fbo):
        fbo.bind()
        fbo.add(self.rect)
        fbo.release()
        fbo.draw()
        self.canvas.ask_update()

    def _remove_graphics(self, fbo):

        fbo.bind()
        fbo.clear_buffer()
        if self.rect in fbo.children:
            fbo.remove(self.rect)
        fbo.release()
        fbo.draw()


    def get_from_texture(self, tetxure, pos, size):
        x, y = pos
        w, h = size
        self.texture = improc.texture_copy_region(tetxure, (x, y, w, h))
        self.texture.mag_filter = 'nearest'
        self.texture.min_filter = 'nearest'
        self.texture = improc.texture_flip(self.texture)

    def _cancel_paste(self):
        self._remove_graphics(self.fbo)
        self.disable()

    def on_touch_down(self, touch):
        if self.enabled:
            if self.collide_point(touch.pos):
                self.state = 'move'

    def on_touch_up(self, touch):
        self.state = None

    def on_touch_move(self, touch, fbo):
        scaled_pos = self.app.aPaint.scale_pos(touch.pos)
        if self.state == 'move':
            self.fbo = fbo
            self._remove_graphics(fbo)
            self.pos = scaled_pos[0] - self.size[0] / 2, scaled_pos[1] - self.size[1] / 2
            self.rect.pos = self.pos
            self._add_graphics(fbo)

    def collide_point(self, pos):
        x, y = self.app.aPaint.scale_pos(pos)
        if self.pos[0] < x < self.pos[0] + self.size[0] and self.pos[1] < y < self.pos[1] + self.size[1]:
            return True
        return False

    def on_scale(self):
        pass

