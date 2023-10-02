from PySide6.QtWidgets import QApplication
from smaug_cmd.ui import CategoryListWidget


menu_tree_home = {
    "id": "clmriy1pz0009bq90cuqtpyff",
    "name": "Home",
    "iconName": "menu",
    "children": [
        {
            "id": 19,
            "name": "3D Plants",
            "children": [
                {
                    "id": 20,
                    "name": "Bushes",
                    "children": []
                },
                {
                    "id": 21,
                    "name": "Flower",
                    "children": []
                },
                {
                    "id": 22,
                    "name": "Grass",
                    "children": []
                },
                {
                    "id": 23,
                    "name": "Tree",
                    "children": []
                }
            ]
        },
        {
            "id": 24,
            "name": "Surfaces",
            "children": [
                {
                    "id": 25,
                    "name": "Brick",
                    "children": []
                },
                {
                    "id": 26,
                    "name": "Concrete",
                    "children": []
                },
                {
                    "id": 27,
                    "name": "Fabric",
                    "children": []
                },
                {
                    "id": 28,
                    "name": "Ground",
                    "children": []
                },
                {
                    "id": 29,
                    "name": "Lawn",
                    "children": []
                },
                {
                    "id": 30,
                    "name": "Marble",
                    "children": []
                },
                {
                    "id": 31,
                    "name": "Metal",
                    "children": []
                },
                {
                    "id": 32,
                    "name": "Rock",
                    "children": []
                },
                {
                    "id": 33,
                    "name": "Roofing",
                    "children": []
                },
                {
                    "id": 34,
                    "name": "Sand",
                    "children": []
                },
                {
                    "id": 35,
                    "name": "Snow",
                    "children": []
                },
                {
                    "id": 36,
                    "name": "Soil",
                    "children": []
                },
                {
                    "id": 37,
                    "name": "Stone",
                    "children": []
                },
                {
                    "id": 38,
                    "name": "Tile",
                    "children": []
                },
                {
                    "id": 39,
                    "name": "Wood",
                    "children": []
                },
                {
                    "id": 41,
                    "name": "Other",
                    "children": []
                }
            ]
        },
        {
            "id": 1,
            "name": "No Category",
            "children": []
        },
        {
            "id": 2,
            "name": "2D Asset",
            "children": [
                {
                    "id": 3,
                    "name": "FX",
                    "children": []
                }
            ]
        },
        {
            "id": 4,
            "name": "3D Asset",
            "children": [
                {
                    "id": 8,
                    "name": "Building",
                    "children": []
                },
                {
                    "id": 9,
                    "name": "Char",
                    "children": [
                        {
                            "id": 10,
                            "name": "Male",
                            "children": []
                        },
                        {
                            "id": 11,
                            "name": "Parts",
                            "children": []
                        }
                    ]
                },
                {
                    "id": 12,
                    "name": "Indoor",
                    "children": []
                },
                {
                    "id": 13,
                    "name": "Exterior",
                    "children": []
                },
                {
                    "id": 14,
                    "name": "Naturel",
                    "children": [
                        {
                            "id": 15,
                            "name": "Rocks",
                            "children": []
                        }
                    ]
                },
                {
                    "id": 16,
                    "name": "Scene",
                    "children": []
                },
                {
                    "id": 17,
                    "name": "Product",
                    "children": []
                },
                {
                    "id": 18,
                    "name": "Weapon",
                    "children": []
                },
                {
                    "id": 5,
                    "name": "Accessories",
                    "children": []
                },
                {
                    "id": 6,
                    "name": "Animal",
                    "children": [
                        {
                            "id": 7,
                            "name": "Fish",
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "id": 40,
            "name": "Other",
            "children": []
        }
    ]
}


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication()
    
    my_widget =CategoryListWidget()
    my_widget.show()
    my_widget.addMenuTree(menu_tree_home)
    app.exec()
