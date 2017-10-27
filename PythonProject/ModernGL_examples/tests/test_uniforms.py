import struct
import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()
        cls.vbo = cls.ctx.buffer(reserve=1024)
        cls.res = cls.ctx.buffer(reserve=1024)
        cls.vbo.clear()

        cls.shader = '''
            #version %(version)s
            uniform %(type)s Uniform;
            in %(type)s v_in;
            out %(type)s v_out;
            void main() {
                v_out = Uniform * v_in;
            }
        '''

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_float_uniform(self):
        vertex_shader = self.ctx.vertex_shader('''
            #version 330
            uniform float Uniform;
            in float v_in;
            out float v_out;
            void main() {
                v_out = Uniform * v_in;
            }
        ''')

        prog = self.ctx.program(vertex_shader, ['v_out'])
        vbo = self.ctx.buffer(struct.pack('f', 1.0))
        vao = self.ctx.simple_vertex_array(prog, vbo, ['v_in'])

        prog.uniforms['Uniform'].value = 7.0
        vao.transform(self.res)

        val = struct.unpack('f', self.res.read(4))[0]
        self.assertAlmostEqual(val, 7.0)

    def test_int_uniform(self):
        vertex_shader = self.ctx.vertex_shader('''
            #version 330
            uniform int Uniform;
            in int v_in;
            out int v_out;
            void main() {
                v_out = Uniform * v_in;
            }
        ''')

        prog = self.ctx.program(vertex_shader, ['v_out'])
        vbo = self.ctx.buffer(struct.pack('i', 1))
        vao = self.ctx.simple_vertex_array(prog, vbo, ['v_in'])

        prog.uniforms['Uniform'].value = -2
        vao.transform(self.res)

        val = struct.unpack('i', self.res.read(4))[0]
        self.assertAlmostEqual(val, -2)

    def test_vec_uniform(self):
        vertex_shader = self.ctx.vertex_shader('''
            #version 330
            uniform vec3 Uniform;
            in vec3 v_in;
            out vec3 v_out;
            void main() {
                v_out = Uniform * v_in;
            }
        ''')

        prog = self.ctx.program(vertex_shader, ['v_out'])
        vbo = self.ctx.buffer(struct.pack('3f', 1.0, 1.0, 1.0))
        vao = self.ctx.simple_vertex_array(prog, vbo, ['v_in'])

        prog.uniforms['Uniform'].value = (0.5, 1.0, 1.5)
        vao.transform(self.res)

        x, y, z = struct.unpack('3f', self.res.read(12))
        self.assertAlmostEqual(x, 0.5)
        self.assertAlmostEqual(y, 1.0)
        self.assertAlmostEqual(z, 1.5)

    def test_mat_uniform(self):
        vertex_shader = self.ctx.vertex_shader('''
            #version 330
            uniform mat2x3 Uniform;
            in float v_in;
            out mat2x3 v_out;
            void main() {
                v_out = Uniform * v_in;
            }
        ''')

        prog = self.ctx.program(vertex_shader, ['v_out'])
        vbo = self.ctx.buffer(struct.pack('f', 1.0))
        vao = self.ctx.simple_vertex_array(prog, vbo, ['v_in'])

        prog.uniforms['Uniform'].value = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0)
        vao.transform(self.res)

        m = struct.unpack('6f', self.res.read(24))
        self.assertAlmostEqual(m[0], 0.0)
        self.assertAlmostEqual(m[1], 1.0)
        self.assertAlmostEqual(m[2], 2.0)
        self.assertAlmostEqual(m[3], 3.0)
        self.assertAlmostEqual(m[4], 4.0)
        self.assertAlmostEqual(m[5], 5.0)


if __name__ == '__main__':
    unittest.main()
