import unittest

import ModernGL

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

        cls.vertex_shader = cls.ctx.vertex_shader('''
            #version 330
            uniform mat4 Mvp;
            in vec4 vertex;
            uniform Block {
                mat4 Transform;
            };
            void main() {
                gl_Position = Mvp * Transform * vertex;
            }
        ''')

        cls.geometry_shader = cls.ctx.geometry_shader('''
            #version 330
            layout(points) in;
            uniform vec4 Position;
            layout(line_strip, max_vertices = 2) out;
            out vec4 color;
            void main() {
                gl_Position = gl_in[0].gl_Position + Position;
                EmitVertex();
                gl_Position = gl_in[0].gl_Position - Position;
                EmitVertex();
                EndPrimitive();
            }
        ''')

        cls.fragment_shader = cls.ctx.fragment_shader('''
            #version 330
            uniform vec4 Color;
            uniform Lights {
                uniform vec4 Light[1];
            };
            out vec4 color;
            void main() {
                color = Color * Light[0];
            }
        ''')

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_program_uniforms_1(self):
        program = self.ctx.program(self.vertex_shader)

        self.assertIn('Mvp', program.uniforms)
        self.assertNotIn('Block', program.uniforms)
        self.assertNotIn('Transform', program.uniforms)

    def test_program_uniforms_2(self):
        program = self.ctx.program([self.vertex_shader, self.geometry_shader, self.fragment_shader])

        self.assertIn('Mvp', program.uniforms)
        self.assertIn('Position', program.uniforms)
        self.assertIn('Color', program.uniforms)

    def test_program_uniform_blocks(self):
        program = self.ctx.program([self.vertex_shader, self.fragment_shader])

        self.assertIn('Block', program.uniform_blocks)
        self.assertIn('Lights', program.uniform_blocks)
        self.assertNotIn('Transform', program.uniform_blocks)
        self.assertNotIn('Light', program.uniform_blocks)
        self.assertNotIn('Block', program.uniforms)
        self.assertNotIn('Lights', program.uniforms)

    def test_program_geometry_primitives_1(self):
        program = self.ctx.program(self.vertex_shader)

        self.assertIsNone(program.geometry_input)
        self.assertIsNone(program.geometry_output)
        self.assertEqual(program.geometry_vertices, 0)

    def test_program_geometry_primitives_2(self):
        program = self.ctx.program([self.vertex_shader, self.geometry_shader])

        self.assertIsInstance(program.geometry_input, ModernGL.Primitive)
        self.assertIsInstance(program.geometry_output, ModernGL.Primitive)
        self.assertEqual(program.geometry_vertices, 2)

    def test_program_duplicate_shader_1(self):
        with self.assertRaisesRegex(ModernGL.Error, 'duplicate'):
            self.ctx.program([self.vertex_shader, self.vertex_shader])

    def test_program_duplicate_shader_2(self):
        with self.assertRaisesRegex(ModernGL.Error, 'duplicate'):
            self.ctx.program([self.vertex_shader, self.fragment_shader, self.fragment_shader])


if __name__ == '__main__':
    unittest.main()
