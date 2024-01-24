import os
import unittest
from pprint import pprint
from unittest.mock import patch, mock_open
from smaug_cmd.domain.parsing import md_parsing

test_data_resource = os.getenv("TEST_DATA_RESOURCE") 

md_content = """---

kanban-plugin: basic

---

## Asian_Temple<br>中國東方高山寺廟

- [ ] ![[AsianTempleWide-1920x1080-3254a435ec9ac532e57cc9f390c80031.jpg]]![[AsianTemple_All.jpg]]![[HighresScreenshot00002 copy-1920x1080-bcd8b1ec4b74c0b94289d5a290cb608c.jpg]]![[Untitled200001.jpg-1920x1080-093eb78830ea1b5d3d25b9d76134b78a.jpg]]![[Untitled200012.jpg-1920x1080-a4f9dd9298cfcf1884d6315ade236a2a.jpg]]![[Untitled200023.jpg-1920x1080-10485def6c596075d7caa3f248fac5f1.jpg]]![[Untitled200034.jpg-1920x1080-7edaa2660c1f27924304e5faf23df17b.jpg]]![[Untitled200045.jpg-1920x1080-644da78f63e9c37d78239dfac0e83765.jpg]]![[Untitled200056.jpg-1920x1080-fe9bcbef415937b12a2688ff3135aaa5.jpg]]![[Untitled200067.jpg-1920x1080-8495590ffde0eb4d58413b35fa29628c.jpg]]![[Untitled200078.jpg-1920x1080-d2b6221a4181dbde8449b96a0cf26767.jpg]]![[Untitled200089.jpg-1920x1080-e11cbe01f7a1b349bfb1e4b8fd9a5eec.jpg]]![[Untitled2000910.jpg-1920x1080-3603eaec7a6fa25bfc9c3f7802ac07a5.jpg]]![[Untitled2001011.jpg-1920x1080-9f06da02bd8046ec2b90ef693bcb22a0.jpg]]![[Untitled2001112.jpg-1920x1080-c64d2ae518322fbeed7211e0ee99dce1.jpg]]![[Untitled2001213.jpg-1920x1080-77824efc7b09433e08eb0c009f8ee938.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/AsianTemple/)<br><br>東方寺廟、中國高山、飛鳥群、松柏木、藤蔓、龍雕像、片狀雲霧、瀑布、紅葉樹、松柏、河川


## House_Of_Changwon<br>韓國傳統建築

- [ ] ![[1-1920x1080-386e4d9801485f6bcd48d7dcaee90d2a.jpg]]![[10-1920x1080-f315fab967e2587dc0a8cfe3daa8fb1f.jpg]]![[2-1920x1080-a4935e8b7a099a70ccdae2a42c259ee5.jpg]]![[3-1920x1080-b9190448a7b0f8c25851f106743e52d8.jpg]]![[4-1920x1080-85bba27a53c878b62e2a57a31baec3d1.jpg]]![[5-1920x1080-952b7913047e611d6fe309ab527e4859.jpg]]![[6-1920x1080-4c08f320849e300103cd9a14b3e79bd5.jpg]]![[7-1920x1080-c5a7bb8f97f2e47e6f2181d61af95d0d.jpg]]![[8-1920x1080-9a983e242d9799a76413dbb30707693c.jpg]]![[9-1920x1080-2a9f262acddecb70481c17a18b6c22ba.jpg]]![[House Of Changwon_All.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/House_Of_Changwon/)<br><br>韓國傳統建築、昌原市韓國古代建築、涼亭、韓屋、木造建築、木造地板、木造門房、東方傳統瓦器瓷器、 匾額、東方傳統建築、階梯欄杆、屋樑、木工工具、東方傳統妝台、木箱、閂鎖


## Ray_Traced_Cinematic_Lighting<br>日式寺廟建築

- [ ] ![[52201920x1080-1920x1080-b4ee24e93a5fe0b9f112564815aefb64.jpg]]![[Ray_Traced_Cinematic_Lighting_All.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00000.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00001.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00002.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00003.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00004.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00005.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00006.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00007.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00008.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00009.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00010.jpg]]![[Ray_Traced_Cinematic_Lighting_HighresScreenshot00011.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Ray_Traced_Cinematic_Lighting/)<br><br>日式寺廟建築、龍石像、日本武士風格建築、石梯、石獅子、高塔、墓碑、石柱、香爐、地藏王石碑、石燈、高塔、日本武士風格獸人、木桌木椅、日式撞鐘


## Japanese_temple<br>日本寺廟建築

- [ ] ![[Japanese_temple_All.jpg]]![[Japanese_temple_Preview1.jpg]]![[Japanese_temple_Preview2.jpg]]![[Japanese_temple_Preview3.jpg]]![[Japanese_temple_Preview4.jpg]]![[Japanese_temple_Preview5.jpg]]![[Japanese_temple_Preview6.jpg]]![[Japanese_temple_Preview7.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Japanese_temple/)<br><br>日本寺廟、橋、木橋、鳥居、日式建築、和式、榻榻米、紙窗、紅柱


## Jejumok_Gwana<br>韓國傳統建築

- [ ] ![[1-1920x1080-8007bccbac0e1896cd7a8d0c8f5dc138.jpg]]![[2-1920x1080-4b7a572ae21cdc76a08feef8f4e49730.jpg]]![[3-1920x1080-5cf6344e1e57e4ce2b64acba9b8bf075.jpg]]![[4-1920x1080-be2cfff450a28647162de2d2c2e30464.jpg]]![[5-1920x1080-6429cce8a86e1c9178bb79aa452bae16.jpg]]![[6-1920x1080-9b7fc6aa94a428359350545e5362b29d.jpg]]![[7-1920x1080-a6856511b2a83e42fa4a9890eaf65167.jpg]]![[8-1920x1080-35e877e00eb8fef4401a7157fe5cc9ef.jpg]]![[Jejumok Gwana_All.jpg]]![[jj1-1920x1080-00cede112b9a7136ac1071a8e5cdfac9.jpg]]![[jj2-1920x1080-a09ff34f1c0effec9ad721e9ce912b86.jpg]]![[jj3-1920x1080-056795097930d9737efe70306d5fdcaf.jpg]]![[jj4-1920x1080-920abdd7318b082f2969cf8e24c542a8.jpg]]![[jj5-1920x1080-b48e82846d7e89e3d3f171988e44ca9f.jpg]]![[jj6-1920x1080-b1625065b2fee055e5c77e0606ab9762.jpg]]![[jj7-1920x1080-5be094a000948f33bcc24ec3a1bfa4ce.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Jejumok_Gwana/)<br><br>濟州牧官衙、韓國傳統建築、匾額、韓國傳統木造門房屋梁、磚牆、水井、墓碑、韓國傳統旗幟、石燈


## Korean_Traditional_Props<br>韓國傳統物件

- [ ] ![[1-1920x1080-e8577e470dc6d0de71ca7c2022590573.jpg]]![[10-1920x1080-9ed990c64850e5c46ed3410e512fcd96.jpg]]![[11-1920x1080-bccd61f08cae1b93474aaec21be82678.jpg]]![[12-1920x1080-1ef408839ed2c25b1b9480e7a009bb18.jpg]]![[13-1920x1080-6f0ab513be08792e46a7b3133361c33d.jpg]]![[2-1920x1080-f49e73f8fb6c041e81b56b95a84c5681.jpg]]![[3-1920x1080-b0a88f24e827fa637ae9536f34f87d6c.jpg]]![[4-1920x1080-e7a48cd6b9c5d9023e5f4535e540d9ba.jpg]]![[Korean Traditional Props_All.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Korean_Traditional_Props/)<br><br>韓國傳統物件、韓國傳統樂器、韓國傳統武器、伽倻琴、玄琴、杖鼓、蕭、韓服、石碑、石像、寶塔、洋槍、小刀


## Lowpoly_Style_Asia_Environment<br>古代東方村莊

- [ ] ![[Lowpoly Style Asia Environment_All.jpg]]![[LPSA00001-1920x1080-7c1703878e9febf6cfebb6da8ff2fe83.jpg]]![[LPSA00012-1920x1080-c04b5a21a8288af57ad5c8b872bf9985.jpg]]![[LPSA00023-1920x1080-2d8a4e831194ff8254e649b109ec9936.jpg]]![[LPSA00034-1920x1080-e2be426b8f8cde224acfe5b53ee7b576.jpg]]![[LPSA00045-1920x1080-44982a0094b8c76ecc0248527bb88793.jpg]]![[LPSA00056-1920x1080-d9a6f41742f91918c00cc8ed18ee2c7f.jpg]]![[LPSA00067-1920x1080-1547e278b87fca203aad22853e73384c.jpg]]![[LPSA00078-1920x1080-edddcdb7e9a304ee42f333937cdcf52d.jpg]]![[LPSA00089-1920x1080-554fb5923a97b30aea2526223c9ee3e1.jpg]]![[LPSA000910-1920x1080-550abdd5e393d1f82bcb86dd334b20c5.jpg]]![[LPSA001112-1920x1080-e157943e99d9e52ce8a8147bf770117c.jpg]]![[LPSA001314-1920x1080-a4dc1034d9ecab135fc28cbd46e28491.jpg]]![[LPSA001415-1920x1080-1fc9527bb650db562244f1ada13c770d.jpg]]![[LPSA001516-1920x1080-4041f1e05134183f70f3dfc238e33bf8.jpg]]![[LPSA001617-1920x1080-4e6c5e48b266940b9091a7a7f43961cb.jpg]]![[LPSA001718-1920x1080-e6fec53107c01118d6a627541959144c.jpg]]![[LPSA001819-1920x1080-9ba537a2a8aceaab437997a8ba0502b1.jpg]]![[LPSA001920-1920x1080-68d25f3f550bcde5191149ac4e28a66f.jpg]]![[LPSA002021-1920x1080-4d68da36e07512276726ce48428d8671.jpg]]![[LPSA002122-1920x1080-983cb23741d6e5a4a61f0d67d3c8702c.jpg]]![[LPSA002223-1920x1080-76b49c7dc3baf84bcc292809c7b49746.jpg]]![[LPSA002324-1920x1080-24d3f6fdb17ec365f9a4c0b49216f68b.jpg]]![[LPSA002425-1920x1080-7ef3f4eea3bbe0d5986b52c7295c48c5.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Lowpoly_Style_Asia_Environment/)<br><br>Lowpoly、古代東方低模建築、古代東方村莊、廟宇、佛像、鳥居、紅葉樹、低模植物、石獅子、日式建築、日式庭院、日式神社、Lowpoly 火堆 VFX


## Stylized_Eastern_Village<br>卡通風格古代東方村莊建築

- [ ] ![[01-1920x1080-478a600641db3f47ec6ded6ed62217c6.jpg]]![[02-1920x1080-9aae25915a112ec9bf8dc3b3317bcb63.jpg]]![[03-1920x1080-5ab5007a29a6c18dc9c66bc2d4e51ab7.jpg]]![[04-1920x1080-fac35135e0ff99608cfa46f16b7f0b4c.jpg]]![[05-1920x1080-475e2ad7c8ab50d0cb86b660ebe61b0a.jpg]]![[06-1920x1080-94e20d3a5459f603b9577cc0def5733b.jpg]]![[07-1920x1080-cca6a144c681570e13c70462e56cf77d.jpg]]![[08-1920x1080-90f53691cc049d8ade9464e3ac5382e3.jpg]]![[09-1920x1080-cfb2dbb862bbe7618a0e7babe8d115c1.jpg]]![[10-1920x1080-c3f79ae84386216d522b476fc71b3c38.jpg]]![[11-1920x1080-468cb5434c8fe6cedaab387ef0588abb.jpg]]![[13-1920x1080-17b668c3dcbc86831da77902e09e222f.jpg]]![[14-1920x1080-4092e7b56362a519475a742efc390038.jpg]]![[15-1920x1080-c077fab8343da2219b3e8fd7427d3679.jpg]]![[17-1920x1080-3d4a9c631cfbd327ac1e643fe5b16d4d.jpg]]![[Stylized Eastern Village_All.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Stylized_Eastern_Village/)<br><br>古代東方村莊建築、茅草屋、木造欄杆、竹林、紅葉樹、廟宇、木造燈、石像、木造階梯、石造階梯、棚子、岩塊、松木、木橋、古代東方門派、瀑布、水潭


## ZhangJiajie_Mountain<br>張家界高山古廟

- [ ] ![[HighresScreensh001-1920x1040-5dc0ed09fcf446ab72f2e217766ac500.jpg]]![[HighresScreensh002-1920x1040-eac0ebd533cdac0fcdf7b4b1c097ce76.jpg]]![[HighresScreensh003-1920x1040-dd258175e582a607e20d84444d84a30c.jpg]]![[HighresScreensh004 (1)-1920x1040-3a8a0e6c15d7d03dbf7c196f5c753e48.jpg]]![[HighresScreensh005-1920x1040-4c85e304714ab19272939009add69f53.jpg]]![[ZhangJiajieMountain_All.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/ZhangJiajieMountain/)<br><br>張家界高山、中國古廟、古松、松樹、巨岩、涼亭、瀑布、小水池、紅葉樹、石階、雲霧繚繞、石燈、峭壁、懸崖


## Slay_Animation_Sample<br>日式寺廟建築

- [ ] ![[Slay_Animation_Sample_All.jpg]]![[Slay_Marketplace_screenshot_1_1920x1080-5955f58cbd8f315c28db25f35955bd9e.jpg]]![[Slay_Marketplace_screenshot_2_1920x1080-6ee6ac6edcf363935e5317a49d91766a.jpg]]![[Slay_Marketplace_screenshot_3_1920x1080-b58307ae7a3c6f1214fb65dd678a95b5.jpg]]![[Slay_Marketplace_screenshot_4_1920x1080-2fb381376b0af8018ed0582680b4abfd.jpg]]<br><br>[Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/Slay_Animation_Sample/)<br><br>日式寺廟建築、龍石像、日本武士風格建築、石梯、石獅子、高塔、墓碑、石柱、香爐、地藏王石碑、石燈、高塔、日本武士風格獸人、木桌木已、日式撞鐘


## Japanses_Village<br>日式村莊古風建築

- [ ] [Open Folder](file://R:/_Asset/Game_Unreal/AncientEast/JapansesVillage/)<br><br>![[JapansesVillage_1361108-1171789708.jpg]]![[JapansesVillage_1361108-1248468267.jpg]]![[JapansesVillage_1361108-1283314766.jpg]]![[JapansesVillage_1361108-1299005827.jpg]]![[JapansesVillage_1361108-1313465731.jpg]]![[JapansesVillage_1361108-1315268934.jpg]]![[JapansesVillage_1361108-1463029867.jpg]]![[JapansesVillage_1361108-1510573088.jpg]]![[JapansesVillage_1361108-1596709077.jpg]]![[JapansesVillage_1361108-1759882641.jpg]]![[JapansesVillage_1361108-333612903.jpg]]![[JapansesVillage_1361108-538528032.jpg]]![[JapansesVillage_1361108-710789521.jpg]]<br><br>日式村莊、櫻花、古風建築、木屋、遊戲廳、居酒屋、櫻花樹、日式建築




%% kanban:settings
```
{"kanban-plugin":"basic"}
```
%%"""


class TestMdParsing2(unittest.TestCase):
    def test_md_json(self):
        md_file = f"{test_data_resource}/_Obsidian/MoonShineAsset/Unreal Asset/Unreal_AncientEast 古代東方場景.md"
        with patch("builtins.open", mock_open(read_data=md_content)) as mock_file:
            re = md_parsing(md_file)
            pprint(re)


if __name__ == "__main__":
    unittest.main()
