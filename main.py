import datetime as dt

import pandas as pd

from src.reports import spending_by_category
from src.services import get_cashback_by_category
from src.utils import get_transactions_from_xls, get_user_settings
from src.views import get_main_page_data


def main_page() -> pd.DataFrame | str:
    """Приветствие пользователя на главной странице"""

    user_currencies, user_stocks = get_user_settings()
    print(
        f"""Здравствуйте!
    Ваши настройки:
    Курсы валют: {user_currencies}
    Курсы акций: {user_stocks}
    Путь к файлу с транзакциями по умолчанию: "data/operations.xls"
    Сегодняшняя дата: 31.12.2021
    """
    )

    path_to_file = input("Введите путь к файлу с транзакциями или ничего не вводи, чтобы оставить путь по умолчанию: ")
    if path_to_file == "":
        transactions = get_transactions_from_xls()

    else:
        transactions = get_transactions_from_xls(path_to_file)

    if not isinstance(transactions, pd.DataFrame):
        return "Список транзакций не был получен"

    print("Главная страница:\n")
    print(get_main_page_data(transactions, "31.12.2021", user_currencies, user_stocks))

    return transactions


def user_func(transactions: pd.DataFrame) -> None:
    """Доступ к пользовательским возможностям"""

    print(
        """Вам доступны следующие функции:
    1. Наиболее выгодные категории для кэшбека за выбранный месяц
    2. Выгрузка трат по выбранной категории за три месяца
        """
    )

    user_choice = input("Выберите функцию (введите её номер): ")

    match user_choice:
        case "1":
            while True:
                try:
                    year = int(input("Введите год: "))
                    if 2000 <= year <= dt.datetime.now().year:
                        break
                    print("Введите корректный год")
                except (TypeError, ValueError):
                    print("Введите корректный год")
            while True:
                try:
                    month = int(input("Введите месяц: "))
                    if 1 <= month <= 12:
                        break
                    print("Введите корректный месяц")
                except (TypeError, ValueError):
                    print("Введите корректный месяц")

            print("Наиболее выгодные категории")
            print(get_cashback_by_category(transactions, year, month))

        case "2":
            while True:
                try:
                    category = input("Введите категорию: ")
                    date = input("Введите дату в формате ДД.ММ.ГГГГ или пропустите ввод для принятия текущей даты: ")
                    if date == "":
                        date = "31.12.2021"
                    dt.datetime.strptime(date, "%d.%m.%Y")
                    spending_by_category(transactions, category, date)

                    print("Данные сохранены в файл reports/spending_by_category.xlsx")
                    break
                except Exception:
                    print("Введите корректные данные")

        case _:
            print("\nОШИБКА ВВОДА! Укажите число 1 или 2")
            user_func(transactions)


if __name__ == "__main__":
    tr = main_page()
    if isinstance(tr, pd.DataFrame):
        user_func(tr)
