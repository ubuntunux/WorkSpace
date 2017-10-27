import struct
import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_1(self):
        if self.ctx.version_code < 400:
            self.skipTest('OpenGL 4.0 is not supported')

        vbo1 = self.ctx.buffer(struct.pack('4f', 0.0, 0.0, 0.0, 0.0))
        vbo2 = self.ctx.buffer(struct.pack('4f', 0.0, 0.0, 0.0, 0.0))

        vert = self.ctx.vertex_shader('''
            #version 400

            in vec4 vert;
            out vec4 color;

            subroutine vec4 color_t();

            subroutine(color_t)
            vec4 ColorRed() {
                return vec4(1, 0, 0, 1);
            }

            subroutine(color_t)
            vec4 ColorBlue() {
                return vec4(0, 0.5, 1, 1);
            }

            subroutine(color_t)
            vec4 ColorYellow() {
                return vec4(1, 1, 0, 1);
            }

            subroutine uniform color_t Color;

            void main() {
                color = vert + Color();
            }
        ''')

        prog = self.ctx.program(vert, ['color'])
        vao = self.ctx.simple_vertex_array(prog, vbo1, ['vert'])

        vao.subroutines = (prog.vertex_shader.subroutines['ColorRed'],)
        vao.transform(vbo2)

        x, y, z, w = struct.unpack('4f', vbo2.read())
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 0.0)
        self.assertAlmostEqual(z, 0.0)
        self.assertAlmostEqual(w, 1.0)

        vao.subroutines = [prog.vertex_shader.subroutines['ColorBlue']]
        vao.transform(vbo2)

        x, y, z, w = struct.unpack('4f', vbo2.read())
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.5)
        self.assertAlmostEqual(z, 1.0)
        self.assertAlmostEqual(w, 1.0)

        vao.subroutines = [prog.vertex_shader.subroutines['ColorYellow'].index]
        vao.transform(vbo2)

        x, y, z, w = struct.unpack('4f', vbo2.read())
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 1.0)
        self.assertAlmostEqual(z, 0.0)
        self.assertAlmostEqual(w, 1.0)


if __name__ == '__main__':
    unittest.main()
