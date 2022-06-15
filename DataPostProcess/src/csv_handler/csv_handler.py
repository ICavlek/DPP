import pandas as pd
import os

from ..errors.errors import FileMissingError


def get_dataframe_from_csv_file(file_name, format_file=True):
    csv_handler = CSVHandler(file_name)
    df = csv_handler.get_data()
    if format_file:
        csv_handler.format_file()
    return df


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