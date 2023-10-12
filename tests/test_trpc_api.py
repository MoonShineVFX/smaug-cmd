import unittest

from smaug_cmd.model.data import get_category


class TestTrpcApi(unittest.TestCase):

    def test_category_tree(self):
        value = get_category(7)
        assert value is not None

if __name__ == "__main__":
    unittest.main()
