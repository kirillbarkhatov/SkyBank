import pandas as pd
from src.utils import get_transactions_from_xls, date_converter

import datetime as dt
import numpy as np

def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: str = None) -> pd.DataFrame:
    """ Функция возвращает траты по заданной категории за последние три месяца (от переданной даты) """

    if date is None:
        end_date = dt.datetime.now()
    else:
        end_date = dt.datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date.replace(month=((end_date.month + 8) % 12 + 1), hour=0, minute=0, second=0, microsecond=0)
    print(end_date, start_date)
    # start_date = date64.astype('M8[M]') - np.timedelta64(3, 'M')
    # start_date = start_date.astype('M8[D]') + np.timedelta64(date64.day(), 'D')
    # print(date64.astype('M8[M]'))
    transactions_by_category = transactions.loc[(transactions['Дата операции'] <= end_date) & (transactions['Дата операции'] >= start_date) & (transactions['Категория'] == category)]
    print(df)






if __name__ == "__main__":
    df = get_transactions_from_xls()
    spending_by_category(df,"Аптеки", "01.04.2020")