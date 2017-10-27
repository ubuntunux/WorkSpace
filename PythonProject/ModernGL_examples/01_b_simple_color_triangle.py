import ModernGL
from ModernGL.ext.examples import run_example
import numpy as np

"""
    Renders a traingle that has all RGB combinations
"""


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                      #version 330

                      in vec2 in_vert;

                      in vec3 in_color;
                      out vec3 v_color;    // Goes to the fragment shader

                      void main() {
                          gl_Position = vec4(in_vert, 0.0, 1.0);
                          v_color = in_color;
                      }
                  '''),
            self.ctx.fragment_shader('''
                      #version 330

                      in vec3 v_color;
                      out vec4 f_color;

                      void main() {
                          // We're not interested in changing the alpha value
                          f_color = vec4(v_color, 1.0);
                      }
                  '''),
        ])

        # Point coordinates are put followed by the vec3 color values
        vertices = np.array([
            # x, y, red, green, blue
            0.0, 0.8, 1.0, 0.0, 0.0,
            -0.6, -0.8, 0.0, 1.0, 0.0,
            0.6, -0.8, 0.0, 0.0, 1.0,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())

        # We control the 'in_vert' and `in_color' variables
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_vert', 'in_color'])

    def render(self):
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render()


run_example(Example)
