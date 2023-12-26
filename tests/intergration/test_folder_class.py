import unittest
from pprint import pprint
from smaug_cmd.domain.upload_strategies.avalon_source import (
    _group_files_by_directory,
    _filter_by_keywors
)


class TestFolderAva(unittest.TestCase):
    def setUp(self):
        self.ava_folder_list = [
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/201903_Jdb_Bag_lookdev_Preview_camera1.jpg",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/201903_Jdb_Bag_lookdev_Preview_camera2.jpg",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/Bag_lookdev.ma",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/Bag_lookdev_render.ma",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_BaseColor.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_BaseColor_sRGB_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_ground_BaseColor.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_ground_Height.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_ground_Metallic.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_ground_Normal.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_ground_Roughness.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Height.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Height_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Metallic.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Metallic_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Normal.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Normal_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Roughness.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_bag_Roughness_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_BaseColor.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_BaseColor_sRGB_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Height.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Height_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Metallic.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Metallic_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Normal.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Normal_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Roughness.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_ribbon_Roughness_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_BaseColor.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_BaseColor_sRGB_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Height.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Height_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Metallic.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Metallic_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Normal.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Normal_Raw_scene-linear Rec 709_sRGB.png.tx",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Roughness.png",
            "Y:/resource/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/_AvalonSource/texture/bag_all_yunbao_Roughness_Raw_scene-linear Rec 709_sRGB.png.tx",
        ]

    def test_folder_ava(self):
        keyword_group = ["_AvalonSource/texture", "_AvalonSource/texture_low"]
        group_files = _group_files_by_directory(self.ava_folder_list)
        filter_group_files = _filter_by_keywors(keyword_group, group_files)
        pprint(filter_group_files)


if __name__ == '__main__':
    unittest.main()

    