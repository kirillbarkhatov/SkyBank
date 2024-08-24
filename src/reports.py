import datetime
import datetime as dt
import logging
from functools import wraps
from typing import Any, Callable

import pandas as pd

from src.utils import date_converter, get_transactions_from_xls

# Настройки логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def save_report(filename: str | None = None) -> Callable:
    """Декоратор для записи отчета в файл"""

    def wrapper(func: Callable) -> Callable:

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if filename is None:
                filename_to_save = func.__name__
            else:
                filename_to_save = filename
            result = func(*args, **kwargs)
            result.to_excel(f"reports/{filename_to_save}.xlsx")
            logger.info(f"Применен декоратор save_report - данные записаны в {filename_to_save}")

        return inner

    return wrapper


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    logger.info(f"Запущено формирование отчета spending_by_category с параметрами {category}, {date}")
    if date is None:
        end_date = dt.datetime.now()
    else:
        end_date = date_converter(date)
    start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=91)
    transactions_by_category = transactions.loc[
        (transactions["Дата операции"] <= end_date)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Категория"] == category)
    ]
    logger.info(f"Отчет сформирован с параметрами {category}, {start_date}, {end_date}")
    return transactions_by_category


if __name__ == "__main__":
    df = get_transactions_from_xls()
    spending_by_category(get_transactions_from_xls(), "Аптеки", "01.04.2020")
