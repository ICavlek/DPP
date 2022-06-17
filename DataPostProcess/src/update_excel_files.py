from .csv_handler.csv_handler import get_csv_handler
from .csv_to_excel_formatter.csv_to_excel_formatter import get_dfs_split_by_year_month
from .excel_handler.excel_handler import get_excel_handler


def update_excel_files(file_name, format_file, target_folder):
    print("Reading content from csv file...")
    csv_handler = get_csv_handler(file_name)
    df = csv_handler.get_data()
    print("Preparing data for excel...")
    dfs_year_month = get_dfs_split_by_year_month(df)
    print("Updating excel sheets...")
    excel_handler = get_excel_handler(target_folder)
    for df_year_month in dfs_year_month:
        excel_handler.update_excel(df_year_month)
    if format_file:
        print("Formatting file...")
        csv_handler.format_file()
    print("Application successfully finished!")
