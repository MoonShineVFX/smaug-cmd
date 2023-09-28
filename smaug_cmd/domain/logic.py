import os
from PySide6.QtCore import QObject, Slot
from smaug_cmd.domain.fs import TaskGroup
from smaug_cmd.domain.smaug_types import Asset


class UploadHandler(QObject):
    def __init__(self, ui_widget):
        self._ui = ui_widget
        self.__is_uploading = False

    def to_asset_dict(self, asset_folder):
        """generate asset dict from asset folder

        Args:
            asset_folder(str):  asset folder
        """
        # 轉成 asset template 格式
        # 處理應該泛生出來的壓縮檔
        # 轉成 smaug asset dict 格式
        asset_dict: Asset = {}
    

    # ---------------------------------------------------------------
    @Slot(str)
    def traverse_asset_folder(self, assets_folder):
        traverse_thread = threading.Thread(
            target=self.__traverse, kwargs={"assets_folder": assets_folder}
        )
        traverse_thread.start()

    def __traverse(self, **kwargs):
        self._ui.toggle_busy(True)
        assets_folder = kwargs["assets_folder"]

        def json_files():
            for folder, _, files in os.walk(assets_folder):
                for f in files:
                    if f.lower() == "galaxy.json":
                        yield os.path.join(folder, f)

        error_msg = ""
        line_count = 0
        for json_path in json_files():
            try:
                stat = update_json_file(json_path)
                self._ui.append_asset(json_path, stat=stat)
            except Exception as e:
                print("Exception: {} @ {}".format(e, json_path))
                error_msg += json_path + "\n"
                line_count += 1
        if error_msg:
            if line_count == 1:
                error_msg += "格式有誤"
            else:
                error_msg += "等檔案格式有誤"
            msg_box = QMessageBox(QMessageBox.Warning, "JSON檔案錯誤", error_msg)
            msg_box.exec_()
        self._ui.toggle_busy(False)

    def compose_task_groups(self, assets_info):
        for json_path, asset, fbx_path, preview_folder in assets_info:
            engname = os.path.splitext(os.path.basename(fbx_path))[0]
            fbx_path = fbx_path.replace("/", "\\")
            fbx_folder = os.path.dirname(fbx_path)

            # KeepAliveTask
            keep_alive_task_ = GXKeepAliveTask(scale=0.0, offset=0)

            # UploadPreviewTask
            preview_paths = [
                os.path.join(preview_folder, f)
                for f in os.listdir(preview_folder)
                if f.lower().startswith("large")
            ]
            upload_preview_task_ = GXUploadPreviewTask(
                asset, preview_paths, scale=0.01, offset=0
            )

            # CompressTask
            texture_folder = os.path.join(fbx_folder, "Texture")
            texture_paths = []
            for t in os.listdir(texture_folder):
                if t.lower().endswith("jpg"):
                    texture_paths.append(os.path.join(texture_folder, t))
                elif t.lower().endswith("png"):
                    texture_paths.append(os.path.join(texture_folder, t))
            input_files = texture_paths
            input_files.append(fbx_path)
            # input_files = [p.replace(fbx_folder, '.') for p in input_files]
            compressed_file = "%s\\%s.gz" % (fbx_folder, engname)
            compress_task_ = GXCompressTask(
                input_files, fbx_folder, compressed_file, engname, scale=0.49, offset=1
            )

            # UploadTask
            upload_task_ = GXUploadTask(asset, compressed_file, scale=0.5, offset=50)

            # CleanUpGask
            files_to_be_removed = [compressed_file]
            clean_up_task_ = GXCleanUpTask(files_to_be_removed)
            task_group = TaskGroup()
            task_group.append_task(keep_alive_task_)
            task_group.append_task(upload_preview_task_)
            task_group.append_task(compress_task_)
            task_group.append_task(upload_task_)
            task_group.append_task(clean_up_task_)
            yield json_path, task_group

    @Slot(list)
    def batch_upload(self, json_paths):
        if self.__is_uploading:
            return
        self.__is_uploading = True
        assets_to_upload = collect_assets_info(json_paths)

        self.__groups_to_json_paths = {}
        for json_path, task_group in self.compose_task_groups(assets_to_upload):
            self.__groups_to_json_paths[task_group] = json_path
            task_runner().append_task_group(task_group)

        task_runner().set_report_cb(self.report_progresses)
        task_runner().set_complete_cb(self.on_task_complete)
        task_runner().run()

    def report_progresses(self, task_status):
        for group, task_name, progress in task_status:
            json_path = self.__groups_to_json_paths[group]
            self._ui.handle_progress1(json_path, progress)

    def on_task_complete(self, task_group):
        json_path = self.__groups_to_json_paths[task_group]
        self._ui.handle_progress1(json_path, 100)

    def on_all_task_complete(self):
        self.__is_uploading = False
        self._ui.showText("序列上傳完畢！", title="序列上傳", modal=True)

    #         qbox = QMessageBox(QMessageBox.Information, u'序列上傳',
    #                 u'序列上傳完畢！')
    #         main_thread = QApplication.instance().thread()
    #         if qbox.thread() != main_thread:
    #             qbox.moveToThread(main_thread)
    #         qbox.exec_()

    def gen_update_thumbnail(self, key, source_file):
        """generate and update row data icon from large picture

        Args:
            key(str): json file path, treat as a key to find specify row
            source_file(str): the file use to genrate small picture.
        """
        folder_name = os.path.dirname(source_file)
        thumb_target = os.path.join(folder_name, "Small.jpg")
        misc.gen_thumbnail(source_file, thumb_target)
        self._ui.set_preview(key, thumb_target)
        return True
