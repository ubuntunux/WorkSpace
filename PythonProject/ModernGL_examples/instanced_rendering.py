import ModernGL
from ModernGL.ext.examples import run_example
import numpy as np


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                in vec2 in_vert;
                in vec4 in_color;

                out vec4 v_color;

                uniform float Rotation;
                uniform vec2 Scale;

                void main() {
                    v_color = in_color;
                    float r = Rotation * (0.5 + gl_InstanceID * 0.05);
                    mat2 rot = mat2(cos(r), sin(r), -sin(r), cos(r));
                    gl_Position = vec4((rot * in_vert) * Scale, 0.0, 1.0);
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                in vec4 v_color;
                out vec4 f_color;

                void main() {
                    f_color = v_color;
                }
            '''),
        ])

        self.scale = self.prog.uniforms['Scale']
        self.rotation = self.prog.uniforms['Rotation']

        vertices = np.array([
            # x, y, red, green, blue, alpha
            1.0, 0.0, 1.0, 0.0, 0.0, 0.5,
            -0.5, 0.86, 0.0, 1.0, 0.0, 0.5,
            -0.5, -0.86, 0.0, 0.0, 1.0, 0.5,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_vert', 'in_color'])

    def render(self):
        width, height = self.wnd.size
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(ModernGL.BLEND)
        self.scale.value = (height / width * 0.75, 0.75)
        self.rotation.value = self.wnd.time
        self.vao.render(instances=10)


run_example(Example)
