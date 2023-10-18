import os
import unittest

from smaug_cmd.adapter import remote_fs as rfs


class TestRemoteFS(unittest.TestCase):
    def setUp(self):
        self.file = "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.png"

    def test_file_upload_and_delete(self):
        file_name = os.path.basename(self.file).split('.')[0]
        file_extension = os.path.splitext(self.file)[-1].lower()
        object_name = f"/test_asset_id/{file_name}_preview{file_extension}"
        upload_opbject_name = rfs.upload_file(self.file, object_name)
        self.assertTrue(upload_opbject_name == object_name)

        # delete file
        rfs.client.remove_object("smaug", upload_opbject_name)

        # list bucket smaug, should be empty
        objects = rfs.client.list_objects("smaug", recursive=True)
        self.assertTrue(len(objects) == 0)


if __name__ == "__main__":
    unittest.main()
