import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_compute_shader(self):
        if self.ctx.version_code < 430:
            self.skipTest('OpenGL 4.3 is not supported')

        src = '''
            #version 430
            layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
            void main() {
            }
        '''

        compute_shader = self.ctx.compute_shader(src)
        self.assertEqual(compute_shader.source, src)


if __name__ == '__main__':
    unittest.main()
