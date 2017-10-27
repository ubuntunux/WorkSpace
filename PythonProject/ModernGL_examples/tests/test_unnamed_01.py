import struct
import unittest

import ModernGL

from common import get_context


class TestBuffer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

        cls.vert = cls.ctx.vertex_shader('''
            #version 330

            in mat2 in_m;
            in vec2 in_v;

            out vec2 out_v;

            uniform float mult;

            void main() {
                out_v = in_m * in_v * mult;
            }
        ''')

        cls.prog = cls.ctx.program(cls.vert, ['out_v'])

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_1(self):
        buf_m = self.ctx.buffer(struct.pack('4f', 1, 1, 1, 2))
        buf_v = self.ctx.buffer(struct.pack('2f', 4, 7))
        res = self.ctx.buffer(reserve=buf_v.size)

        vao = self.ctx.vertex_array(self.prog, [
            (buf_m, '4f', ['in_m']),
            (buf_v, '2f', ['in_v']),
        ])

        self.prog.uniforms['mult'].value = 0.0
        vao.transform(res, ModernGL.POINTS)
        x, y = struct.unpack('2f', res.read())
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.0)

        self.prog.uniforms['mult'].value = 1.0
        vao.transform(res, ModernGL.POINTS)
        x, y = struct.unpack('2f', res.read())
        self.assertAlmostEqual(x, 11.0)
        self.assertAlmostEqual(y, 18.0)

        self.prog.uniforms['mult'].value = 2.0
        vao.transform(res, ModernGL.POINTS)
        x, y = struct.unpack('2f', res.read())
        self.assertAlmostEqual(x, 22.0)
        self.assertAlmostEqual(y, 36.0)


if __name__ == '__main__':
    unittest.main()
