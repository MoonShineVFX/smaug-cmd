import unittest
import time
from smaug_cmd.model.data import CachedNestedDict, NestedDict
from smaug_cmd import setting

setting.cache_time = 1


class TestCachedNestedDict(unittest.TestCase):

    def setUp(self):
        self.cache = CachedNestedDict()

    def test_set_and_get_value(self):
        self.cache[("api", "id", "1")] = "123"
        self.assertEqual(self.cache[("api", "id", "1")].value(), "123")

    def test_cache_expiration(self):
        self.cache[("api", "id", "2")] = "456"
        time.sleep(setting.cache_time + 1)  # Wait for cache to expire
        self.assertIsNone(self.cache[("api", "id", "2")].value())

    def test_nested_dict_creation(self):
        self.cache[("api", "id", "3")] = "789"
        self.assertIsInstance(self.cache[("api",)], CachedNestedDict)
        self.assertIsInstance(self.cache[("api", "id")], CachedNestedDict)
        self.assertIsInstance(self.cache[("api", "id", "3")], NestedDict)

    def test_nonexistent_key(self):
        self.assertIsNone(self.cache[("api", "nonexistent")].value())

    def test_single_key(self):
        self.cache["api"] = "endpoint"
        self.assertEqual(self.cache["api"].value(), "endpoint")

    def test_overwrite_value(self):
        self.cache[("api", "id", "4")] = "000"
        self.assertEqual(self.cache[("api", "id", "4")].value(), "000")
        self.cache[("api", "id", "4")] = "111"
        self.assertEqual(self.cache[("api", "id", "4")].value(), "111")

if __name__ == '__main__':
    unittest.main()