import os
import unittest

from smaug_cmd.services import remote_fs as rfs


class TestRemoteFS(unittest.TestCase):
    def setUp(self):
        self.file_linux = "/home/deck/repos/smaug/storage/_source/Tree_A/Texture/2K/Tree_A_Leaf_Low_Basecolor.png"
        self.file_win = "test_assets\\Tree_A\\Tree_A_Lowpoly.jpg"
        self.file = self.file_linux
    def test_file_upload_and_delete(self):
        if os.sys.platform == "win32":
            basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.file = os.path.join(basedir, self.file_win)
        file_name = os.path.basename(self.file).split('.')[0]
        file_extension = os.path.splitext(self.file)[-1].lower()
        object_name = f"/test_asset_id/{file_name}_preview{file_extension}"
        upload_opbject_name = rfs.put_file(self.file, object_name)
        self.assertTrue(upload_opbject_name == object_name)

        # delete file
        rfs.client.remove_object("smaug", upload_opbject_name)

        # list bucket smaug, should be empty
        objects = list(rfs.client.list_objects("smaug", recursive=True))
        self.assertTrue(len(objects) == 0)


if __name__ == "__main__":
    unittest.main()
