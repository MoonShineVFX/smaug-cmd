import unittest
from smaug_cmd.model.data import get_menus

class TestGetMenusIntegration(unittest.TestCase):
    def test_get_menus(self):
        # Act
        result = get_menus()

        # Assert
        self.assertTrue(result is not None)


if __name__ == '__main__':
    unittest.main()