import pandas as pd
from src.utils import get_transactions_from_xls, date_converter

import datetime as dt
import numpy as np

def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: str = None) -> pd.DataFrame:
    """ Функция возвращает траты по заданной категории за последние три месяца (от переданной даты) """

    date64 = date_converter(date)
    start_date = date64.astype('M8[M]') - np.timedelta64(3, 'M')
    # start_date = start_date.astype('M8[D]') + np.timedelta64(date64.day(), 'D')
    print(date64.astype('M8[M]'))
    df = df.loc[(df['Дата операции'] <= date64) & (df['Дата операции'] >= start_date)]





if __name__ == "__main__":
    df = get_transactions_from_xls()
    spending_by_category(df,"Аптеки", "01.05.2020")