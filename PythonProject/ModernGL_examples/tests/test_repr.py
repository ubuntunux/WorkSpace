import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_buffer_repr(self):
        buf = self.ctx.buffer(reserve=1024)
        self.assertRegex(repr(buf), r'<Buffer: \d+>')

    def test_compute_shader_repr(self):
        if self.ctx.version_code < 430:
            self.skipTest('OpenGL 4.3 is not supported')

        compute_shader = self.ctx.compute_shader('''
            #version 430
            layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
            void main() {
            }
        ''')

        self.assertRegex(repr(compute_shader), r'<ComputeShader: \d+>')

    def test_renderbuffer_and_framebuffer_repr(self):
        rbo = self.ctx.renderbuffer((16, 16))
        self.assertRegex(repr(rbo), r'<Renderbuffer: \d+>')

        with self.subTest(rbo=rbo):
            fbo = self.ctx.framebuffer(rbo)
            self.assertRegex(repr(fbo), r'<Framebuffer: \d+>')

    def test_shader_and_program_repr(self):
        vertex_shader = self.ctx.vertex_shader('''
            #version 330
            in vec4 vertex;
            void main() {
                gl_Position = vertex;
            }
        ''')

        self.assertRegex(repr(vertex_shader), r'<Shader: \d+>')

        with self.subTest(vertex_shader=vertex_shader):
            prog = self.ctx.program(vertex_shader)
            self.assertRegex(repr(prog), r'<Program: \d+>')

    def test_texture_repr(self):
        texture = self.ctx.texture((4, 4), 3)
        self.assertRegex(repr(texture), r'<Texture: \d+>')


if __name__ == '__main__':
    unittest.main()
