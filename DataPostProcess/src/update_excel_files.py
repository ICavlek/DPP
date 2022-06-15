from csv_handler.csv_handler import get_dataframe_from_csv_file
from .csv_to_excel_formatter.csv_to_excel_formatter import get_dfs_split_by_year_month
from .excel_handler.excel_handler import get_excel_handler
from .errors.errors import BaseError

from ..test.test_main import Test1


def update_excel_files(file_name, format_file, target_folder):
    print("Reading content from csv file...")
    df = get_dataframe_from_csv_file(file_name, format_file=format_file)
    print("Preparing data for excel...")
    dfs_year_month = get_dfs_split_by_year_month(df)
    print("Updating excel sheets...")
    excel_handler = get_excel_handler(target_folder)
    for df_year_month in dfs_year_month:
        excel_handler.update_excel(df_year_month)
    print("Application successfully finished!")


if __name__ == '__main__':
    file_name = "Trade_Report_SP500.csv"
    format_file = False
    target_folder = "ExcelReports"
    try:
        update_excel_files(file_name, format_file, target_folder)
    except BaseError as e:
        print(e)
