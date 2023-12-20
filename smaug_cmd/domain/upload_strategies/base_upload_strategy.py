from abc import ABC, abstractmethod


class BaseUploadStrategy(ABC):

    @abstractmethod
    def upload_previews(self, asset_template, upload_user):
        pass

    @abstractmethod
    def upload_renders(self, asset_template,upload_user):
        pass

    @abstractmethod
    def upload_textures(self, asset_template, upload_user):
        pass

    @abstractmethod
    def upload_models(self, asset_template, upload_user):
        pass

    @abstractmethod
    def upload_3d_preview(self, asset_template, upload_user):
        pass
