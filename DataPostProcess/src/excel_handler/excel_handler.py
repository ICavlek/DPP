import os
import shutil
import pandas as pd
import openpyxl
import numpy as np
from ..errors.errors import FileMissingError


def get_excel_handler(template_path, target_folder):
    excel_handler = ExcelHandler(template_path, target_folder)
    excel_handler.instantiate()
    return excel_handler


class ExcelHandler:
    def __init__(self, template_path, target_folder):
        self._template_path = template_path
        self._target_folder = target_folder
        self._excel_files = dict()

    def instantiate(self):
        self._if_template_file_exists()
        self._if_target_folder_exists()

    def update_excel(self, df):
        START_INDEX = 5
        year = df.Year[START_INDEX]
        excel_single = self._get_excel_single(year)
        excel_single.update(df)

    def _get_excel_single(self, year):
        template_file_name = os.path.split(self._template_path)[-1]
        excel_file_name = template_file_name.replace("Template", str(year))
        excel_file_path = os.path.join(self._target_folder, excel_file_name)
        if not os.path.exists(excel_file_path):
            shutil.copy(self._template_path, excel_file_path)
        if year not in self._excel_files.keys():
            excel_single = ExcelSingle(excel_file_path, year)
            excel_single.instantiate()
            self._excel_files[year] = excel_single
        return self._excel_files[year]

    def _if_template_file_exists(self):
        if os.path.exists(self._template_path):
            return
        raise FileMissingError(self._template_path)

    def _if_target_folder_exists(self):
        if os.path.exists(self._target_folder):
            return
        os.mkdir(self._target_folder)


class ExcelSingle:
    START_ROW = 3
    START_INDEX = 5
    NUM_OF_COLUMNS = 9

    def __init__(self, file_path, year):
        self._file_path = file_path
        self._year = year
        self._excel_sheets = dict()

    def instantiate(self):
        self._instantiate_sheets()

    def update(self, df):
        month = df.Month[self.START_INDEX]
        df = self._get_standard_format(df)
        df = self._set_axis(df)
        self._excel_sheets[month].update(df)
        self._update_sheet_in_excel(month)

    def _instantiate_sheets(self):
        xls = pd.ExcelFile(self._file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(io=self._file_path, sheet_name=sheet_name)
            if sheet_name == ExcelSheetYearlyReport.NAME:
                self._excel_sheets[sheet_name] = ExcelSheetYearlyReport(sheet_name, df)
            else:
                df = self._reformat_dataframe(df)
                self._excel_sheets[sheet_name] = ExcelSheetMonth(sheet_name, df)

    def _update_sheet_in_excel(self, month):
        df = self._excel_sheets[month].data_frame
        wb = openpyxl.load_workbook(filename=self._file_path)
        month = ExcelSingle._month_to_sheet_number(month)
        for index_r, row in df.iterrows():
            for index_c, value in row.iteritems():
                wb.worksheets[month].cell(row=index_r, column=index_c).value = value
        wb.save(self._file_path)

    def _reformat_dataframe(self, df):
        df = self._get_standard_format(df)
        df = self._set_axis(df)
        if isinstance(df.iloc[self.START_ROW, 1], float):
            return None
        df = df.iloc[self.START_ROW:df.index.size, :]
        df.index = np.arange(self.START_INDEX, df.index.size + self.START_INDEX)
        df = df.dropna()
        return df

    def _get_standard_format(self, df):
        return df.iloc[:, :self.NUM_OF_COLUMNS]

    def _set_axis(self, df):
        df.set_axis(
            labels=list(range(1,self.NUM_OF_COLUMNS+1)),
            axis=1,
            inplace=True
        )
        return df

    @classmethod
    def _month_to_sheet_number(cls, month):
        month_to_num = {
            "Jan" : 0, "Feb" : 1, "Mar" : 2, "Apr" : 3, "May" : 4, "Jun" : 5,
            "Jul" : 6, "Aug" : 7, "Sep" : 8, "Oct" : 9, "Nov" : 10, "Dec" : 11
        }
        return month_to_num[month]


class ExcelSheetBase:
    START_ROW = 5

    def __init__(self, name, df):
        self._name = name
        self._df = df

    def update(self, df):
        start_row = self._get_start_row()
        self._update_df(df, start_row)

    def _get_start_row(self):
        if self._df is not None:
            return self._df.index.size + self.START_ROW
        else:
            return self.START_ROW

    def _update_df(self, df, start_row):
        if self._df is not None:
            for index, row in df.iterrows():
                self._df.loc[start_row] = row
                start_row = start_row + 1
        else:
            self._df = df

    @property
    def data_frame(self):
        return self._df


class ExcelSheetMonth(ExcelSheetBase):
    def __init__(self, month, df):
        super().__init__(month, df)


class ExcelSheetYearlyReport(ExcelSheetBase):
    NAME = "Yearly Result"

    def __init__(self, name, df):
        super().__init__(name, df)
