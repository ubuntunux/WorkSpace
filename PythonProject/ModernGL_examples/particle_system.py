import ModernGL
from ModernGL.ext.examples import run_example
import numpy as np


def particle():
    a = np.random.uniform(0.0, np.pi * 2.0)
    r = np.random.uniform(0.0, 0.001)
    return np.array([0.0, 0.0, np.cos(a) * r - 0.003, np.sin(a) * r - 0.008]).astype('f4').tobytes()


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                in vec2 in_vert;

                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                out vec4 f_color;

                void main() {
                    f_color = vec4(0.30, 0.50, 1.00, 1.0);
                }
            '''),
        ])

        self.tvert = self.ctx.vertex_shader('''
            #version 330

            uniform vec2 Acc;

            in vec2 in_pos;
            in vec2 in_prev;

            out vec2 out_pos;
            out vec2 out_prev;

            void main() {
                out_pos = in_pos * 2.0 - in_prev + Acc;
                out_prev = in_pos;
            }
        ''')

        self.transform = self.ctx.program(self.tvert, ['out_pos', 'out_prev'])
        self.acc = self.transform.uniforms['Acc']
        self.acc.value = (0.0, -0.0001)

        self.vbo1 = self.ctx.buffer(b''.join(particle() for i in range(1024)))
        self.vbo2 = self.ctx.buffer(reserve=self.vbo1.size)

        self.vao1 = self.ctx.simple_vertex_array(self.transform, self.vbo1, ['in_pos', 'in_prev'])
        self.vao2 = self.ctx.simple_vertex_array(self.transform, self.vbo2, ['in_pos', 'in_prev'])

        self.render_vao = self.ctx.vertex_array(self.prog, [
            (self.vbo1, '2f8x', ['in_vert']),
        ])

        self.idx = 0

    def render(self):
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.point_size = 2.0

        for i in range(8):
            self.vbo1.write(particle(), offset=self.idx * 16)
            self.idx = (self.idx + 1) % 1024

        self.render_vao.render(ModernGL.POINTS, 1024)
        self.vao1.transform(self.vbo2, ModernGL.POINTS, 1024)
        self.ctx.copy_buffer(self.vbo1, self.vbo2)


run_example(Example)
