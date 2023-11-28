import os
from typing import Optional
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ImageHandler:
    @staticmethod
    def make_thumbnail(asset_dir:str, filepath:Optional[str]=None):
        if filepath is None:
            return ''
        pixmap = QPixmap(filepath)
        cache_dir = asset_dir + "/" + ".smaug"
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        cache_file = cache_dir+ "/" +"preview.png"
        pixmap_scaled = pixmap.scaled(420, 270, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap_scaled.save(cache_file)
        return cache_file
