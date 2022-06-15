import unittest
import os
import shutil
from ..src.update_excel_files import update_excel_files


class Test1:
    @classmethod
    def prepare_excel_files(cls):
        Test1._prepare_excel_file(2021)
        Test1._prepare_excel_file(2022)

    @classmethod
    def _prepare_excel_file(cls, year):
        excl_orig_path = f'./resources/test_1/out_excel_result/TradeReportSP500_{year}_Orig.xlsx'
        excl_path = f'./resources/test_1/out_excel_result/TradeReportSP500_{year}.xlsx'
        if os.path.exists(excl_path):
            os.remove(excl_path)
        shutil.copy(excl_orig_path, excl_orig_path)


class TestExcelIsEqual(unittest.TestCase):
    def setUp(self) -> None:
        Test1.prepare_excel_files()

    def test_is_equal(self):
        self.assertEqual('1', '1')


if __name__ == '__main__':
    unittest.main()
