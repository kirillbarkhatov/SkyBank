from pandas import Timestamp


dict_raw = {
    "Дата операции": {
        0: "31.12.2021 16:44:00",
        1: "31.12.2021 16:42:04",
        2: "31.12.2021 16:39:04",
        3: "31.12.2021 15:44:39",
        4: "31.12.2021 01:23:42",
    },
    "Дата платежа": {0: "31.12.2021", 1: "31.12.2021", 2: "31.12.2021", 3: "31.12.2021", 4: "31.12.2021"},
    "Номер карты": {0: "*7197", 1: "*7197", 2: "*7197", 3: "*7197", 4: "*5091"},
    "Статус": {0: "OK", 1: "OK", 2: "OK", 3: "OK", 4: "OK"},
    "Сумма операции": {0: -160.89, 1: -64.0, 2: -118.12, 3: -78.05, 4: -564.0},
    "Валюта операции": {0: "RUB", 1: "RUB", 2: "RUB", 3: "RUB", 4: "RUB"},
    "Сумма платежа": {0: -160.89, 1: -64.0, 2: -118.12, 3: -78.05, 4: -564.0},
    "Валюта платежа": {0: "RUB", 1: "RUB", 2: "RUB", 3: "RUB", 4: "RUB"},
    "Кэшбэк": {0: None, 1: None, 2: None, 3: None, 4: None},
    "Категория": {
        0: "Супермаркеты",
        1: "Супермаркеты",
        2: "Супермаркеты",
        3: "Супермаркеты",
        4: "Различные товары",
    },
    "MCC": {0: 5411.0, 1: 5411.0, 2: 5411.0, 3: 5411.0, 4: 5399.0},
    "Описание": {0: "Колхоз", 1: "Колхоз", 2: "Магнит", 3: "Колхоз", 4: "Ozon.ru"},
    "Бонусы (включая кэшбэк)": {0: 3, 1: 1, 2: 2, 3: 1, 4: 5},
    "Округление на инвесткопилку": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
    "Сумма операции с округлением": {0: 160.89, 1: 64.0, 2: 118.12, 3: 78.05, 4: 564.0},
}

dict_prepared = {
    "Дата операции": {
        0: Timestamp("2021-12-31 16:44:00"),
        1: Timestamp("2021-12-31 16:42:04"),
        2: Timestamp("2021-12-31 16:39:04"),
        3: Timestamp("2021-12-31 15:44:39"),
        4: Timestamp("2021-12-31 01:23:42"),
    },
    "Дата платежа": {
        0: Timestamp("2021-12-31 00:00:00"),
        1: Timestamp("2021-12-31 00:00:00"),
        2: Timestamp("2021-12-31 00:00:00"),
        3: Timestamp("2021-12-31 00:00:00"),
        4: Timestamp("2021-12-31 00:00:00"),
    },
    "Номер карты": {0: "*7197", 1: "*7197", 2: "*7197", 3: "*7197", 4: "*5091"},
    "Статус": {0: "OK", 1: "OK", 2: "OK", 3: "OK", 4: "OK"},
    "Сумма операции": {0: -160.89, 1: -64.0, 2: -118.12, 3: -78.05, 4: -564.0},
    "Валюта операции": {0: "RUB", 1: "RUB", 2: "RUB", 3: "RUB", 4: "RUB"},
    "Сумма платежа": {0: -160.89, 1: -64.0, 2: -118.12, 3: -78.05, 4: -564.0},
    "Валюта платежа": {0: "RUB", 1: "RUB", 2: "RUB", 3: "RUB", 4: "RUB"},
    "Кэшбэк": {0: None, 1: None, 2: None, 3: None, 4: None},
    "Категория": {
        0: "Супермаркеты",
        1: "Супермаркеты",
        2: "Супермаркеты",
        3: "Супермаркеты",
        4: "Различные товары",
    },
    "MCC": {0: 5411.0, 1: 5411.0, 2: 5411.0, 3: 5411.0, 4: 5399.0},
    "Описание": {0: "Колхоз", 1: "Колхоз", 2: "Магнит", 3: "Колхоз", 4: "Ozon.ru"},
    "Бонусы (включая кэшбэк)": {0: 3, 1: 1, 2: 2, 3: 1, 4: 5},
    "Округление на инвесткопилку": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
    "Сумма операции с округлением": {0: 160.89, 1: 64.0, 2: 118.12, 3: 78.05, 4: 564.0},
}


top_five_transactions = [
    {"date": "31.12.2021", "amount": -64.0, "category": "Супермаркеты", "description": "Колхоз"},
    {"date": "31.12.2021", "amount": -78.05, "category": "Супермаркеты", "description": "Колхоз"},
    {"date": "31.12.2021", "amount": -118.12, "category": "Супермаркеты", "description": "Магнит"},
    {"date": "31.12.2021", "amount": -160.89, "category": "Супермаркеты", "description": "Колхоз"},
    {"date": "31.12.2021", "amount": -564.0, "category": "Различные товары", "description": "Ozon.ru"},
]
