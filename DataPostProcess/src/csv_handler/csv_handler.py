import pandas as pd
import os

from .errors import FileMissingError


def get_csv_handler(file_name):
    return CSVHandler(file_name)


class CSVHandler:
    def __init__(self, file_path, include_header=None):
        self._file_path = file_path
        self._include_header = include_header

    def get_data(self):
        if os.path.exists(self._file_path):
            return pd.read_csv(self._file_path, header=self._include_header)
        raise FileMissingError(self._file_path)

    def format_file(self):
        open(self._file_path, "w+").close()