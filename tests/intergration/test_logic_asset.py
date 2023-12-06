import unittest
from smaug_cmd.domain import command as cmd
from smaug_cmd.adapter.cmd_handlers.handler import handler

class TestLogicAsset(unittest.TestCase):
    def test_asset_create(self):
        create_cmd = cmd.CreateAsset(name="test", categoryId=1, meta={}, tags=["測試"])
        re = handler(create_cmd)
        self.assertTrue(re)
        

if __name__ == "__main__":
    unittest.main()