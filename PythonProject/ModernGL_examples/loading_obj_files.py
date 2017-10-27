import os

import ModernGL
from ModernGL.ext.examples import run_example
from ModernGL.ext.obj import Obj
from PIL import Image
from pyrr import Matrix44


class Example:
    def __init__(self, wnd):
        self.wnd = wnd
        self.ctx = ModernGL.create_context()

        self.obj = Obj.open(os.path.join(os.path.dirname(__file__), 'data', 'sitting_dummy.obj'))
        self.wood = Image.open(os.path.join(os.path.dirname(__file__), 'data', 'wood.jpg'))

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
                    v_vert = in_vert;
                    v_norm = in_norm;
                    v_text = in_text;
                    gl_Position = Mvp * vec4(v_vert, 1.0);
                }
            '''),
            self.ctx.fragment_shader('''
                #version 330

                uniform sampler2D Texture;
                uniform vec4 Color;
                uniform vec3 Light;

                in vec3 v_vert;
                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {
                    float lum = dot(normalize(v_norm), normalize(v_vert - Light));
                    lum = acos(lum) / 3.14159265;
                    lum = clamp(lum, 0.0, 1.0);
                    lum = lum * lum;
                    lum = smoothstep(0.0, 1.0, lum);
                    lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;
                    lum = lum * 0.8 + 0.2;

                    vec3 color = texture(Texture, v_text).rgb;
                    color = color * (1.0 - Color.a) + Color.rgb * Color.a;
                    f_color = vec4(color * lum, 1.0);
                }

            '''),
        ])

        self.light = self.prog.uniforms['Light']
        self.color = self.prog.uniforms['Color']
        self.mvp = self.prog.uniforms['Mvp']

        self.texture = self.ctx.texture(self.wood.size, 3, self.wood.tobytes())
        self.texture.build_mipmaps()

        self.vbo = self.ctx.buffer(self.obj.pack('vx vy vz nx ny nz tx ty'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, ['in_vert', 'in_norm', 'in_text'])

    def render(self):
        width, height = self.wnd.size
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(ModernGL.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, width / height, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (-85, -180, 140),
            (0.0, 0.0, 65.0),
            (0.0, 0.0, 1.0),
        )

        self.light.value = (-140.0, -300.0, 350.0)
        self.color.value = (1.0, 1.0, 1.0, 0.25)
        self.mvp.write((proj * lookat).astype('f4').tobytes())

        self.texture.use()
        self.vao.render()


run_example(Example)
