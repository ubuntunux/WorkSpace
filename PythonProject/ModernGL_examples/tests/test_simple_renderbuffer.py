import unittest

import ModernGL

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_renderbuffer(self):
        self.ctx.renderbuffer((64, 64))

    def test_multisample_renderbuffer(self):
        if self.ctx.max_samples < 2:
            self.skipTest('multisampling is not supported')

        self.ctx.renderbuffer((64, 64), samples=2)

    def test_depth_renderbuffer(self):
        self.ctx.depth_renderbuffer((64, 64))

    def test_multisample_depth_renderbuffer(self):
        if self.ctx.max_samples < 2:
            self.skipTest('multisampling is not supported')

        self.ctx.depth_renderbuffer((64, 64), samples=2)

    def test_renderbuffer_invalid_samples(self):
        with self.assertRaisesRegex(ModernGL.Error, 'sample'):
            self.ctx.renderbuffer((64, 64), samples=3)


if __name__ == '__main__':
    unittest.main()
