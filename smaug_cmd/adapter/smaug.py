import ctypes
import logging
import json
import os

logger = logging.getLogger("smaug_cmd.adapter")


class SmaugJson:
    def __init__(self, asset_base_path: str):
        self._dot_smaug = os.path.join(asset_base_path, ".smaug").replace("\\", "/")
        self.create_dot_smaug_folder()
        self.json_file = os.path.join(self._dot_smaug, "smaug.json").replace("\\", "/")
        self._data: dict = {}
        self.deserialize()  # load data from json file

    def serialize(self):
        try:
            if not os.path.exists(self._dot_smaug):
                os.makedirs(self._dot_smaug, exist_ok=True)
            with open(self.json_file, "w") as f:
                json.dump(self._data, f, indent=4)
        except Exception as e:
            logger.error("Failed to serialize smaug.json. Reson: %s", e)

    def deserialize(self) -> dict:
        try:
            if not os.path.exists(self.json_file):
                return {}
            with open(self.json_file, "r") as f:
                smaug_data = f.read()
            data = json.loads(smaug_data)
            self._data.update(data)
            return data
        except Exception as e:
            logger.error("Failed to deserialize smaug.json: %s", e)
            return {}

    def create_dot_smaug_folder(self):
        if os.path.exists(self._dot_smaug):
            return
        # 建立資料夾
        os.makedirs(self._dot_smaug, exist_ok=True)

        # 在Windows下設置資料夾為隱藏
        if os.name == "nt":
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ret = ctypes.windll.kernel32.SetFileAttributesW(
                self._dot_smaug, FILE_ATTRIBUTE_HIDDEN
            )

            if not ret:
                print(
                    f"Could not set {self._dot_smaug} as hidden. Error code: {ctypes.GetLastError()}"
                )

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __enter__(self):
        return self._data

    def __exit__(self, exc_type, exc_value, traceback):
        self.serialize()
