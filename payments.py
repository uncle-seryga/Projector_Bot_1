import datetime

import pandas as pd

import db_controller


class Payments:
    def __init__(self):
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        self.df = self.__get_data()
        self.rate = self.__get_rates()['PRICE'][0]
        self.debt = self.__get_rates()['PRICE'][1]

    @staticmethod
    def __get_data():
        sheet_id = '1PnMkGXh-VC6IyOzr56C38wvv_AVtGQZG1I5dMnhabuU'
        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'
        df = pd.read_csv(url)
        return df

    @staticmethod
    def __get_rates():
        df = pd.read_excel("rates.xls")
        return df

    def get_if_debt(self, tel_id):
        first_column = self.df.iloc[1:, 0]
        rest = self.df.iloc[1:, 4:16]
        data_frame = pd.concat([first_column, rest], axis=1)
        data_frame.columns = ['apartment', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                              'September', 'October', 'November', 'December']
        mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']
        code = db_controller.Residents().select(['apartment_code'], key_word="tel_id", value=tel_id)
        data_frame[mon] = data_frame[mon].apply(pd.to_numeric, errors='coerce')
        formula = lambda row: row.count() * self.rate - row.sum()
        data_frame['Paid'] = data_frame[mon].apply(formula, axis=1)
        target = data_frame[data_frame['apartment'] == code]
        res = data_frame.loc[target.index.values[0]]["Paid"]
        print(f"{res}<{self.debt}")
        return True if res < self.debt else False
