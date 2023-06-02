import datetime

import pandas


class Payments:
    def __init__(self):
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year

    def __get_data(self, filename):
        return pandas.read_excel(f"{filename}.xls")

    def get_debt_by_apartment_id(self, apartment_id, year=None):
        data = self.__get_data(year)
        fee_size = int(eval(open(f'settings.txt', 'r').read())['fee'])
        total_paid = data.loc[apartment_id - 1][1:].transpose().sum()
        need_to_be_paid = fee_size * self.current_month
        print(total_paid, need_to_be_paid)
        return True if total_paid - need_to_be_paid > -(fee_size * 3) else False

