import json
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QIcon


AssetRole = Qt.ItemDataRole.UserRole + 1 


class UploadModel(QAbstractTableModel):
    def __init__(self, assets=None, parent=None):
        super(UploadModel, self).__init__(parent)
        self.assets = assets if assets else list()  # a list of asset object ( a dict )
        self.assets_folder = ""
        self._base_header = [
            "upload",
            "progress",
            "icon_path",
            "chinese_name",
            "english_name",
            "category",
            "tags",
        ]
        self._header_map = {
            "icon_path": "Preview",
            "chinese_name": "Chinese Name",
            "english_name": "English Name",
            "category": "Category",
            "tags": "Tags",
            "upload": "Upload",
            "progress": "Progress",
        }
        # this is display name of a column

        self._disable_edit = [
            "icon_path",
            "preview_folder",
            "uuid",
            "asset_folder",
            "asset_path",
        ]
        self._show_checkbox_column = "upload"
        self._hidden_column = ["json_path"]
        self._uuids = dict()  # check multiple uuid
        self._stat = dict()
        self._assets_progress = dict()  # 上傳進度值

        self.bs_wrong_uuid = QBrush(QColor(255, 204, 204, 235))
        self.bs_wrong_uuid.setStyle(Qt.BrushStyle.BDiagPattern)
        self._icon_wrong = QBrush(QColor(252, 119, 3, 235))
        self._icon_wrong.setStyle(Qt.BrushStyle.BDiagPattern)

    def rowCount(self, idx=QModelIndex()):
        num = len(self.assets)
        return num

    def columnCount(self, idx=QModelIndex()):
        return 10

    #         num = len(self._base_header)
    #         return num

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            try:
                key = self._base_header[section]
                header_name = self._header_map.get(key, key)  # 轉換成顯示名稱
                return header_name
            except IndexError:
                return ""

        elif orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            num = str(section + 1)
            return num

    def data(self, idx:QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not idx.isValid():
            return

        row = idx.row()
        col = idx.column()
        key = self._base_header[col]
        ast = self.assets[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if key == self._show_checkbox_column:
                return
                # 如果這欄要顯示 checkbox, 那就不管 DisplayRole 了
            elif key == "icon_path":
                return
            elif key == "progress":
                try:
                    return self._assets_progress[ast["json_path"]]
                except KeyError:
                    print("%s\n not in list" % (ast["json_path"]))
                    return 0
            elif key == "tags":
                tags = ast[key]
                return ",".join(tags)
            elif key in ast.keys():
                return ast[key]
            else:
                return

        if role == Qt.ItemDataRole.DecorationRole:
            if key == "icon_path":
                icon_path = ast.get(key, None)
                if icon_path:
                    return QIcon(ast[key])
                else:
                    return
            else:
                return

        if role == Qt.ItemDataRole.CheckStateRole:
            if key == self._show_checkbox_column:
                return ast[key]
            else:
                return

        if role == Qt.EditRole:
            return self.data(idx, Qt.ItemDataRole.DisplayRole)

        if role == Qt.ItemDataRole.BackgroundRole:
            if "uuid" not in ast.keys():
                return
            uuid = ast["uuid"]
            if not uuid:
                return

            if len(self._uuids[uuid]) >= 2:
                return self.bs_wrong_uuid

            for stat in self._stat.keys():
                if ast["json_path"] in self._stat[stat]:
                    return self._icon_wrong
            return

        if role == Qt.ItemDataRole.FontRole:
            return QFont("微軟正黑體", 11)

        if role == AssetRole:
            return ast

    def flags(self, idx):
        if not idx.isValid():
            return

        original_flags = super(UploadModel, self).flags(idx)
        col = idx.column()
        key = self._base_header[col]
        if key == "upload":
            return (
                original_flags
                | Qt.ItemIsUserCheckable
                | Qt.ItemIsEnabled
                | Qt.ItemIsSelectable
            )
        if key in self._disable_edit:
            return original_flags
        else:
            return (
                original_flags
                | Qt.ItemIsEditable
                | Qt.ItemIsEnabled
                | Qt.ItemIsSelectable
            )

    def setData(self, idx, value, role=Qt.ItemDataRole.EditRole):
        if not idx.isValid():
            return

        row = idx.row()
        col = idx.column()
        key = self._base_header[col]
        ast = self.assets[row]
        if key == "progress":
            old = self._assets_progress[ast["json_path"]]
        else:
            old = ast[key]

        if key == "tags":
            value = value.split(",")
        ast[key] = value

        upload_val = ast["upload"]
        del ast["upload"]
        # 拿掉不需要寫入檔案的，保留值，準備寫完之後加回去

        if key == "progress":
            self._assets_progress[ast["json_path"]] = int(value)
            ast["upload"] = upload_val
            self.dataChanged.emit(idx, idx)
            return True
        # 上傳的部份是以一個用 json_path 為鍵值的字典來保存的

        if key == "icon_path":
            ast[key] = value

        with open(ast["json_path"], "r", encoding="utf-8") as fp:
            org_file_content = fp.read()
        update_fail = False
        try:
            with open(ast["json_path"], "w", encoding="utf-8") as fp:
                content = json.dumps(ast, indent=4, ensure_ascii=False)
                fp.write(content)
        except Exception as e:
            print(e)
            ast[key] = old
            ast["upload"] = upload_val
            update_fail = True

        if update_fail:
            try:
                with open(ast["json_path"], "w", encoding="utf-8") as fp:
                    fp.write(org_file_content)
            except Exception as e:
                raise RuntimeError(
                    "update data failed and restore data fialed, data is lost\nPath:{}".format(
                        ast["json_path"]
                    )
                ) from e

        ast["upload"] = upload_val
        self.dataChanged.emit(idx, idx)
        return True

    def appendAssets(self, json_paths):
        for json_path in json_paths:
            self.appendAsset(json_path)

    def appendAsset(self, json_path, stat=None):
        assert json_path
        if stat:
            if stat in self._stat.keys():
                self._stat[stat].append(json_path)
            else:
                self._stat[stat] = [json_path]
        # 登錄異常狀態

        with open(json_path, encoding="utf-8") as fp:
            asset = json.load(fp)
        cols = asset.keys()
        asset["upload"] = Qt.CheckState.Checked
        asset["json_path"] = json_path

        ext_cols = [col for col in cols if col not in self._base_header]
        for col in self._hidden_column:
            try:
                idx = ext_cols.index(col)
                ext_cols.pop(idx)
            except ValueError:
                pass
        # 確認是否有多出來的欄

        if ext_cols:
            self._base_header.extend(ext_cols)

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.assets.append(asset)

        if self._check_repeat_uuid(asset):
            asts = self._uuids[asset["uuid"]]
            last_ast = asts[len(asts) - 2]
            last_ast["upload"] = Qt.CheckState.Unchecked
            asset["upload"] = Qt.CheckState.Unchecked
        # 檢查是否有重覆的 uuid, 有的話把最後的跟之前的

        self._assets_progress[json_path] = 0
        # 加入進度字典

        self.endInsertRows()

    def _check_repeat_uuid(self, asset):
        uuid = asset["uuid"] if "uuid" in asset.keys() else ""
        if not uuid:
            return
        if uuid in self._uuids.keys():
            self._uuids[uuid].append(asset)
            return True
        else:
            self._uuids[uuid] = [asset]
            return False

    def clearAssets(self):
        self.beginResetModel()
        self.assets = list()
        self._uuids = dict()
        self._stat = dict()
        self._assets_progress = dict()
        self.endResetModel()

    def setProgressbar(self, json_file, value):
        jsons = [ast["json_path"] for ast in self.assets]
        the_idx = jsons.index(json_file)
        index = self.createIndex(the_idx, 1)
        self.setData(index, value)

    def setPreview(self, json_file, preview_file):
        jsons = [ast["json_path"] for ast in self.assets]
        the_idx = jsons.index(json_file)
        index = self.createIndex(the_idx, 2)
        self.setData(index, preview_file)
