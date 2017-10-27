import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_transform(self):

        vertex_shader = self.ctx.vertex_shader('''
            #version 330

            in vec4 vert;
            out float vert_length;

            void main() {
                vert_length = length(vert);
            }
        ''')

        program = self.ctx.program(vertex_shader, ['vert_length'])

        self.assertIsNot(program.vertex_shader, None)
        self.assertIs(program.fragment_shader, None)
        self.assertIs(program.geometry_shader, None)
        self.assertIs(program.tess_evaluation_shader, None)
        self.assertIs(program.tess_control_shader, None)

        self.assertIs(program.geometry_input, None)
        self.assertIs(program.geometry_output, None)

        self.assertEqual(len(program.uniforms), 0)
        self.assertEqual(len(program.attributes), 1)

        self.assertEqual(len(program.varyings), 1)
        self.assertEqual(len(program.uniform_blocks), 0)

        self.assertTrue('vert' in program.attributes)
        self.assertTrue('vert' not in program.varyings)

        self.assertTrue('vert_length' not in program.attributes)
        self.assertTrue('vert_length' in program.varyings)


if __name__ == '__main__':
    unittest.main()
