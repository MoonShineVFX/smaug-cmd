import os
import unittest
from unittest.mock import patch
from smaug_cmd.domain.folder_parsing import (
    is_asset_depart_model_folder,
    is_3dmax_model_folder,
    is_avalon_source_model_folder,
    is_taiwan_culture_model_folder,
    is_normal_resource_model_folder,
    is_download_variant1_model_folder,
)

from smaug_cmd.domain.folder_class import FolderClassFactory
from dotenv import load_dotenv

from smaug_cmd.domain.folder_parsing.folder_typing import FolderType

load_dotenv()

TEST_DATA_RESOURCE = os.getenv("TEST_DATA_RESOURCE")


class TestKindOfFolder(unittest.TestCase):
    def test_is_asset_depart_model_folder(self):
        asset_depart_return = [
            "Tree_A_Lowpoly.jpg",
            ".smaug",
            "Model",
            "Render",
            "Texture",
        ]
        with patch(
            "smaug_cmd.domain.folder_parsing.util.list_dir",
            return_value=asset_depart_return,
        ):
            asset_depart_folder = f"{TEST_DATA_RESOURCE}\\Asset_Depart\\Tree_A"
            self.assertFalse(is_taiwan_culture_model_folder(asset_depart_folder))
            self.assertFalse(is_avalon_source_model_folder(asset_depart_folder))
            self.assertTrue(is_asset_depart_model_folder(asset_depart_folder))
            self.assertFalse(is_normal_resource_model_folder(asset_depart_folder))
            self.assertFalse(is_download_variant1_model_folder(asset_depart_folder))
            self.assertFalse(is_3dmax_model_folder(asset_depart_folder))

    def test_is_taiwan_culture_model_folder(self):
        taiwain_return = [
            "3D",
            "BTStation_HighPoly.fbx",
            "BTStation_HighPoly_Large_0.jpg",
            "BTStation_HighPoly_Large_1.jpg",
            "BTStation_HighPoly_Large_2.jpg",
            "BTStation_HighPoly_Large_3.jpg",
            "BTStation_HighPoly_Large_4.jpg",
            "BTStation_HighPoly_Large_5.jpg",
            "BTStation_HighPoly_Large_6.jpg",
            "BTStation_HighPoly_Large_7.jpg",
            "BTStation_HighPoly_Large_8.jpg",
            "BTStation_HighPoly_Large_9.jpg",
            "BTStation_HighPoly_Small.jpg",
            "galaxy.json",
            "Preview",
            "Render",
            "texture",
        ]
        with patch(
            "smaug_cmd.domain.folder_parsing.util.list_dir", return_value=taiwain_return
        ):
            taiwan_folder = f"{TEST_DATA_RESOURCE}\\TaiwanCultureProject_2020\\3D\\BTStation_HighPoly"
            self.assertTrue(is_taiwan_culture_model_folder(taiwan_folder))
            self.assertFalse(is_avalon_source_model_folder(taiwan_folder))
            self.assertFalse(is_normal_resource_model_folder(taiwan_folder))
            self.assertFalse(is_download_variant1_model_folder(taiwan_folder))
            self.assertFalse(is_3dmax_model_folder(taiwan_folder))

    def test_is_avalon_source_model_folder(self):
        ava_folder_return = [
            "202007_LianYue_Backpack_lookdev_render_Preview_camera1.jpg",
            "202007_LianYue_Backpack_lookdev_render_Preview_camera2.jpg",
            "_AvalonSource",
            "已上架.txt",
        ]
        with patch(
            "smaug_cmd.domain.folder_parsing.util.list_dir",
            return_value=ava_folder_return,
        ):
            ava_folder = f"{TEST_DATA_RESOURCE}\\MoonshineProject_2020_Obsidian\\202007_LianYue\\Props\\Backpack"
            self.assertFalse(is_taiwan_culture_model_folder(ava_folder))
            self.assertTrue(is_avalon_source_model_folder(ava_folder))
            self.assertFalse(is_normal_resource_model_folder(ava_folder))
            self.assertFalse(is_download_variant1_model_folder(ava_folder))
            self.assertFalse(is_3dmax_model_folder(ava_folder))

    def test_is_download_variant1_model_folder(self):
        down_variant1 = [
            "dobot-magician-smart-robotic-arm-3d-model-max-obj-3ds-fbx-c4d-lwo-lw-lws.jpg",
            "uploads_files_791169_Dobot+Magician+-+Standard",
            "uploads_files_791169_Dobot+Magician+-+Vray",
            "uploads_files_791169_Dobot+Magician+-+Vray+Light",
        ]
        with patch(
            "smaug_cmd.domain.folder_parsing.util.list_dir", return_value=down_variant1
        ):
            down_variant1_folder = f"{TEST_DATA_RESOURCE}\\MoonshineProject_2020_Obsidian\\202003_ChptWokflow\\robotic_arm"
            self.assertFalse(is_taiwan_culture_model_folder(down_variant1_folder))
            self.assertFalse(is_avalon_source_model_folder(down_variant1_folder))
            self.assertFalse(is_normal_resource_model_folder(down_variant1_folder))
            self.assertTrue(is_download_variant1_model_folder(down_variant1_folder))
            self.assertFalse(is_3dmax_model_folder(down_variant1_folder))

    def test_is_3dmax_model_folder(self):
        threed_max = ["202003_ChptWokflow_DHQ.jpg", "3d_Max"]
        with patch(
            "smaug_cmd.domain.folder_parsing.util.list_dir", return_value=threed_max
        ):
            threed_max_folder = f"{TEST_DATA_RESOURCE}\\MoonshineProject_2020_Obsidian\\202003_ChptWokflow\\DHQ"
            self.assertFalse(is_taiwan_culture_model_folder(threed_max_folder))
            self.assertFalse(is_avalon_source_model_folder(threed_max_folder))
            self.assertFalse(is_normal_resource_model_folder(threed_max_folder))
            self.assertFalse(is_download_variant1_model_folder(threed_max_folder))
            self.assertTrue(is_3dmax_model_folder(threed_max_folder))


class TestFolderClass(unittest.TestCase):
    def test_folder_asset_depart(self):
        asset_depart_return = [
            "Tree_A_Lowpoly.jpg",
            ".smaug",
            "Model",
            "Render",
            "Texture",
        ]
        with patch(
            "smaug_cmd.domain.folder_parsing.util.list_dir",
            return_value=asset_depart_return,
        ):
            ava_folder = f"{TEST_DATA_RESOURCE}\\MoonshineProject_2020_Obsidian\\202007_LianYue\\Props\\Backpack"
            folder_obj = FolderClassFactory(ava_folder).create()
            self.assertTrue(folder_obj.folder_type() == FolderType.ASSET_DEPART_MODEL)


if __name__ == "__main__":
    unittest.main()
