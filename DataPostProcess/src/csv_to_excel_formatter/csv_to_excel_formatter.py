from dateutil import parser
import numpy as np

def get_dfs_split_by_year_month(df):
    dfs_year_month = DFSYearMonth(df)
    dfs_year_month.instantiate()
    dfs_year_month.split_dfs_by_year()
    dfs_year_month.split_dfs_by_month()
    return dfs_year_month


class DFSYearMonth:
    MONTHS = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    def __init__(self, df):
        self._df = df
        self._dfs_split = dict()

    def __iter__(self):
        for year in self._dfs_split.keys():
            for month in self._dfs_split[year].keys():
                yield self._dfs_split[year][month]

    def instantiate(self):
        self._add_header()
        self._add_years_column()
        self._add_months_column()

    def _add_header(self):
        self._df.set_axis(
            ["Date", "Type", "Successful", "Open", "S/L",
             "Volume", "Profit", "Swap", "Balance"],
            axis=1,
            inplace=True
        )

    def _add_years_column(self):
        all_years = [parser.parse(date).year for date in self._df["Date"]]
        self._df.insert(len(self._df.columns), "Year", all_years)

    def _add_months_column(self):
        all_months = [
            self.MONTHS[parser.parse(date).month-1]
            for date in self._df["Date"]
        ]
        self._df.insert(len(self._df.columns), "Month", all_months)

    def split_dfs_by_year(self):
        unique_years = self._df["Year"].unique()
        for year in unique_years:
            self._dfs_split[year] = dict()

    def split_dfs_by_month(self):
        START_INDEX = 5
        for year in self._dfs_split.keys():
            df_year = self._df.loc[self._df["Year"] == year]
            for month in self.MONTHS:
                df_year_month = df_year.loc[df_year["Month"] == month]
                if df_year_month.empty:
                    continue
                self._dfs_split[year][month] = df_year_month
                self._dfs_split[year][month].index = np.arange(
                    START_INDEX, len(self._dfs_split[year][month]) + START_INDEX
                )


    @property
    def years(self):
        for year in self._dfs_split.keys():
            yield year
