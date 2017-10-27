import struct
import unittest

import ModernGL

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

        if cls.ctx.vendor.startswith('Intel'):
            raise unittest.SkipTest('')

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_dvec2(self):
        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 410

                in dvec2 in_a[2];
                out dvec2 out_a[2];

                void main() {
                    out_a[0] = in_a[0];
                    out_a[1] = in_a[1];
                }
            '''),
        ], ['out_a'])

        self.vbo1 = self.ctx.buffer(struct.pack('2d2d', 1.0, 1.0, 1.0, 1.0))
        self.vbo2 = self.ctx.buffer(struct.pack('2d2d', 0.0, 0.0, 0.0, 0.0))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo1, ['in_a'])
        self.vao.transform(self.vbo2, ModernGL.POINTS, 1)
        x1, y1, x2, y2 = struct.unpack('2d2d', self.vbo2.read())
        self.assertAlmostEqual(x1, 1.0)
        self.assertAlmostEqual(y1, 1.0)
        self.assertAlmostEqual(x2, 1.0)
        self.assertAlmostEqual(y2, 1.0)

    def test_dvec3(self):
        self.prog = self.ctx.program([
            self.ctx.vertex_shader('''
                #version 410

                in dvec3 in_a[2];
                out dvec3 out_a[2];

                void main() {
                    out_a[0] = in_a[0];
                    out_a[1] = in_a[1];
                }
            '''),
        ], ['out_a'])

        self.vbo1 = self.ctx.buffer(struct.pack('3d3d', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0))
        self.vbo2 = self.ctx.buffer(struct.pack('3d3d', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo1, ['in_a'])
        self.vao.transform(self.vbo2, ModernGL.POINTS, 1)
        x1, y1, z1, x2, y2, z2 = struct.unpack('3d3d', self.vbo2.read())
        self.assertAlmostEqual(x1, 1.0)
        self.assertAlmostEqual(y1, 1.0)
        self.assertAlmostEqual(z1, 1.0)
        self.assertAlmostEqual(x2, 1.0)
        self.assertAlmostEqual(y2, 1.0)
        self.assertAlmostEqual(z2, 1.0)


if __name__ == '__main__':
    unittest.main()
