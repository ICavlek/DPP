from src import update_excel_files, CsvHandlerBaseError


if __name__ == '__main__':
    file_name = "D:\\Demo\\TradeReport\\Trade_Report_GBPUSD.csv"
    format_file = False
    target_folder = "D:\\Demo\\ExcelReports"
    try:
        update_excel_files(file_name, format_file, target_folder)
    except CsvHandlerBaseError as e:
        print(e)
