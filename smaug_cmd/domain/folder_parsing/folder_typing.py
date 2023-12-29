from enum import Enum


class FolderType(Enum):
    """Enum for the type of resource folder."""

    UNKNOWN = "UNKNOWN"

    ASSET_DEPART_MODEL = "ADM"
    # 資料夾下有 Texture, Render, Model 三個目錄
    # 目錄下有多張 preview 圖片

    AVALON_SOURCE_MODEL = "ASM"
    # 目錄下有多張 preview 圖片
    # 目錄下會有 _AvalonSource 資料夾,
    # 目錄下有 _AvalonSource 目錄
    # _AvalonSource 下會有數個 texture 目錄，通常名為texture, texture_low, ...等等， 並包含多個 dcc 檔案
    # 至少要有一個 dcc 檔跟一個貼圖檔
    # _AvalonSource 下會有 preview 檔，需排除
    # dcc 檔可能有變體, 例加有後綴 _low 的模型檔案, Optional
    # 範例目錄：
    #     _Asset\MoonshineProject_2019_Obsidian\201903_Jdb\Prop\Bag
    #     _Asset\MoonshineProject_2020_Obsidian\202007_LianYue\Props\Backpack

    NORMAL_RESOURCE_MODEL = "NRM"
    # 資料夾下有一個貼圖目錄，名字可能為 Texture、tex,
    # 資料夾下有多個 dcc 檔案
    # 資料夾下有複數 preview 圖片
    # 有時也會在 folder_path 下有一個 Texture_JPG 資料夾，放置轉為 JPG 的貼圖檔案，這個資料夾為 Optinoal
    # 在指定該有 dcc 檔的地方應該最少要有一個 dcc 檔案
    # 在指定該有貼圖的地方最少要有一個貼圖檔案
    # 範例目錄：
    #     _Asset\MoonshineProject_2019\BundleProject_TheBeltAndRoad\TheBeltAndRoad\Environment\ChangAnGate
    #     _Asset\MoonshineProject_2020_Obsidian\202003_AdventureLemon\jianguo

    # DOWNLOAD_VARIANT1_MODEL = "DVM"
    # 資料夾下數個以 `uploads_files_` 開頭的資料夾，內含貼圖跟 dcc 檔，該資料夾的名稱 `+` 替代 ` `(空白)
    # 資料夾下也有 preview 圖片

    # example:
    #     _Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\robotic_arm
    #     _Asset\MoonshineProject_2020_Obsidian\202001_AsusBrandVideo4\Buy\Sci+Fi+Power+Suit

    THREE_MAX_MODEL = "3DM"
    # 資料夾裡有 3d_max 目錄

    # example:
    #     _Asset\MoonshineProject_2020_Obsidian\202003_ChptWokflow\DHQ

    TAIWAN_CULTURE_MODEL = "TCM"
    # 資料夾下有 dcc 檔，通常為 fbx
    # 資料夾下有數個 preview 圖檔
    # 有 3D 目錄, 下有其他的 dcc 檔
    # 有 texture 目錄, 下有貼圖
    # 有 Preview 目錄, 目錄裡的也是 preview 圖檔
    # 有 Render 目錄, 下有 render 出來的圖檔

    # example:
    #     _Asset\Source_Taiwan\Culture01\BTStation_HighPoly

    UASSET_MODEL = "UM"
