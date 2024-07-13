import json
import logging
import pandas as pd
import numpy as np
import datetime as dt


from src.utils import get_transactions_from_xls, date_converter, get_user_settings
from src.external_api import currency_rate, stocks_rate

# Настройки логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_current_month_data(transactions: pd.DataFrame, date: str) -> pd.DataFrame:
    """Возвращает данные за текущий месяц. Если дата — 20.05.2020,
    то данные для анализа будут в диапазоне 01.05.2020-20.05.2020
    """

    logger.info(f"Функция get_transactions_from_xls вызвана с датой {date}")
    end_date = date_converter(date)
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)
    start_date = end_date.replace(day=1)
    month_transactions = transactions.loc[(transactions['Дата операции'] <= end_date) & (transactions['Дата операции'] >= start_date)]
    return month_transactions


def filtered_card_data(transactions: pd.DataFrame) -> list[dict]:
    """ Возвращает сумму операций и кешбека по картам """

    # Доделать конвертацию в дату операции - не факт, что нужно. Сумма платежа вроде должна помогать, но есть CNY
    # currency_list = list(set(df["Валюта операции"].to_list()))
    # if len(currency_list) > 1 or "RUB" not in currency_list:
    #     currency_rate_list = currency_rate(currency_list)
    #     print(currency_rate_list)

    logger.info(f"Функция filtered_card_data вызвана")
    card_data = transactions.groupby(by="Номер карты").agg("Сумма платежа").sum().to_dict()
    output_data = []
    for card_number, total_spent in card_data.items():
        output_data.append({
            "last_digits": card_number,
            "total_spent": total_spent,
            "cashback": round(total_spent / 100, 2)
        }
        )

    return output_data


def filtered_top_five_transactions(transactions: pd.DataFrame) -> list[dict]:
    """ Возвращает топ-5 транзакций по сумме платежа"""

    logger.info(f"Функция filtered_top_five_transactions вызвана")
    top_five_transactions = transactions.sort_values(by="Сумма платежа", ascending=False).iloc[:5].to_dict(orient="records")
    top_transactions = []
    for transaction in top_five_transactions:
        top_transactions.append(
            {
      "date": transaction["Дата операции"].date().strftime("%d.%m.%Y"),
      "amount": transaction["Сумма платежа"],
      "category": transaction["Категория"],
      "description": transaction["Описание"]
    }
        )
    return top_transactions


def get_greeting() -> str:
    """ Возвращает приветствие в зависимости от времени суток"""

    logger.info(f"Функция get_greeting вызвана")
    hour = dt.datetime.now().hour
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

    logger.info(f"Функция get_main_page_data вызвана с параметрами {date_time}, {user_currencies}, {user_stocks}, {file_path}")
    greeting = get_greeting()
    transactions = get_transactions_from_xls(file_path)
    transactions = get_current_month_data(transactions, date_time)
    cards_data = filtered_card_data(transactions)
    top_transactions = filtered_top_five_transactions(transactions)
    # currencies = currency_rate(user_currencies)
    # stocks = stocks_rate(user_stocks)

    output_json = json.dumps(
        {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            # "currency_rates": currencies,
            # "stock_prices": stocks
        },
        indent=4,
        ensure_ascii=False
    )

    return output_json
