import os
import unittest

import ModernGL


class TestCase(unittest.TestCase):

    def test_local(self):
        path1 = os.path.normpath(os.path.dirname(os.path.dirname(ModernGL.__file__)))
        path2 = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.assertEqual(path1.lower(), path2.lower(), msg='Using installed ModernGL')


if __name__ == '__main__':
    unittest.main()
