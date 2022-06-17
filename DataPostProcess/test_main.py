import unittest
import os
import shutil
import pandas as pd

from src.update_excel_files import update_excel_files


class ExcelTable:
    def __init__(self, test, year):
        self._excl_path = f'./test_resources/{test}/out_excel_result/TradeReportSP500_{year}.xlsx'
        self._excl_orig_path = f'./test_resources/{test}/out_excel_result/TradeReportSP500_{year}_Orig.xlsx'
        self._excl_reference_path = f'./test_resources/{test}/out_excel_reference/TradeReportSP500_{year}.xlsx'

    def prepare_excel_file(self):
        if os.path.exists(self._excl_path):
            os.remove(self._excl_path)
        shutil.copy(self._excl_orig_path, self._excl_path)

    def is_equal_as_reference(self, month):
        df = pd.read_excel(self._excl_path, sheet_name=month)
        df_reference = pd.read_excel(self._excl_reference_path, sheet_name=month)
        return df.equals(df_reference)


class Test1:
    def __init__(self):
        self._excl_2021 = ExcelTable('test_01', 2021)
        self._excl_2022 = ExcelTable('test_01', 2022)

    def setup(self):
        self._prepare_excel_files()
        update_excel_files(
            file_name='test_resources/test_01/in_csv/Trade_Report_SP500.csv',
            format_file=False,
            target_folder='test_resources/test_01/out_excel_result'
        )

    def _prepare_excel_files(self):
        self._excl_2021.prepare_excel_file()
        self._excl_2022.prepare_excel_file()

    def is_true(self):
        return self._excl_2021.is_equal_as_reference('Dec') and self._excl_2022.is_equal_as_reference('Jan') and \
               self._excl_2022.is_equal_as_reference('Feb') and self._excl_2022.is_equal_as_reference('Mar') and \
               self._excl_2022.is_equal_as_reference('Apr') and self._excl_2022.is_equal_as_reference('May')


class Test2:
    def __init__(self):
        self._excl_2022 = ExcelTable('test_02', 2022)

    def setup(self):
        self._prepare_excel_files()
        update_excel_files(
            file_name='test_resources/test_02/in_csv/Trade_Report_SP500.csv',
            format_file=False,
            target_folder='test_resources/test_02/out_excel_result'
        )

    def _prepare_excel_files(self):
        self._excl_2022.prepare_excel_file()

    def is_true(self):
        return self._excl_2022.is_equal_as_reference('May') and self._excl_2022.is_equal_as_reference('Jun')


class TestExcelIsEqual(unittest.TestCase):
    def setUp(self) -> None:
        self._test1 = Test1()
        self._test1.setup()
        self._test2 = Test2()
        self._test2.setup()

    def test1_is_true(self):
        self.assertTrue(self._test1.is_true())

    def test2_is_true(self):
        self.assertTrue(self._test2.is_true())


if __name__ == '__main__':
    unittest.main()
