import os
import cv2
import logging
import numpy as np
from PySide6.QtGui import QPixmap, QPainter, QRadialGradient, QColor, QBrush
from PySide6.QtWidgets import QGraphicsBlurEffect, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtCore import Qt, QPoint

logger = logging.getLogger("smaug_smd.adapter.image_handler")


class CacheHandler:
    def __init__(self, asset_dir: str):
        self.asset_dir = asset_dir
        self.cache_dir = asset_dir + "/" + ".smaug"
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def get_cache_file(self, filename: str):
        return self.cache_dir + "/" + filename


class ImageHandler:
    @classmethod
    def make_thumbnail(cls, asset_dir: str, filepath: str):
        # 取得圖片暗部代表色
        dark_color = cls.extract_dark_color(filepath)
        dark_qcolor = QColor(dark_color[0], dark_color[1], dark_color[2], 255)
        # 建立一張以 filepath 丟到 blur_and_scale 的 pixmap 的底
        background_pixmap = cls.blur_and_scale(filepath)

        # 讀取圖片並縮放
        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            raise ValueError(f"The file {filepath} could not be loaded as a QPixmap.")
        pixmap_scaled = pixmap.scaled(
            420,
            270,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # 用 combine_images 將縮放後的圖片疊在模糊的圖片上
        combined_pixmap = cls.combine_images(pixmap_scaled, background_pixmap)
        # 套用暗角效果
        result_pixmap = cls.vignette(combined_pixmap, cornerColor=dark_qcolor)
        return result_pixmap

    @classmethod
    def blur_and_scale(cls, image_path):
        # 讀取圖片
        pixmap = QPixmap(image_path)
        if pixmap.size().width() <= 472:
            new_width = 472 + 40
        else:
            new_width = pixmap.size().width() + 40
        if pixmap.size().height() <= 270:
            new_height = 270 + 40
        else:
            new_height = pixmap.size().height() + 40

        pixmap = pixmap.scaled(
            new_width,
            new_height,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        # 創建模糊效果
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(50)  # 設定模糊半徑

        # 將模糊效果應用到圖片
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        item.setGraphicsEffect(blur_effect)
        scene.addItem(item)

        # 將模糊後的圖片轉換為QPixmap
        blurred_pixmap = QPixmap(pixmap.size())
        blurred_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(blurred_pixmap)
        scene.render(painter)
        painter.end()

        # 裁切圖片
        crop_pixmap = blurred_pixmap.copy(20, 20, 472, 270)
        # scaled_pixmap = blurred_pixmap.scaled(472, 270, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        return crop_pixmap

    @classmethod
    def extract_dark_color(cls, image_path, brightness_threshold=180) -> tuple[int, ...]:
        # 讀取圖像
        image = cv2.imread(image_path)

        # 轉換到HSV色彩空間
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 篩選出亮度低於閾值的像素
        dark_pixels = hsv_image[hsv_image[:, :, 2] < brightness_threshold]

        # 計算這些暗像素的平均色彩
        if len(dark_pixels) > 0:
            average_color = np.mean(dark_pixels, axis=0)
            rgb_color = cls.hsv_to_rgb(average_color)
            return rgb_color
        else:
            logger.warning(f"Could not extract a dark color from {image_path}.")
            return (0, 0, 0)

    @classmethod
    def combine_images(cls, center_image_path, background_image_path):
        # 讀取兩張圖片
        center_pixmap = QPixmap(center_image_path)
        background_pixmap = QPixmap(background_image_path)

        # 計算第二張圖片應該繪製的位置，使其位於中央
        x = (background_pixmap.width() - center_pixmap.width()) // 2
        y = (background_pixmap.height() - center_pixmap.height()) // 2

        # 創建一個painter來繪製合成的圖片
        painter = QPainter(background_pixmap)

        # 繪製第二張圖片
        painter.drawPixmap(x, y, center_pixmap)

        # 結束繪製
        painter.end()

        return background_pixmap

    @classmethod
    def vignette(cls, pixmap, cornerColor=QColor(0, 0, 0, 255)):
        # 創建一個和原圖一樣大小的 QPixmap 作為遮罩
        mask = QPixmap(pixmap.size())
        mask.fill(Qt.GlobalColor.transparent)
        # 創建一個 radial gradient 作為暗角
        gradient = QRadialGradient(
            QPoint(mask.width() / 2, mask.height() / 2),
            max(mask.width(), mask.height()) / 2,
        )
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, cornerColor)

        # 將 gradient 繪製到遮罩上
        painter = QPainter(mask)
        painter.fillRect(0, 0, mask.width(), mask.height(), QBrush(gradient))
        painter.end()

        # 將遮罩繪製到原圖上
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Multiply)
        painter.drawPixmap(0, 0, mask)
        painter.end()

        return pixmap

    @classmethod
    def hsv_to_rgb(cls, hsv):
        # 將HSV元組轉換為NumPy陣列，並調整形狀以符合cv2.cvtColor的要求
        hsv_array = np.array([[hsv]], dtype=np.uint8)

        # 使用cv2.cvtColor將HSV轉換為RGB
        rgb_array = cv2.cvtColor(hsv_array, cv2.COLOR_HSV2BGR)

        # 將RGB陣列轉換回元組
        rgb = tuple(map(int, rgb_array[0, 0]))

        return rgb