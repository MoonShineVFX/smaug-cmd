import os
import unittest
from pprint import pprint
from unittest.mock import patch, mock_open
from smaug_cmd.domain.parsing import md_parsing

test_data_resource = os.getenv("TEST_DATA_RESOURCE") 

md_content = """---

kanban-plugin: basic

---

## Bag

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/Bag/)<br><br>![[201903_Jdb_Bag_lookdev_Preview_camera1.jpg]]![[201903_Jdb_Bag_lookdev_Preview_camera2.jpg]]<br><br>金元寶、錢袋


## folding_fan

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019_Obsidian/201903_Jdb/Prop/folding_fan/)<br><br>![[201903_Jdb_folding_fan_lookdev_Preview_camera1.jpg]]![[201903_Jdb_folding_fan_lookdev_Preview_camera2.jpg]]<br><br>扇子


## ChangAnGate

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Environment/ChangAnGate/)<br><br>![[TheBeltAndRoad_env_ChangAnGate_Preview.jpg]]<br><br>長安城門
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityBuildingHigh/)<br><br>![[ChangAnCityBuildingHigh_ABDE_Preview.jpg]]![[ChangAnCityBuildingHigh_BuildingWallAHigh_Preview.jpg]]![[ChangAnCityBuildingHigh_BuildingWallCHigh_Preview.jpg]]![[ChangAnCityBuildingHigh_FGIJ_Preview.jpg]]![[ChangAnCityBuildingHigh_LMNO_Preview.jpg]]![[ChangAnCityBuildingHigh_PQST_Preview.jpg]]![[ChangAnCityBuildingHigh_U_Preview.jpg]]<br><br>中國古代房屋


## ChangAnCityObj

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/BucketACandleAChair/)<br><br>![[BucketACandleAChair_Preview.jpg]]<br><br>椅凳、水桶、燭台、天平砝碼
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityBillboard/)<br><br>![[ChangAnCityBillboard_Preview.jpg]]<br><br>中國古代街道告示牌
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityFence/)<br><br>![[ChangAnCityFence_Preview.jpg]]<br><br>中國古代圍牆
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityFlag_ChangAnCityFlag/)<br><br>![[ChangAnCityFlag_ChangAnCityFlag_Preview.jpg]]<br><br>中國古代紅色裝飾吊飾、旗幟
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityLenternPole/)<br><br>![[ChangAnCityLenternPole_Preview.jpg]]<br><br>中國古代燈籠
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityLenternWall/)<br><br>![[ChangAnCityLenternWall_Preview.jpg]]<br><br>中國古代街道物件
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCitySign_Sign/)<br><br>![[ChangAnCitySign_Sign_Preview.jpg]]<br><br>中國古代招牌
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityStreetlightTowerCuju/)<br><br>![[ChangAnCityStreetlightTowerCuju_Preview.jpg]]<br><br>中國古代街道物件
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityVendor_Vendor/)<br><br>![[ChangAnCityVendor_Vendor_Preview.jpg]]<br><br>中國古代攤位
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/CupFenceFilterNetFlag/)<br><br>![[CupFenceFilterNetFlag_Preview.jpg]]<br><br>中國古代旗幟、茶葉曬藍
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/HanFlag/)<br><br>![[HanFlagHanFlag_Preview.jpg]]<br><br>中國古代旗幟
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/Jade/)<br><br>![[JadeJade_Preview.jpg]]<br><br>中國古代玉器
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/Kite/)<br><br>![[KiteKiteKite_Preview.jpg]]<br><br>中國古代風箏
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/Mirror/)<br><br>![[MirrorMirrorMirror_Preview.jpg]]<br><br>銅鏡


## ChangAnCityBuilding

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityBuildingMid/)<br><br>![[ChangAnCityBuildingMid_BuildingAMid_ABDEF_Preview.jpg]]![[ChangAnCityBuildingMid_BuildingAMid_GIJLM_Preview.jpg]]![[ChangAnCityBuildingMid_BuildingAMid_NOPQS_Preview.jpg]]![[ChangAnCityBuildingMid_BuildingAMid_XY_Preview.jpg]]
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityBuildingLow/)<br><br>![[ChangAnCityBuildingLow_A_Preview.jpg]]![[ChangAnCityBuildingLow_BuildingFloorLow_Preview.jpg]]![[ChangAnCityBuildingLow_XYX_Texture_Preview.jpg]]<br><br>中國古代建築、中國古代地板街道
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityPavilionPillar/)<br><br>![[ChangAnCityPavilionPillar_Preview.jpg]]<br><br>中國古代涼亭、中國古代旗幟
- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityStage/)<br><br>![[ChangAnCityStage_Preview.jpg]]<br><br>中國古代 擂台


## ChangAnCityPalace

- [ ] [Open Folder](file://R:/_Asset/MoonshineProject_2019/BundleProject_TheBeltAndRoad/TheBeltAndRoad/Prop/ChangAnCityPalace/)<br><br>![[ChangAnCityPalace_PalaceA_Preview.jpg]]![[ChangAnCityPalace_PalaceB_Preview.jpg]]![[ChangAnCityPalace_PalaceC_Preview.jpg]]![[ChangAnCityPalace_PalaceD_Preview.jpg]]![[ChangAnCityPalace_PalaceE_Preview.jpg]]<br><br>中國古代宮殿、中國古代城門




%% kanban:settings
```
{"kanban-plugin":"basic"}
```
%%"""


class TestMdParsing2(unittest.TestCase):
    def test_md_json(self):
        md_file = f"{test_data_resource}/_Obsidian/MoonShineAsset/Project 2019/Project2019_AncientEast 古代東方.md"
        with patch("builtins.open", mock_open(read_data=md_content)) as mock_file:
            re = md_parsing(md_file)
            pprint(re)


if __name__ == "__main__":
    unittest.main()
