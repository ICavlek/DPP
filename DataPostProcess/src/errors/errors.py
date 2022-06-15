class BaseError(Exception):
    pass


class FileMissingError(BaseError):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name

    def __str__(self):
        return f'Cannot find specified file {self._file_name}'