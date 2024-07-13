from src.external_api import currency_rate, stocks_rate
from src.reports import spending_by_category

from src.services import get_cashback_by_category
from src.utils import date_converter, get_transactions_from_xls, get_user_settings
from src.views import get_main_page_data, filtered_top_five_transactions, filtered_card_data
import pandas as pd
from pandas import Timestamp

def main_page() -> pd.DataFrame:
    """Приветствие пользователя на главной странице"""

    user_currencies, user_stocks = get_user_settings()
    print(f"""Здравствуйте!
    Ваши настройки:
    Курсы валют: {user_currencies}
    Курсы акций: {user_stocks}
    Путь к файлу с транзакциями по умолчанию: "data/operations.xls"
    Сегодняшняя дата: 31.12.2021
    
    """)
    path_to_file = input("Введите путь к файлу с транзакциями или ничего не вводи, чтобы оставить путь по умолчанию: ")
    if path_to_file == "":
        transactions = get_transactions_from_xls()

    else:
        transactions = get_transactions_from_xls(path_to_file)
    print("Главная страница:\n")
    print(get_main_page_data(transactions, "31.12.2021", user_currencies, user_stocks))

    return transactions


def user_func(transactions: pd.DataFrame) -> None:
    """Доступ к пользовательским возможностям"""

    print("""Вам доступны следующие функции:
    1. Наиболее выгодные категории для кэшбека за выбранный месяц
    2. Выгрузка трат по выбранной категории за три месяца
    
    """)

    user_choice = input("Выберите функцию (введите её номер): ")

    match user_choice:
            case "1":
                while True:
                    try:
                        year = int(input(""))
                    if

                month = input("")
                print("Наиболее выгодные категории")
                return get_transactions_from_json("data/operations.json")
            case "2":
                print("Программа: Для обработки выбран CSV-файл")
                return get_transactions_from_csv("data/transactions.csv")
            case "3":
                print("Программа: Для обработки выбран XLSX-файл")
                return get_transactions_from_xls("data/transactions_excel.xlsx")
            case _:
                print("\nОШИБКА ВВОДА! Укажите число 1 или 2")
                user_func(transactions)

# print(currency_rate(user_currencies))
# print(stocks_rate(user_stocks))
# spending_by_category(get_transactions_from_xls(), "Аптеки", "01.06.2020")
# # print(get_cashback_by_category(get_transactions_from_xls(), 2020, 2))

# df = pd.read_excel("data/operations.xls")
# df_dict = get_transactions_from_xls().iloc[:5].to_dict()
# print(df_dict)
# df = pd.DataFrame(
#     {
#         "Дата операции": {
#             0: Timestamp("2021-12-31 16:44:00"),
#             1: Timestamp("2021-12-31 16:42:04"),
#             2: Timestamp("2021-12-31 16:39:04"),
#             3: Timestamp("2021-12-31 15:44:39"),
#             4: Timestamp("2021-12-31 01:23:42"),
#         },
#         "Дата платежа": {
#             0: Timestamp("2021-12-31 00:00:00"),
#             1: Timestamp("2021-12-31 00:00:00"),
#             2: Timestamp("2021-12-31 00:00:00"),
#             3: Timestamp("2021-12-31 00:00:00"),
#             4: Timestamp("2021-12-31 00:00:00"),
#         },
#         "Номер карты": {0: "*7197", 1: "*7197", 2: "*7197", 3: "*7197", 4: "*5091"},
#         "Статус": {0: "OK", 1: "OK", 2: "OK", 3: "OK", 4: "OK"},
#         "Сумма операции": {0: -160.89, 1: -64.0, 2: -118.12, 3: -78.05, 4: -564.0},
#         "Валюта операции": {0: "RUB", 1: "RUB", 2: "RUB", 3: "RUB", 4: "RUB"},
#         "Сумма платежа": {0: -160.89, 1: -64.0, 2: -118.12, 3: -78.05, 4: -564.0},
#         "Валюта платежа": {0: "RUB", 1: "RUB", 2: "RUB", 3: "RUB", 4: "RUB"},
#         "Кэшбэк": {0: None, 1: None, 2: None, 3: None, 4: None},
#         "Категория": {
#             0: "Супермаркеты",
#             1: "Супермаркеты",
#             2: "Супермаркеты",
#             3: "Супермаркеты",
#             4: "Различные товары",
#         },
#         "MCC": {0: 5411.0, 1: 5411.0, 2: 5411.0, 3: 5411.0, 4: 5399.0},
#         "Описание": {0: "Колхоз", 1: "Колхоз", 2: "Магнит", 3: "Колхоз", 4: "Ozon.ru"},
#         "Бонусы (включая кэшбэк)": {0: 3, 1: 1, 2: 2, 3: 1, 4: 5},
#         "Округление на инвесткопилку": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
#         "Сумма операции с округлением": {0: 160.89, 1: 64.0, 2: 118.12, 3: 78.05, 4: 564.0},
#     }
# )
# print(spending_by_category(df, "Супермаркеты", "31.12.2021"))
