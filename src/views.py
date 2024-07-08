import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path

from src.utils import get_transactions_from_xls, date_converter
from external_api import currency_rate


def get_current_month_data(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Возвращает данные за текущий месяц. Если дата — 20.05.2020,
    то данные для анализа будут в диапазоне 01.05.2020-20.05.2020
    """

    date64 = date_converter(date)
    date_day = date64.astype('M8[D]') + np.timedelta64(1, 'D')
    date_month = date64.astype('M8[M]')
    df = df.loc[(df['Дата операции'] <= date_day) & (df['Дата операции'] >= date_month)]
    return df


def filtered_card_data(df: pd.DataFrame) -> list[dict]:
    """ Возвращает сумму операций и кешбека по картам """

    # Доделать конвертацию в дату операции - не факт, что нужно. Сумма платежа вроде должна помогать, но есть CNY
    # currency_list = list(set(df["Валюта операции"].to_list()))
    # if len(currency_list) > 1 or "RUB" not in currency_list:
    #     currency_rate_list = currency_rate(currency_list)
    #     print(currency_rate_list)

    df = df.groupby(by="Номер карты").agg("Сумма платежа").sum().to_dict()
    print(df)
    output_data = []
    for card_number, total_spent in df.items():
        output_data.append({
            "last_digits": card_number,
            "total_spent": total_spent,
            "cashback": round(total_spent / 100, 2)
        }
        )

    print(output_data)
    return output_data


def filtered_top_five_transactions(df: pd.DataFrame) -> list[dict]:
    """ Возвращает топ-5 транзакций по сумме платежа"""

    df = df.sort_values(by="Сумма платежа", ascending=False).iloc[:5].to_dict(orient="records")
    print(df)
    top_transactions = []
    for transaction in df:
        top_transactions.append(
            {
      "date": transaction["Дата операции"].date().strftime("%d.%m.%Y"),
      "amount": transaction["Сумма платежа"],
      "category": transaction["Категория"],
      "description": transaction["Описание"]
    }
        )
    print(top_transactions)
    return top_transactions


def get_greeting(date_time: str) -> str:
    """ Возвращает приветствие в зависимости от времени суток"""

    hour = dt.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S").hour
    if hour >= 23 or hour < 4:
        return "Доброй ночи"
    if 4 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 16:
        return "Добрый день"
    if 16 <= hour < 23:
        return "Добрый вечер"


if __name__ in "__main__":
    file_path = Path.cwd().parent.joinpath("data", "operations.xls")
    # df = get_transactions_from_xls(file_path)
    df = get_current_month_data(get_transactions_from_xls(file_path), "20.07.2020")
    filtered_card_data(df)
    filtered_top_five_transactions(df)
    print(get_greeting("2021-01-20 13:00:00"))

