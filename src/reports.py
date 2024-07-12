import pandas as pd
from src.utils import get_transactions_from_xls, date_converter

import datetime as dt
import numpy as np


from functools import wraps
from typing import Any, Callable


def save_report(filename: str | None = None) -> Callable:
    """ Декоратор для записи отчета в файл """

    def wrapper(func: Callable) -> Callable:

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if filename is None:
                filename_to_save = func.__name__
            else:
                filename_to_save = filename
            result = func(*args, **kwargs)
            result.to_excel(f"reports/{filename_to_save}.xlsx")
            print(result)
        return inner

    return wrapper


@save_report()
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
    print(transactions)
    transactions_by_category = transactions.loc[(transactions['Дата операции'] <= end_date) & (transactions['Дата операции'] >= start_date) & (transactions['Категория'] == category)]
    return transactions_by_category






if __name__ == "__main__":
    df = get_transactions_from_xls()
    spending_by_category(df,"Аптеки", "01.04.2020")