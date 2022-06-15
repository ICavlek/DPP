from src.csv_handler.csv_handler import get_dataframe_from_csv_file
from src.csv_to_excel_formatter.csv_to_excel_formatter import get_dfs_split_by_year_month
from src.excel_handler.excel_handler import get_excel_handler
from src.errors.errors import BaseError


def main(file_name, format_file, template_path, target_folder):
    print("Reading content from csv file...")
    df = get_dataframe_from_csv_file(file_name, format_file=format_file)
    print("Preparing data for excel...")
    dfs_year_month = get_dfs_split_by_year_month(df)
    print("Updating excel sheets...")
    excel_handler = get_excel_handler(template_path, target_folder)
    for df_year_month in dfs_year_month:
        excel_handler.update_excel(df_year_month)
    print("Application successfully finished!")


if __name__ == '__main__':
    file_name = "Trade_Report_SP500.csv"
    format_file = True
    template_path = "DataPostProcess/resources/TradeReportSP500_Template.xlsx"
    target_folder = "ExcelReports"
    try:
        main(file_name, format_file, template_path, target_folder)
    except BaseError as e:
        print(e)
