import math

from kivy.uix.stencilview import StencilView
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.graphics.fbo import Fbo
from kivy.graphics.texture import Texture
from kivy.graphics.opengl import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE
from kivy.graphics import PushMatrix, PopMatrix
from kivy.graphics import context_instructions
from kivy.vector import Vector
from kivy.properties import NumericProperty

from globals import *
from tools import ToolBehavior
import layer
import improc
import dialog


def distance(pos1, pos2):
    return Vector(pos1).distance(pos2)


class Paint(StencilView):
    scale = NumericProperty()

    def __init__(self, app, **kwargs):
        StencilView.__init__(self, **kwargs)
        self.app = app
        self.xx = 0
        self.scale = 1.0
        self.size_hint = (None, None)
        self.cursor_pos = (0, 0)
        self.fbo_size = DEFAULT_IMAGE_SIZE
        self.fbo = None
        self.fbo_rect = None
        self.tool_fbo = None
        self.tool_fbo_rect = None
        self.bg_rect = None
        self.rect = None
        self.fbo_clear_color = (1, 1, 1, 1)
        self.layer_undo_stack = []
        self.undo_layer_index = 0
        self.layer_rect = []
        self.fbo_create_on_canvas()
        self.touches = []
        self.move_image = False
        self.active_layer = None
        self.tool_buffer_enabled = True
        self.px = None
        self.py = None
        self.grid_texture = None
        self.active_layer_last_texture = None

    def grid_create(self, size):
        self.grid_texture = Texture.create(size=size, colorfmt='rgba', bufferfmt='ubyte')
        tex = improc.texture_draw_grid(self.grid_texture, 255, 4)
        return tex

    def fbo_create(self, size, tex=None):
        if tex is None:
            tex = Texture.create(size=size, colorfmt='rgba', bufferfmt='ubyte')
            tex.mag_filter = 'nearest'
            tex.min_filter = 'nearest'
        if self.fbo is None:
            self.fbo = Fbo(size=size, texture=tex)
            self.fbo.texture.mag_filter = 'nearest'
            self.fbo.texture.min_filter = 'nearest'
        else:
            self.fbo = Fbo(size=size, texture=tex)
            self.fbo.texture.mag_filter = 'nearest'
            self.fbo.texture.min_filter = 'nearest'
        tool_tex = Texture.create(size=size, colorfmt='rgba', bufferfmt='ubyte')
        tool_tex.mag_filter = 'nearest'
        tool_tex.min_filter = 'nearest'
        if self.tool_fbo is None:
            self.tool_fbo = Fbo(size=size, texture=tool_tex)
            self.tool_fbo.texture.mag_filter = 'nearest'
            self.tool_fbo.texture.min_filter = 'nearest'
        else:
            self.tool_fbo = Fbo(size=size, texture=tool_tex)
            self.tool_fbo.texture.mag_filter = 'nearest'
            self.tool_fbo.texture.min_filter = 'nearest'
        return self.fbo

    def refbo(self):
        tex = Texture.create(size=self.fbo.texture.size, colorfmt='rgba', bufferfmt='ubyte')
        self.fbo = Fbo(size=tex.size, texture=tex)
        self.fbo.texture.mag_filter = 'nearest'
        self.fbo.texture.min_filter = 'nearest'
        self.fbo.draw()
        self.canvas.ask_update()

    def canvas_put_drawarea(self, texture=None):
        self.canvas.clear()
        if texture:
            self.fbo_size = texture.size
            self.fbo_create(texture.size, tex=texture)
        self.bg_rect = layer.Layer.layer_bg_rect
        with self.canvas:
            self.canvas.add(self.bg_rect)
            Color(1, 1, 1, 1)
            for laybox in layer.LayerBox.boxlist:
                if laybox.layer:
                    if laybox.layer.texture and laybox.layer.visible:
                        self.canvas.add(laybox.layer.rect)
                        laybox.layer.rect.pos = self.fbo_rect.pos

                if self.tool_buffer_enabled:
                    self.tool_fbo_rect = Rectangle(pos=self.fbo_rect.pos, size=self.tool_fbo.texture.size,
                                                   texture=self.tool_fbo.texture)
        self.fbo_update_pos()
        self.fbo.draw()
        self.canvas.ask_update()

    def fbo_create_on_canvas(self, size=None, pos=(0, 0)):
        self.canvas.clear()
        if size is None:
            size = self.fbo_size
        else:
            self.fbo_size = size
        self.fbo_create(size)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.fbo_rect = Rectangle(texture=self.fbo.texture, pos=pos, size=self.fbo.texture.size)
            self.tool_fbo_rect = Rectangle(texture=self.tool_fbo.texture, pos=pos, size=self.tool_fbo.texture.size)
        self.fbo.draw()
        self.canvas.ask_update()


    def fbo_clear(self):
        self.fbo.bind()
        self.fbo.clear()
        self.fbo.clear_color = self.fbo_clear_color
        self.fbo.clear_buffer()
        self.fbo.release()
        self.fbo.draw()

    def fbo_update_pos(self):
        x = self.app.aPaintLayout.size[0] / self.scale / 2 - self.fbo.size[0] / 2
        y = self.app.aPaintLayout.size[1] / self.scale / 2 - self.fbo.size[1] / 2
        self.fbo_rect.pos = (x, y)
        self.tool_fbo_rect.pos = (x, y)
        if self.bg_rect:
            self.bg_rect.pos = (x, y)
        if self.app.layer_ribbon:
            for lb in layer.LayerBox.boxlist:
                if lb.layer.rect:
                    lb.layer.rect.pos = self.fbo_rect.pos

    def fbo_move_by_offset(self, offset):
        if self.bg_rect:
            self.bg_rect.pos = self.bg_rect.pos[0] + offset[0], self.bg_rect.pos[1] + offset[1]
            self.fbo_rect.pos = self.bg_rect.pos
            self.tool_fbo_rect.pos = self.bg_rect.pos
        if self.app.layer_ribbon:
            for lb in layer.LayerBox.boxlist:
                if lb.layer.rect:
                    lb.layer.rect.pos = self.fbo_rect.pos
        # self.ox, self.oy = self.bg_rect.pos
    #
    def fbo_render(self, touch, width):
        self.fbo.bind()
        if touch and touch.ud.has_key('line'):
            with self.fbo:
                self.fbo.add(self.app.aColor)
                d = width
                self.cursor_pos = ((touch.x - d / 2) / self.scale - self.fbo_rect.pos[0],
                                   (touch.y - d / 2) / self.scale - self.fbo_rect.pos[1])
                touch.ud['line'].points += self.cursor_pos
        self.fbo.release()
        self.fbo.draw()
        self.canvas.ask_update()

    def fbo_get_texture(self):
        return self.fbo.texture

    def fbo_get_pixel_color(self, touch, format='1'):
        self.fbo.bind()
        x = touch.x / self.scale - self.fbo_rect.pos[0]
        y = touch.y / self.scale - self.fbo_rect.pos[1]
        data = glReadPixels(x, y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)
        self.fbo.release()
        if format == '1':
            c = [ord(a) / 255.0 for a in data]
        else:
            c = [ord(a) for a in data]
        return c

    def fbo_fill_region(self, touch):
        x = int(touch.x / self.scale - self.fbo_rect.pos[0])
        y = int(touch.y / self.scale - self.fbo_rect.pos[1])
        improc.fillimage(self.fbo, (x, y), [int(255 * c) for c in self.app.aColor.rgba])
        self.canvas.ask_update()

    def fbo_replace_color(self, touch, width):
        cx = int(touch.x / self.scale - self.fbo_rect.pos[0])
        cy = int(touch.y / self.scale - self.fbo_rect.pos[1])
        if self.px is None:
            self.px = cx
        if self.py is None:
            self.py = cy
        if (cx - self.px) > 0:
            tg_alpha = float((cy - self.py)) / (cx - self.px)
            step = int(math.copysign(1, tg_alpha))
            if abs(cx - self.px) > abs(cy - self.py):
                coords = [(x, self.py + (x - self.px) * tg_alpha) for x in xrange(int(self.px), int(cx))]
            else:
                coords = [(self.px + (y - self.py) / tg_alpha, y) for y in xrange(int(self.py), int(cy), step)]
        elif (cx - self.px) < 0:
            tg_alpha = float((cy - self.py)) / (cx - self.px)
            step = int(math.copysign(1, tg_alpha))
            if abs(cx - self.px) > abs(cy - self.py):
                coords = [(x, self.py + (x - self.px) * tg_alpha) for x in xrange(int(cx), int(self.px))]
            else:
                coords = [(self.px + (y - self.py) / tg_alpha, y) for y in xrange(int(cy), int(self.py), step)]
        elif (cx - self.px) == 0:
            if (cy - self.py) > 0:
                coords = [(cx, y) for y in xrange(int(self.py), int(cy))]
            elif (cy - self.py) < 0:
                coords = [(cx, y) for y in xrange(int(cy), int(self.py))]
            else:
                coords = [(cx, cy), ]
        self.fbo.bind()
        for (x, y) in coords:
            improc.texture_replace_color(tex=self.fbo.texture, pos=(x, y), color=0, size=(width, width))
        self.fbo.release()
        self.fbo.clear()
        self.fbo.draw()
        self.canvas.ask_update()
        self.px = cx
        self.py = cy

    def pos_to_widget(self, touch):
        return self.to_widget(touch.x, touch.y)

    def scale_canvas(self, zoom):
        with self.canvas.before:
            PushMatrix()
            self.scale *= zoom
            context_instructions.Scale(zoom)
        with self.canvas.after:
            PopMatrix()
        self.fbo_update_pos()

    def on_scale(self, instance, scale):
        ToolBehavior.scale()

    def scale_pos(self, pos):
        return [pos[0] / self.scale - self.fbo_rect.pos[0],
                pos[1] / self.scale - self.fbo_rect.pos[1]]

    def scaled_pos(self):
        return [self.fbo_rect.pos[0] * self.scale,
                self.fbo_rect.pos[1] * self.scale]

    def scaled_size(self):
        return [self.fbo_rect.texture.size[0] * self.scale,
                self.fbo_rect.texture.size[1] * self.scale]

    def add_touch(self, touch):
        if touch and len(self.touches) < 2:
            self.touches.append(touch)
        if len(self.touches) >= 2:
            self.touch_dist = self.touches[0].distance(self.touches[1])
            self.touch_dist_const = self.touch_dist
            self.first_touch = self.touches[0]

    def double_touch(self):
        if len(self.touches) > 1:
            return True

    # def double_touch_distance(self):
    #     return Vector(self.touches[0].pos).distance(self.touches[1].pos)

    def touch_responce(self):
        result = False
        if len(self.touches) >= 2:
            pos1 = self.pos_to_widget(self.touches[0])
            pos2 = self.touches[1].pos
            dist = distance(pos1, pos2)
            if dist > self.touch_dist + 10:
                self.touch_dist = dist
                result = 2
            elif dist <= self.touch_dist - 10:
                self.touch_dist = dist
                result = 1
            if abs(self.touch_dist_const - dist) < 10:
                result = 3
            return result
        return False

    def on_touch_down(self, touch):
        self.tool_buffer.on_touch_down(touch)

        if self.collide_point(*touch.pos):
            if self.app.config.getint('toolbars', 'toolbar_autohide'):
                self.app.toolbar.animate_hide()
            if self.app.config.getint('toolbars', 'palette_autohide'):
                self.app.palette.animate_hide()
            if self.app.config.getint('toolbars', 'layer_ribbon_autohide'):
                self.app.layer_ribbon.animate_hide()

        if not self.collide_point(*touch.pos):
            if self.app.active_tool == TOOL_LINE:
                self.tool_line._render_and_reset_state(self.fbo, self.tool_fbo)
                self.fbo.draw()
                self.canvas.ask_update()

            return False

        touch.grab(self)

        self.add_touch(touch)

        if len(self.touches) == 1:
            self.active_layer_backup_texture()

        if self.double_touch():
            self.active_layer_set_last_backup_texture()
            return

        if not self.app.layer_ribbon.get_active_layer().visible:
            dialog.PopupMessage("Notification", "The current layer is hidden, make it visible for edit")
            return
        if self.app.layer_ribbon.get_active_layer().texture_locked:
            dialog.PopupMessage("Notification", "The current layer is locked, make it unlock for edit")
            return

        if self.app.active_tool == TOOL_PENCIL1:
            self.fbo.bind()
            if touch:
                with self.fbo:
                    self.fbo.add(self.app.aColor)
                    d = 1.
                    self.cursor_pos = ((touch.x - d / 2) / self.scale - self.fbo_rect.pos[0],
                                       (touch.y - d / 2) / self.scale - self.fbo_rect.pos[1])
                    Ellipse(pos=self.cursor_pos, size=(d, d))
                    touch.ud['line'] = Line(points=self.cursor_pos, width=d)
            self.fbo.release()
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_PENCIL2:
            self.fbo.bind()
            if touch:
                with self.fbo:
                    self.fbo.add(self.app.aColor)
                    d = 2.1
                    self.cursor_pos = ((touch.x - d / 2) / self.scale - self.fbo_rect.pos[0],
                                       (touch.y - d / 2) / self.scale - self.fbo_rect.pos[1])
                    Ellipse(pos=self.cursor_pos, size=(d, d))
                    touch.ud['line'] = Line(points=self.cursor_pos, width=d / 2.0)
            self.fbo.release()
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_PENCIL3:
            self.fbo.bind()
            if touch:
                with self.fbo:
                    self.fbo.add(self.app.aColor)
                    d = 3.
                    self.cursor_pos = ((touch.x - d / 2) / self.scale - self.fbo_rect.pos[0],
                                       (touch.y - d / 2) / self.scale - self.fbo_rect.pos[1])
                    Ellipse(pos=self.cursor_pos, size=(d, d))
                    touch.ud['line'] = Line(points=self.cursor_pos, width=d / 2)
            self.fbo.release()
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_PICKER:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    c = self.fbo_get_pixel_color(touch)
                    self.app.aColor = Color(c[0], c[1], c[2], c[3])
                    self.app.toolbar.tools_select(self.app.prev_tool)
        elif self.app.active_tool == TOOL_FILL:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_fill_region(touch)
        elif self.app.active_tool == TOOL_ERASE1:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_replace_color(touch, width=1)
        elif self.app.active_tool == TOOL_ERASE2:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_replace_color(touch, width=2)
        elif self.app.active_tool == TOOL_ERASE3:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_replace_color(touch, width=3)
        elif self.app.active_tool == TOOL_SELECT:
            if touch:
                if not self.tool_buffer.enabled:
                    self.tool_select.on_touch_down(touch, self.fbo, self.tool_fbo)
                else:
                    pass
        elif self.app.active_tool == TOOL_LINE:
            if touch:
                self.tool_line.on_touch_down(touch, self.fbo, self.tool_fbo)
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_RECT:
            if touch:
                self.tool_rect.on_touch_down(touch, self.fbo, self.tool_fbo)
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_ELLIPSE:
            if touch:
                self.tool_ellipse.on_touch_down(touch, self.fbo, self.tool_fbo)
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_MOVE:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.move_image = True
                    self.ox, self.oy = touch.pos
        return True

    def on_touch_move(self, touch):
        result = self.touch_responce()
        if result == 2:
            self.scale_canvas(1.02)
            return
        elif result == 1:
            self.scale_canvas(0.98)
            return
        elif result == 3:
            dist = self.touches[0].distance(self.first_touch)
            self.fbo_move_by_offset((dist / self.scale, dist / self.scale))

        if self.app.active_tool == TOOL_PENCIL1:
            self.fbo_render(touch, width=1.)
        elif self.app.active_tool == TOOL_PENCIL2:
            self.fbo_render(touch, width=2.)
        elif self.app.active_tool == TOOL_PENCIL3:
            self.fbo_render(touch, width=3.)
        elif self.app.active_tool == TOOL_PICKER:
            c = self.fbo_get_pixel_color(touch)
            self.app.aColor = Color(c[0], c[1], c[2])
        elif self.app.active_tool == TOOL_ERASE1:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_replace_color(touch, width=1)
        elif self.app.active_tool == TOOL_ERASE2:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_replace_color(touch, width=2)
        elif self.app.active_tool == TOOL_ERASE3:
            if touch:
                if self.collide_point(touch.x, touch.y):
                    self.fbo_replace_color(touch, width=3)
        elif self.app.active_tool == TOOL_SELECT:
            if touch:
                if not self.tool_buffer.enabled:
                    self.tool_select.on_touch_move(touch, self.tool_fbo)
                    self.fbo.draw()
                    self.canvas.ask_update()
                else:
                    pass

        elif self.app.active_tool == TOOL_LINE:
            if touch:
                self.tool_line.on_touch_move(touch, self.tool_fbo)
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_RECT:
            if touch:
                self.tool_rect.on_touch_move(touch, self.tool_fbo)
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_ELLIPSE:
            if touch:
                self.tool_ellipse.on_touch_move(touch, self.tool_fbo)
            self.fbo.draw()
            self.canvas.ask_update()
        elif self.app.active_tool == TOOL_MOVE:
            if self.move_image:
                self.fbo_move_by_offset((touch.dx / self.scale, touch.dy / self.scale))
        self.tool_buffer.on_touch_move(touch, self.fbo)

    def on_touch_up(self, touch):
        self.tool_buffer.on_touch_up(touch)
        if touch.grab_current is not self:
            return False
        if not self.collide_point(*touch.pos):
            return False
        touch.ungrab(self)

        if self.double_touch():
            _not_add_too_undo = True
        else:
            _not_add_too_undo = False

        if touch:
            try:
                self.touches.remove(touch)
            except:
                pass
            if self.app.active_tool == TOOL_SELECT:
                if touch:
                    self.tool_select.on_touch_up(touch)
                self.fbo.draw()
                self.canvas.ask_update()
            elif self.app.active_tool == TOOL_LINE:
                if touch:
                    self.tool_line.on_touch_up(touch)
                self.fbo.draw()
                self.canvas.ask_update()
            elif self.app.active_tool == TOOL_RECT:
                if touch:
                    self.tool_rect.on_touch_up(touch)
                self.fbo.draw()
                self.canvas.ask_update()
            elif self.app.active_tool == TOOL_ELLIPSE:
                if touch:
                    self.tool_ellipse.on_touch_up(touch)
                self.fbo.draw()
                self.canvas.ask_update()
            elif self.app.active_tool == TOOL_MOVE:
                if touch:
                    self.move_image = False
            elif self.app.active_tool == TOOL_ERASE1 or self.app.active_tool == TOOL_ERASE2 or self.app.active_tool == TOOL_ERASE3:
                if touch:
                    self.px = None
                    self.py = None
            if self.app.active_tool == TOOL_PENCIL1 or self.app.active_tool == TOOL_ERASE1 \
                    or self.app.active_tool == TOOL_PENCIL2 or self.app.active_tool == TOOL_ERASE2 \
                    or self.app.active_tool == TOOL_PENCIL3 or self.app.active_tool == TOOL_ERASE3 \
                    or self.app.active_tool == TOOL_FILL:
                rect = self.app.layer_ribbon.get_active_layer().rect
                pos = rect.pos[0] * self.scale, rect.pos[1] * self.scale
                size = rect.size[0] * self.scale, rect.size[1] * self.scale
                if not _not_add_too_undo:
                    if pos[0] <= touch.x <= pos[0] + size[0] and pos[1] <= touch.y <= pos[1] + size[1]:
                        self.add_undo_stack()
        return True

    def add_redo_stack(self):
        pass

    def add_undo_stack(self):
        _active_layer = self.app.layer_ribbon.get_active_layer()
        _active_layer.backup_texture()
        self.layer_undo_stack = self.layer_undo_stack[:self.undo_layer_index + 1]
        self.layer_undo_stack.append(_active_layer)
        self.undo_layer_index = len(self.layer_undo_stack) - 1

    def do_undo(self, *args):
        if self.layer_undo_stack:
            if self.undo_layer_index > 0:
                _layer = self.layer_undo_stack[self.undo_layer_index]
                _layer.texture_from_backup(direction=-1)
                _active_layer = self.app.layer_ribbon.get_active_layer()
                if _layer is _active_layer:
                    self.fbo_create(_active_layer.texture.size, _active_layer.texture)
                self.undo_layer_index -= 1
                self.canvas_put_drawarea()
            self.fbo_update_pos()

    def active_layer_backup_texture(self):
        active_layer = self.app.layer_ribbon.get_active_layer()
        self.active_layer_last_texture = improc.texture_copy(active_layer.texture)

    def active_layer_set_last_backup_texture(self):
        active_layer = self.app.layer_ribbon.get_active_layer()
        # texture = active_layer.textures_array[-1]
        active_layer.replace_texture(self.active_layer_last_texture)

        self.fbo_create(active_layer.texture.size, active_layer.texture)

        self.canvas_put_drawarea()
        self.fbo_update_pos()
        self.canvas.ask_update()

    def do_redo(self, *args):
        if self.layer_undo_stack:
            if self.undo_layer_index < len(self.layer_undo_stack) - 1:
                self.undo_layer_index += 1
                _layer = self.layer_undo_stack[self.undo_layer_index]
                _layer.texture_from_backup(direction=1)
                _active_layer = self.app.layer_ribbon.get_active_layer()
                if _layer is _active_layer:
                    self.fbo_create(_active_layer.texture.size, _active_layer.texture)
                self.canvas_put_drawarea()
            self.fbo_update_pos()
