import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_1(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((4, 4)))

        fbo.clear(0.0, 0.0, 0.0, 0.0)

        self.assertEqual(fbo.read(components=4), b'\x00\x00\x00\x00' * 16)

        fbo.color_mask = (True, False, True, False)
        fbo.clear(0x19 / 255, 0x33 / 255, 0x4c / 255, 0x66 / 255)

        self.assertEqual(fbo.read(components=4), b'\x19\x00\x4c\x00' * 16)

        fbo.color_mask = (False, True, False, True)
        fbo.clear(0x7f / 255, 0x99 / 255, 0xb2 / 255, 0xcc / 255)

        self.assertEqual(fbo.read(components=4), b'\x19\x99\x4c\xcc' * 16)

    def test_2(self):
        fbo = self.ctx.framebuffer([
            self.ctx.renderbuffer((4, 4)),
            self.ctx.renderbuffer((4, 4)),
        ])

        fbo.clear(1.0, 1.0, 1.0, 1.0)

        self.assertEqual(fbo.read(components=4, attachment=0), b'\xff\xff\xff\xff' * 16)
        self.assertEqual(fbo.read(components=4, attachment=1), b'\xff\xff\xff\xff' * 16)

        fbo.color_mask = (
            (True, False, True, False),
            (False, True, False, True),
        )

        fbo.clear(0x19 / 255, 0x33 / 255, 0x4c / 255, 0x66 / 255)

        self.assertEqual(fbo.read(components=4, attachment=0), b'\x19\xff\x4c\xff' * 16)
        self.assertEqual(fbo.read(components=4, attachment=1), b'\xff\x33\xff\x66' * 16)

        fbo.color_mask = (
            (False, True, False, True),
            (True, False, True, False),
        )

        fbo.clear(0x7f / 255, 0x99 / 255, 0xb2 / 255, 0xcc / 255)

        self.assertEqual(fbo.read(components=4, attachment=0), b'\x19\x99\x4c\xcc' * 16)
        self.assertEqual(fbo.read(components=4, attachment=1), b'\x7f\x33\xb2\x66' * 16)


if __name__ == '__main__':
    unittest.main()
