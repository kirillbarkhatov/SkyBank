import json

import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path

from src.utils import get_transactions_from_xls, date_converter, get_user_settings
from src.external_api import currency_rate, stocks_rate



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
    output_data = []
    for card_number, total_spent in df.items():
        output_data.append({
            "last_digits": card_number,
            "total_spent": total_spent,
            "cashback": round(total_spent / 100, 2)
        }
        )

    return output_data


def filtered_top_five_transactions(df: pd.DataFrame) -> list[dict]:
    """ Возвращает топ-5 транзакций по сумме платежа"""

    df = df.sort_values(by="Сумма платежа", ascending=False).iloc[:5].to_dict(orient="records")
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


def get_main_page_data(date_time: str, user_currencies: list, user_stocks: list, file_path: str = "data/operations.xls") -> str:
    """ Функция, для страницы Главная, возвращающая приветствие, данные по картам за этот месяц,
    топ 5 операций за месяц, курсы валют и акций
    """

    greeting = get_greeting(date_time)
    transactions = get_transactions_from_xls(file_path)
    cards_data = filtered_card_data(transactions)
    top_transactions = filtered_top_five_transactions(transactions)
    currencies = currency_rate(user_currencies)
    stocks = stocks_rate(user_stocks)

    output_json = json.dumps(
        {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currency_rates": currencies,
            "stock_prices": stocks
        },
        indent=4,
        ensure_ascii=False
    )

    return output_json



if __name__ in "__main__":
    # file_path = Path.cwd().parent.joinpath("data", "operations.xls")
    # # df = get_transactions_from_xls(file_path)
    # df = get_current_month_data(get_transactions_from_xls(file_path), "20.07.2020")
    # filtered_card_data(df)
    # filtered_top_five_transactions(df)
    # print(get_greeting("2021-01-20 13:00:00"))
    user_currencies, user_stocks = get_user_settings()
    print(get_main_page_data("2020-07-20 13:00:00", user_currencies, user_stocks))
