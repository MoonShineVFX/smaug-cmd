import os
import unittest
# from smaug_cmd.entry.smaug_resource import smaug_resource_uploader


class TestResourceFolder(unittest.TestCase):
    def setUp(self):
        test_data_recource = os.environ["TEST_DATA_RESOURCE"]
        self._resource_folder1 = (
            f"{test_data_recource}\\Source_Taiwan\\Culture01\\BTStation_HighPoly"
        )
        self._avalon_source1 = f"{test_data_recource}\\MoonshineProject_2019_Obsidian\\201903_Jdb\\Prop\\Bag"

    def test_folder_parsing(self):
        print(os.listdir(self._avalon_source1+"\\_AvalonSource"))
        # re = smaug_resource_uploader(self._resource_folder1)


if __name__ == "__main__":
    unittest.main()
