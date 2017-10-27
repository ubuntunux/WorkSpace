import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_vertex_shader(self):
        self.ctx.vertex_shader('''
            #version 330

            void main() {
                gl_Position = vec4(0, 0, 0, 0);
            }
        ''')

    def test_fragment_shader(self):
        self.ctx.fragment_shader('''
            #version 330

            out vec4 color;

            void main() {
                color = vec4(0, 0, 0, 0);
            }
        ''')


if __name__ == '__main__':
    unittest.main()
