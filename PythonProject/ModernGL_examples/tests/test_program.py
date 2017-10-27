import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_program(self):

        vertex_shader = self.ctx.vertex_shader('''
            #version 330

            uniform vec2 pos;
            uniform float scale;

            in vec2 vert;
            out vec2 v_vert;

            void main() {
                gl_Position = vec4(pos + vert * scale, 0.0, 1.0);
                v_vert = vert;
            }
        ''')

        fragment_shader = self.ctx.fragment_shader('''
            #version 330

            in vec2 v_vert;
            out vec4 color;

            void main() {
                color = vec4(v_vert, 0.0, 1.0);
            }
        ''')

        program = self.ctx.program([vertex_shader, fragment_shader])

        self.assertIsNot(program.vertex_shader, None)
        self.assertIsNot(program.fragment_shader, None)
        self.assertIs(program.geometry_shader, None)
        self.assertIs(program.tess_evaluation_shader, None)
        self.assertIs(program.tess_control_shader, None)

        self.assertIs(program.geometry_input, None)
        self.assertIs(program.geometry_output, None)

        self.assertEqual(len(program.uniforms), 2)
        self.assertEqual(len(program.attributes), 1)

        self.assertEqual(len(program.varyings), 0)
        self.assertEqual(len(program.uniform_blocks), 0)

        self.assertTrue('pos' in program.uniforms)
        self.assertTrue('scale' in program.uniforms)
        self.assertTrue('vert' not in program.uniforms)

        self.assertTrue('vert' in program.attributes)
        self.assertTrue('pos' not in program.attributes)


if __name__ == '__main__':
    unittest.main()
