import os
import unittest
from smaug_cmd.entry.smaug_resource import smaug_resource_uploader

class TestResourceFolder(unittest.TestCase):

    def setUp(self):
        test_data_recource = os.environ["TEST_DATA_RESOURCE"]
        self._resource_folder1 = f"{test_data_recource}\\Source_Taiwan\\Culture01\\BTStation_HighPoly"
    
    def test_folder_parsing(self):
        re = smaug_resource_uploader(self._resource_folder1)


if __name__ == "__main__":
    unittest.main()