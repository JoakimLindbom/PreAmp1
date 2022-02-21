import unittest
from ButtonController import ButtonController

class testBC_Len(unittest.TestCase):
    def test_len(self):
        a = ButtonController()
        b = a.get_config("buttons.yaml")

        self.assertEqual(b, 1)
