import os
from django.conf import settings
from django.core.files.storage import get_storage_class, FileSystemStorage
from django.utils._os import abspathu
from django.utils.functional import LazyObject

__all__ = ('SecureFileSystemStorage', 'SecureStorage', 'secure_storage')


class SecureFileSystemStorage(FileSystemStorage):
    def __init__(self, file_permissions_mode=None, directory_permissions_mode=None):
        location = os.path.join(settings.BASE_DIR, 'private')
        base_url = '/private-uploads/'
        self.base_location = location
        self.location = abspathu(self.base_location)
        if base_url is None:
            base_url = ''
        elif not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.file_permissions_mode = (
            file_permissions_mode if file_permissions_mode is not None
            else settings.FILE_UPLOAD_PERMISSIONS
        )
        self.directory_permissions_mode = (
            directory_permissions_mode if directory_permissions_mode is not None
            else settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS
        )


class SecureStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(import_path='app.files.SecureFileSystemStorage')()


secure_storage = SecureStorage()
