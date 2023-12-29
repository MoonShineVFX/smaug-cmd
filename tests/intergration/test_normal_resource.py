import os
from pprint import pprint
import unittest
from unittest.mock import patch
from smaug_cmd.domain.folder_parsing import FolderType
from smaug_cmd.domain.folder_parsing import NormalResourceFolder
from smaug_cmd.domain.upload_strategies import NormalResourceUploadStrategy

test_data_resource = os.environ.get("TEST_DATA_RESOURCE")

walk_data = [
    (
        f"{test_data_resource}/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Environment/ChangAnGate",
        [".mayaSwatches", "Texture", "Texture_JPG"],
        [
            "TheBeltAndRoad_env_ChangAnGate.fbx",
            "TheBeltAndRoad_env_ChangAnGate.max",
            "TheBeltAndRoad_env_ChangAnGate.mb",
            "TheBeltAndRoad_env_ChangAnGate_Preview.jpg",
            "TheBeltAndRoad_env_ChangAnGate_Preview.png",
            "Thumbs.db",
            "已上架.txt",
        ],
    ),
    (
        f"{test_data_resource}/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Environment/ChangAnGate/.mayaSwatches",
        [],
        ["ChangAnGate.mb.swatches"],
    ),
    (
        f"{test_data_resource}/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Environment/ChangAnGate/Texture",
        [],
        [
            "ChangAnGate_Ceiling_SHDR_BaseColor.png",
            "ChangAnGate_Ceiling_SHDR_Height.png",
            "ChangAnGate_Ceiling_SHDR_Normal.png",
            "ChangAnGate_Ceiling_SHDR_Roughness.png",
            "ChangAnGate_F_BaseColor.png",
            "ChangAnGate_F_Height.png",
            "ChangAnGate_F_Normal.png",
            "ChangAnGate_F_Roughness.png",
            "ChangAnGate_Outside_1001_BaseColor.png",
            "ChangAnGate_Outside_1001_Metallic.png",
            "ChangAnGate_Outside_1001_Normal.png",
            "ChangAnGate_Outside_1001_Roughness.png",
            "ChangAnGate_Outside_1002_BaseColor.png",
            "ChangAnGate_Outside_1002_Metallic.png",
            "ChangAnGate_Outside_1002_Normal.png",
            "ChangAnGate_Outside_1002_Roughness.png",
            "ChangAnGate_Outside_1003_BaseColor.png",
            "ChangAnGate_Outside_1003_Metallic.png",
            "ChangAnGate_Outside_1003_Normal.png",
            "ChangAnGate_Outside_1003_Roughness.png",
            "ChangAnGate_Outside_1004_BaseColor.png",
            "ChangAnGate_Outside_1004_Metallic.png",
            "ChangAnGate_Outside_1004_Normal.png",
            "ChangAnGate_Outside_1004_Roughness.png",
            "ChangAnGate_Outside_1005_BaseColor.png",
            "ChangAnGate_Outside_1005_Metallic.png",
            "ChangAnGate_Outside_1005_Normal.png",
            "ChangAnGate_Outside_1005_Roughness.png",
            "ChangAnGate_Outside_1006_BaseColor.png",
            "ChangAnGate_Outside_1006_Metallic.png",
            "ChangAnGate_Outside_1006_Normal.png",
            "ChangAnGate_Outside_1006_Roughness.png",
            "ChangAnGate_Outside_1007_BaseColor.png",
            "ChangAnGate_Outside_1007_Metallic.png",
            "ChangAnGate_Outside_1007_Normal.png",
            "ChangAnGate_Outside_1007_Roughness.png",
            "ChangAnGate_Outside_1008_BaseColor.png",
            "ChangAnGate_Outside_1008_Metallic.png",
            "ChangAnGate_Outside_1008_Normal.png",
            "ChangAnGate_Outside_1008_Roughness.png",
            "ChangAnGate_Outside_1009_BaseColor.png",
            "ChangAnGate_Outside_1009_Metallic.png",
            "ChangAnGate_Outside_1009_Normal.png",
            "ChangAnGate_Outside_1009_Roughness.png",
            "ChangAnGate_Outside_1010_BaseColor.png",
            "ChangAnGate_Outside_1010_Metallic.png",
            "ChangAnGate_Outside_1010_Normal.png",
            "ChangAnGate_Outside_1010_Roughness.png",
        ],
    ),
    (
        f"{test_data_resource}/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Environment/ChangAnGate/Texture_JPG",
        [],
        [
            "ChangAnGate_Ceiling_SHDR_BaseColor.jpg",
            "ChangAnGate_Ceiling_SHDR_Height.jpg",
            "ChangAnGate_Ceiling_SHDR_Normal.jpg",
            "ChangAnGate_Ceiling_SHDR_Roughness.jpg",
            "ChangAnGate_F_BaseColor.jpg",
            "ChangAnGate_F_Height.jpg",
            "ChangAnGate_F_Normal.jpg",
            "ChangAnGate_F_Roughness.jpg",
            "ChangAnGate_Outside_BaseColor_1001.jpg",
            "ChangAnGate_Outside_BaseColor_1002.jpg",
            "ChangAnGate_Outside_BaseColor_1003.jpg",
            "ChangAnGate_Outside_BaseColor_1004.jpg",
            "ChangAnGate_Outside_BaseColor_1005.jpg",
            "ChangAnGate_Outside_BaseColor_1006.jpg",
            "ChangAnGate_Outside_BaseColor_1007.jpg",
            "ChangAnGate_Outside_BaseColor_1008.jpg",
            "ChangAnGate_Outside_BaseColor_1009.jpg",
            "ChangAnGate_Outside_BaseColor_1010.jpg",
            "ChangAnGate_Outside_Metallic_1001.jpg",
            "ChangAnGate_Outside_Metallic_1002.jpg",
            "ChangAnGate_Outside_Metallic_1003.jpg",
            "ChangAnGate_Outside_Metallic_1004.jpg",
            "ChangAnGate_Outside_Metallic_1005.jpg",
            "ChangAnGate_Outside_Metallic_1006.jpg",
            "ChangAnGate_Outside_Metallic_1007.jpg",
            "ChangAnGate_Outside_Metallic_1008.jpg",
            "ChangAnGate_Outside_Metallic_1009.jpg",
            "ChangAnGate_Outside_Metallic_1010.jpg",
            "ChangAnGate_Outside_Normal_1001.jpg",
            "ChangAnGate_Outside_Normal_1002.jpg",
            "ChangAnGate_Outside_Normal_1003.jpg",
            "ChangAnGate_Outside_Normal_1004.jpg",
            "ChangAnGate_Outside_Normal_1005.jpg",
            "ChangAnGate_Outside_Normal_1006.jpg",
            "ChangAnGate_Outside_Normal_1007.jpg",
            "ChangAnGate_Outside_Normal_1008.jpg",
            "ChangAnGate_Outside_Normal_1009.jpg",
            "ChangAnGate_Outside_Normal_1010.jpg",
            "ChangAnGate_Outside_Roughness_1001.jpg",
            "ChangAnGate_Outside_Roughness_1002.jpg",
            "ChangAnGate_Outside_Roughness_1003.jpg",
            "ChangAnGate_Outside_Roughness_1004.jpg",
            "ChangAnGate_Outside_Roughness_1005.jpg",
            "ChangAnGate_Outside_Roughness_1006.jpg",
            "ChangAnGate_Outside_Roughness_1007.jpg",
            "ChangAnGate_Outside_Roughness_1008.jpg",
            "ChangAnGate_Outside_Roughness_1009.jpg",
            "ChangAnGate_Outside_Roughness_1010.jpg",
        ],
    ),
]


class TestNormalResourceFolder(unittest.TestCase):

    def test_create_folder_folder(self):
        with patch("os.walk", return_value=walk_data):
            folder_obj = NormalResourceFolder(
                f"{test_data_resource}/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Environment/ChangAnGate",
                NormalResourceUploadStrategy(),
            )

            self.assertTrue(folder_obj.folder_type() == FolderType.NORMAL_RESOURCE_MODEL, "folder type is worng")


    def test_group_files_rename_and_upload(self):
        pass


if __name__ == "__main__":
    unittest.main()

    # import os

    # walk_data = list()
    # for root, dirs, files in os.walk(
    #     r"C:\repos\smaugs\resource\_Asset\MoonshineProject_2019\BundleProject_TheBeltAndRoad\TheBeltAndRoad\Environment\ChangAnGate"
    # ):
    #     pack = (root, dirs, files)
    #     walk_data.append(pack)
    # pprint(walk_data)
