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


def filtered_card_data(df: pd.DataFrame) -> pd.DataFrame:
    """ Возвращает сумму операций и кешбека по картам """

    df = df.groupby(by="Номер карты").agg("Сумма операции").sum()
    print(df)




if __name__ in "__main__":
    file_path = Path.cwd().parent.joinpath("data", "operations.xls")
    df = get_current_month_data(get_transactions_from_xls(file_path), "20.07.2020")
    filtered_card_data(df)

