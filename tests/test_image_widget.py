import sys

from PySide6.QtWidgets import QApplication

from smaug_cmd.ui.image import ImageDisplayWidget


class Tester:
    def __init__(self):
        app = QApplication(sys.argv)

        # Create the widget
        self.widget = ImageDisplayWidget()

        # Set sample images to display
        image_paths = [
            "/home/deck/Pictures/scandisk_MicroSD_512G.png",
            "/home/deck/Pictures/Screenshot_20230922_161431.png",
            "/home/deck/Pictures/eng7oct071q40wbmvav95hna.jpeg",
        ]  # Add paths to your images here
        self.widget.setPictures(image_paths)

        # Show the widget
        self.widget.show()

        sys.exit(app.exec())


if __name__ == "__main__":
    Tester()
