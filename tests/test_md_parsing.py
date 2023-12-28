import os
import unittest

from pprint import pprint
from dotenv import load_dotenv
from smaug_cmd.domain.parsing import (
    md_parsing_categories,
    md_combine_categories,
    md_parse_kanban_to_json,
    md_parsing_asset,
    md_parsing,
)

load_dotenv()


class TestMdCategory(unittest.TestCase):
    def setUp(self):
        TEST_DATA_RESOURCE = os.getenv("TEST_DATA_RESOURCE")
        test_data = [
            r"Project2019_AncientEast 古代東方.md",
            r"Project2019_Weapon 武器.md",
            r"_Pic",
        ]
        self.test_folder1 = [
            f"{TEST_DATA_RESOURCE}/_Obsidian/MoonShineAsset/Project 2019/{item}".replace(
                "\\", "/"
            )
            for item in test_data
        ]
        self.test_folder1_excepted = [
            [
                {
                    "cate_name": "Project 2019",
                    "parent": None,
                },
                {
                    "cate_name": "AncientEast",
                    "parent": "Project 2019",
                },
            ],
            [
                {"cate_name": "Project 2019", "parent": None},
                {
                    "cate_name": "Weapon",
                    "parent": "Project 2019",
                },
            ],
            [],
        ]

    def test_example(self):
        for idx, ma_path in enumerate(self.test_folder1):
            re = md_parsing_categories(ma_path)
            self.assertTrue(re == self.test_folder1_excepted[idx])
        print(self.test_folder1[1])


class TestMdContent(unittest.TestCase):
    def setUp(self):
        self.test_content1 = """
        ---

kanban-plugin: basic

---
## castle

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2020_Obsidian/202006_TheLegendOfHuangYi/Set/castle/)<br><br>202006_TheLegendOfHuangYi_castle_lookdev_render_Preview_camera1![[202006_TheLegendOfHuangYi_castle_lookdev_render_Preview_camera1.jpg]]-------------------------------202006_TheLegendOfHuangYi_castle_lookdev_render_Preview_camera2![[202006_TheLegendOfHuangYi_castle_lookdev_render_Preview_camera2.jpg]]-------------------------------<br>中國古代城牆、古城

## Monster

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2020_Obsidian/202006_VrMazu/Char/Monster/)<br><br>202006_VrMazu_Monster_lookdev_render_Preview_camera1![[202006_VrMazu_Monster_lookdev_render_Preview_camera1.jpg]]-------------------------------202006_VrMazu_Monster_lookdev_render_Preview_camera2![[202006_VrMazu_Monster_lookdev_render_Preview_camera2.jpg]]-------------------------------<br><br>中國神獸

## CiacdaDove

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2020/BundleProject_TeaGold/Char/CiacdaDove/)<br><br>![[TeaGold_Char_CiacdaDove_Preview.jpg]]<br><br>蟬、鴿子
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2020/BundleProject_TeaGold/Char/Teahopper/)<br><br>![[TeaGold_Char_Teahopper_Preview.jpg]]<br><br>小蚱蜢

%% kanban:settings
```
{"kanban-plugin":"basic"}
```
%%
"""

    def test_md_parsing_content(self):
        test_data_resource = os.environ.get("TEST_DATA_RESOURCE")
        re = md_parse_kanban_to_json(self.test_content1)
        self.assertTrue(
            re
            == [
                {
                    "asset_name": "castle",
                    "data": [
                        {
                            "description": "中國古代城牆、古城",
                            "folder": f"{test_data_resource}/MoonshineProject_2020_Obsidian/202006_TheLegendOfHuangYi/Set/castle/".replace("\\", "/"),
                            "previews": [
                                "202006_TheLegendOfHuangYi_castle_lookdev_render_Preview_camera1.jpg",
                                "202006_TheLegendOfHuangYi_castle_lookdev_render_Preview_camera2.jpg",
                            ],
                        }
                    ],
                },
                {
                    "asset_name": "Monster",
                    "data": [
                        {
                            "description": "中國神獸",
                            "folder": f"{test_data_resource}/MoonshineProject_2020_Obsidian/202006_VrMazu/Char/Monster/".replace("\\", "/"),
                            "previews": [
                                "202006_VrMazu_Monster_lookdev_render_Preview_camera1.jpg",
                                "202006_VrMazu_Monster_lookdev_render_Preview_camera2.jpg",
                            ],
                        }
                    ],
                },
                {
                    "asset_name": "CiacdaDove",
                    "data": [
                        {
                            "description": "蟬、鴿子",
                            "folder": f"{test_data_resource}/MoonshineProject_2020/BundleProject_TeaGold/Char/CiacdaDove/".replace("\\", "/"),
                            "previews": ["TeaGold_Char_CiacdaDove_Preview.jpg"],
                        },
                        {
                            "description": "小蚱蜢",
                            "folder": f"{test_data_resource}/MoonshineProject_2020/BundleProject_TeaGold/Char/Teahopper/".replace("\\", "/"),
                            "previews": ["TeaGold_Char_Teahopper_Preview.jpg"],
                        },
                    ],
                },
            ]
        )


if __name__ == "__main__":
    unittest.main()
