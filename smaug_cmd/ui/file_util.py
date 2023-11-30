import os
import ctypes


class FileUtils:
    @staticmethod
    def create_hidden_folder(folder_name):
        # 當前工作目錄
        current_directory = os.getcwd()

        # 完整路徑
        path = os.path.join(current_directory, folder_name)

        # 建立資料夾
        os.makedirs(path, exist_ok=True)

        # 在Windows下設置資料夾為隱藏
        if os.name == "nt":
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)

            if not ret:
                print(
                    f"Could not set {folder_name} as hidden. Error code: {ctypes.GetLastError()}"
                )
