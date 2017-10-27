import os

import ModernGL
import numpy as np
from ModernGL.ext.obj import Obj
from ModernGL.ext.examples import run_example
from PIL import Image
from pyrr import Matrix44


def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)


class InstancedCrates:
    '''
        This example renders 32x32 crates.
        For each crate the location is [x, y, sin(a * time + b)]
        There are 1024 crates aligned in a grid.
    '''

    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_move;

                in vec3 in_vert;
                in vec3 in_norm;
                in vec2 in_text;

                out vec3 v_vert;
                out vec3 v_norm;
                out vec2 v_text;

                void main() {
                    gl_Position = Mvp * vec4(in_vert + in_move, 1.0);
                    v_vert = in_vert + in_move;
                    v_norm = in_norm;
                    v_text = in_text;
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                uniform vec3 Light;
                uniform sampler2D Texture;

                in vec3 v_vert;
                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {
                    float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
                    f_color = vec4(texture(Texture, v_text).rgb * lum, 1.0);
                }
            '''),
        ])

        self.mvp = self.prog.uniforms['Mvp']
        self.light = self.prog.uniforms['Light']

        obj = Obj.open(local('data', 'crate.obj'))
        img = Image.open(local('data', 'crate.png')).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
        self.texture = self.ctx.texture(img.size, 3, img.tobytes())
        self.texture.build_mipmaps()
        self.texture.use()

        self.vbo1 = self.ctx.buffer(obj.pack('vx vy vz nx ny nz tx ty'))
        self.vbo2 = self.ctx.buffer(reserve=12 * 1024)
        self.vao = self.ctx.vertex_array(self.prog, [
            (self.vbo1, '3f3f2f', ['in_vert', 'in_norm', 'in_text']),
            (self.vbo2, '3f/i', ['in_move']),
        ])

        self.crate_a = np.random.uniform(0.7, 0.8, 32 * 32)
        self.crate_b = np.random.uniform(0.0, 6.3, 32 * 32)
        self.crate_x = (np.tile(np.arange(32), 32) - 16) * 1.5
        self.crate_y = (np.repeat(np.arange(32), 32) - 16) * 1.5
        self.crate_x += np.random.uniform(-0.2, 0.2, 32 * 32)
        self.crate_y += np.random.uniform(-0.2, 0.2, 32 * 32)

    def render(self):
        angle = self.wnd.time * 0.2
        width, height = self.wnd.size
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(ModernGL.DEPTH_TEST)

        camera_pos = (np.cos(angle) * 5.0, np.sin(angle) * 5.0, 2.0)

        proj = Matrix44.perspective_projection(45.0, width / height, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            camera_pos,
            (0.0, 0.0, 0.5),
            (0.0, 0.0, 1.0),
        )

        self.mvp.write((proj * lookat).astype('f4').tobytes())
        self.light.value = camera_pos

        crate_z = np.sin(self.crate_a * self.wnd.time + self.crate_b) * 0.2
        coordinates = np.dstack([self.crate_x, self.crate_y, crate_z])

        self.vbo2.write(coordinates.astype('f4').tobytes())
        self.vao.render(instances=1024)


run_example(InstancedCrates)
