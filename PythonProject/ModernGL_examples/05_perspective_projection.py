import ModernGL
from ModernGL.ext.examples import run_example
import numpy as np

"""
    Renders a blue triangle
"""


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 330

                in vec3 vert;

                uniform float z_near;
                uniform float z_far;
                uniform float fovy;
                uniform float ratio;

                uniform vec3 center;
                uniform vec3 eye;
                uniform vec3 up;

                mat4 perspective() {
                    float zmul = (-2.0 * z_near * z_far) / (z_far - z_near);
                    float ymul = 1.0 / tan(fovy * 3.14159265 / 360);
                    float xmul = ymul / ratio;

                    return mat4(
                        xmul, 0.0, 0.0, 0.0,
                        0.0, ymul, 0.0, 0.0,
                        0.0, 0.0, -1.0, -1.0,
                        0.0, 0.0, zmul, 0.0
                    );
                }

                mat4 lookat() {
                    vec3 forward = normalize(center - eye);
                    vec3 side = normalize(cross(forward, up));
                    vec3 upward = cross(side, forward);

                    return mat4(
                        side.x, upward.x, -forward.x, 0,
                        side.y, upward.y, -forward.y, 0,
                        side.z, upward.z, -forward.z, 0,
                        -dot(eye, side), -dot(eye, upward), dot(eye, forward), 1
                    );
                }

                void main() {
                    gl_Position = perspective() * lookat() * vec4(vert, 1.0);
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                out vec4 color;

                void main() {
                    color = vec4(0.04, 0.04, 0.04, 1.0);

                }
            '''),
        ])

        width, height = self.wnd.size
        self.prog.uniforms['z_near'].value = 0.1
        self.prog.uniforms['z_far'].value = 1000.0
        self.prog.uniforms['ratio'].value = width / height
        self.prog.uniforms['fovy'].value = 60

        self.prog.uniforms['eye'].value = (3, 3, 3)
        self.prog.uniforms['center'].value = (0, 0, 0)
        self.prog.uniforms['up'].value = (0, 0, 1)

        grid = []

        for i in range(65):
            grid.append([i - 32, -32.0, 0.0, i - 32, 32.0, 0.0])
            grid.append([-32.0, i - 32, 0.0, 32.0, i - 32, 0.0])

        grid = np.array(grid)

        self.vbo = self.ctx.buffer(grid.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['vert'])

    def render(self):
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render(ModernGL.LINES, 65 * 4)


run_example(Example)
