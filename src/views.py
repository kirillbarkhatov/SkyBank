import pandas as pd
import numpy as np
from pathlib import Path

from src.utils import get_transactions_from_xls, date_converter


def get_current_month_data(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Возвращает данные за текущий месяц. Если дата — 20.05.2020,
    то данные для анализа будут в диапазоне 01.05.2020-20.05.2020
    """

    date64 = date_converter(date)
    date_day = date64.astype('M8[D]') + np.timedelta64(1, 'D')
    date_month = date64.astype('M8[M]')
    df = df.loc[(df['Дата операции'] <= date_day) & (df['Дата операции'] >= date_month)]
    return df





if __name__ in "__main__":
    get_current_month_data(get_transactions_from_xls(Path.cwd().parent.joinpath("data", "operations.xls")), "20.07.2020")

