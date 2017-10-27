import ModernGL
import numpy as np
from ModernGL.ext.examples import run_example


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                    #version 330

                    in vec2 vert;

                    in vec4 vert_color;
                    out vec4 frag_color;

                    uniform vec2 scale;
                    uniform float rotation;

                    void main() {
                        frag_color = vert_color;
                        float r = rotation * (0.5 + gl_InstanceID * 0.05);
                        mat2 rot = mat2(cos(r), sin(r), -sin(r), cos(r));
                        gl_Position = vec4((rot * vert) * scale, 0.0, 1.0);
                    }
                '''),
            self.ctx.fragment_shader('''
                    #version 330
                    in vec4 frag_color;
                    out vec4 color;
                    void main() {
                        color = vec4(frag_color);
                    }
                '''),
        ])

        self.scale = self.prog.uniforms['scale']
        self.rotation = self.prog.uniforms['rotation']

        width, height = self.wnd.size
        self.scale.value = (height / width * 0.75, 0.75)

        vertices = np.array([
            1.0, 0.0,
            1.0, 0.0, 0.0, 0.5,

            -0.5, 0.86,
            0.0, 1.0, 0.0, 0.5,

            -0.5, -0.86,
            0.0, 0.0, 1.0, 0.5,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['vert', 'vert_color'])

    def render(self):
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(ModernGL.BLEND)
        self.rotation.value = self.wnd.time
        self.vao.render(instances=10)


run_example(Example)
