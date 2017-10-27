import os

import ModernGL
import numpy as np
from ModernGL.ext.examples import run_example
from ModernGL.ext.obj import Obj
from PIL import Image
from pyrr import Matrix44


def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_vert;
                in vec3 in_norm;
                in vec2 in_text;

                out vec3 v_vert;
                out vec3 v_norm;
                out vec2 v_text;

                void main() {
                    gl_Position = Mvp * vec4(in_vert, 1.0);
                    v_vert = in_vert;
                    v_norm = in_norm;
                    v_text = in_text;
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                uniform vec3 Light;
                uniform vec3 Color;
                uniform bool UseTexture;
                uniform sampler2D Texture;

                in vec3 v_vert;
                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {
                    float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
                    if (UseTexture) {
                        f_color = vec4(texture(Texture, v_text).rgb * lum, 1.0);
                    } else {
                        f_color = vec4(Color * lum, 1.0);
                    }
                }
            '''),
        ])

        self.mvp = self.prog.uniforms['Mvp']
        self.light = self.prog.uniforms['Light']
        self.color = self.prog.uniforms['Color']
        self.use_texture = self.prog.uniforms['UseTexture']

        self.objects = {}

        for name in ['ground', 'grass', 'billboard', 'billboard-holder', 'billboard-image']:
            obj = Obj.open(local('data', 'scene-1-%s.obj' % name))
            vbo = self.ctx.buffer(obj.pack('vx vy vz nx ny nz tx ty'))
            vao = self.ctx.simple_vertex_array(self.prog, vbo, ['in_vert', 'in_norm', 'in_text'])
            self.objects[name] = vao

        img = Image.open(local('data', 'infographic-1.jpg')).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
        self.texture1 = self.ctx.texture(img.size, 3, img.tobytes())
        self.texture1.build_mipmaps()

        self.texture2 = self.ctx.texture(self.wnd.size, 3)
        depth_attachment = self.ctx.depth_renderbuffer(self.wnd.size)
        self.fbo = self.ctx.framebuffer(self.texture2, depth_attachment)

    def render(self):
        width, height = self.wnd.size
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(ModernGL.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, width / height, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (47.697, -8.147, 24.498),
            (0.0, 0.0, 8.0),
            (0.0, 0.0, 1.0),
        )

        rotate = Matrix44.from_z_rotation(np.sin(self.wnd.time) * 0.5 + 0.2)

        for mode in ['render_to_texture', 'render_to_window']:
            if mode == 'render_to_texture':
                self.fbo.clear(1.0, 1.0, 1.0)
                self.fbo.use()

            else:
                self.ctx.default_framebuffer.use()

            self.use_texture.value = False

            self.light.value = (67.69, -8.14, 52.49)
            self.mvp.write((proj * lookat * rotate).astype('f4').tobytes())

            self.color.value = (0.67, 0.49, 0.29)
            self.objects['ground'].render()

            self.color.value = (0.46, 0.67, 0.29)
            self.objects['grass'].render()

            self.color.value = (1.0, 1.0, 1.0)
            self.objects['billboard'].render()

            self.color.value = (0.2, 0.2, 0.2)
            self.objects['billboard-holder'].render()

            self.use_texture.value = True

            if mode == 'render_to_texture':
                self.texture1.use()

            else:
                self.texture2.use()

            self.objects['billboard-image'].render()


run_example(Example, backend='PyQt5')
