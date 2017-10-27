import struct
import unittest

import ModernGL

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

        prog = cls.ctx.program([
            cls.ctx.vertex_shader('''
                #version 330
                in vec2 vert;
                out vec2 text;
                void main() {
                    gl_Position = vec4(vert * 2.0 - 1.0, 0.0, 1.0);
                    text = vert;
                }
            '''),
            cls.ctx.fragment_shader('''
                #version 330
                uniform sampler2D Texture;
                in vec2 text;
                out vec4 color;
                void main() {
                    color = texture(Texture, text);
                }
            '''),
        ])

        vbo = cls.ctx.buffer(struct.pack('8f', 0, 0, 0, 1, 1, 0, 1, 1))
        cls.vao = cls.ctx.simple_vertex_array(prog, vbo, ['vert'])

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_1(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((16, 16)))
        pixels = struct.pack('16B', 255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 0, 0, 0, 255)
        texture = self.ctx.texture((2, 2), 4, pixels)

        fbo.use()
        texture.use()

        texture.filter = ModernGL.LINEAR
        self.vao.render(ModernGL.TRIANGLE_STRIP)

        r, g, b = struct.unpack('3B', fbo.read((8, 8, 1, 1)))
        self.assertTrue(abs(r - 49) < 8 and abs(g - 63) < 8 and abs(b - 63) < 8)

        texture.filter = ModernGL.NEAREST
        self.vao.render(ModernGL.TRIANGLE_STRIP)

        r, g, b = struct.unpack('3B', fbo.read((6, 6, 1, 1)))
        self.assertTrue(abs(r - 255) < 8 and abs(g - 0) < 8 and abs(b - 0) < 8)

        r, g, b = struct.unpack('3B', fbo.read((9, 6, 1, 1)))
        self.assertTrue(abs(r - 0) < 8 and abs(g - 255) < 8 and abs(b - 0) < 8)

        r, g, b = struct.unpack('3B', fbo.read((6, 9, 1, 1)))
        self.assertTrue(abs(r - 0) < 8 and abs(g - 0) < 8 and abs(b - 255) < 8)

        r, g, b = struct.unpack('3B', fbo.read((9, 9, 1, 1)))
        self.assertTrue(abs(r - 0) < 8 and abs(g - 0) < 8 and abs(b - 0) < 8)

    def test_2(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((16, 16)))
        pixels1 = struct.pack('16B', 255, 0, 0, 255, 0, 255, 0, 255, 255, 0, 0, 255, 0, 255, 0, 255)
        pixels2 = struct.pack('16B', 20, 30, 40, 255, 80, 70, 60, 255, 20, 30, 40, 255, 80, 70, 60, 255)
        texture = self.ctx.texture((2, 2), 4, pixels1)

        fbo.use()
        texture.use()

        texture.filter = ModernGL.NEAREST
        self.vao.render(ModernGL.TRIANGLE_STRIP)

        r, g, b = struct.unpack('3B', fbo.read((5, 7, 1, 1)))
        self.assertTrue(abs(r - 255) < 8 and abs(g - 0) < 8 and abs(b - 0) < 8)

        r, g, b = struct.unpack('3B', fbo.read((10, 7, 1, 1)))
        self.assertTrue(abs(r - 0) < 8 and abs(g - 255) < 8 and abs(b - 0) < 8)

        texture.write(pixels2)

        texture.filter = ModernGL.NEAREST
        self.vao.render(ModernGL.TRIANGLE_STRIP)

        r, g, b = struct.unpack('3B', fbo.read((5, 7, 1, 1)))
        self.assertTrue(abs(r - 20) < 8 and abs(g - 30) < 8 and abs(b - 40) < 8)

        r, g, b = struct.unpack('3B', fbo.read((10, 7, 1, 1)))
        self.assertTrue(abs(r - 80) < 8 and abs(g - 70) < 8 and abs(b - 60) < 8)

    def test_3(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((16, 16)))
        pixels1 = struct.pack('16B', 255, 0, 0, 255, 0, 255, 0, 255, 255, 0, 0, 255, 0, 255, 0, 255)
        pixels2 = struct.pack('16B', 20, 30, 40, 255, 80, 70, 60, 255, 20, 30, 40, 255, 80, 70, 60, 255)
        texture = self.ctx.texture((2, 2), 4)

        pbo1 = self.ctx.buffer(pixels1)
        pbo2 = self.ctx.buffer(pixels2)

        fbo.use()
        texture.use()

        texture.write(pbo1)
        texture.filter = ModernGL.NEAREST
        self.vao.render(ModernGL.TRIANGLE_STRIP)

        r, g, b = struct.unpack('3B', fbo.read((5, 7, 1, 1)))
        self.assertTrue(abs(r - 255) < 8 and abs(g - 0) < 8 and abs(b - 0) < 8)

        r, g, b = struct.unpack('3B', fbo.read((10, 7, 1, 1)))
        self.assertTrue(abs(r - 0) < 8 and abs(g - 255) < 8 and abs(b - 0) < 8)

        texture.write(pbo2)
        texture.filter = ModernGL.NEAREST
        self.vao.render(ModernGL.TRIANGLE_STRIP)

        r, g, b = struct.unpack('3B', fbo.read((5, 7, 1, 1)))
        self.assertTrue(abs(r - 20) < 8 and abs(g - 30) < 8 and abs(b - 40) < 8)

        r, g, b = struct.unpack('3B', fbo.read((10, 7, 1, 1)))
        self.assertTrue(abs(r - 80) < 8 and abs(g - 70) < 8 and abs(b - 60) < 8)

    def test_4(self):
        pixels = struct.pack('16B', 255, 0, 0, 255, 0, 255, 0, 255, 255, 0, 0, 255, 0, 255, 0, 255)
        texture = self.ctx.texture((2, 2), 4, pixels)
        self.assertEqual(texture.read(), pixels)

    def test_5(self):
        pixels = struct.pack('16B', 255, 0, 0, 255, 0, 255, 0, 255, 255, 0, 0, 255, 0, 255, 0, 255)
        texture = self.ctx.texture((2, 2), 4, pixels)
        buf = bytearray(len(pixels))
        texture.read_into(buf)

        self.assertEqual(bytes(buf), pixels)

    def test_6(self):
        pixels = struct.pack('16B', 255, 0, 0, 255, 0, 255, 0, 255, 255, 0, 0, 255, 0, 255, 0, 255)
        texture = self.ctx.texture((2, 2), 4, pixels)
        pbo = self.ctx.buffer(reserve=len(pixels))
        texture.read_into(pbo)

        self.assertEqual(pbo.read(), pixels)


if __name__ == '__main__':
    unittest.main()
