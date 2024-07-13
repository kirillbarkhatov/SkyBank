import pandas as pd
import pytest
from src.utils import get_transactions_from_xls, date_converter, get_user_settings
from unittest.mock import patch, mock_open
from pandas import Timestamp
import datetime


@pytest.fixture
def dict_for_pd_as_xls():
    return {
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


@pytest.fixture
def dict_for_pd_for_working():
    return {
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


# Тест на отсутствие файла для чтения
@patch("os.path.exists")
def test_get_transactions_from_xls_file_not_exist(mock_os_path_exists):
    mock_os_path_exists.return_value = False
    assert get_transactions_from_xls("test") == []


@patch("pandas.read_excel")
def test_get_transactions_from_xls(mock_read_excel, dict_for_pd_as_xls, dict_for_pd_for_working):
    m = mock_open()
    mock_read_excel.return_value = pd.DataFrame(dict_for_pd_as_xls)
    result = pd.DataFrame(dict_for_pd_for_working)
    with patch("builtins.open", m) as mocked_open:
        assert result.equals(get_transactions_from_xls("test"))
        mock_read_excel.assert_called_once_with("test")


@pytest.mark.parametrize(
    "input_date, output_date",
    [
        ("21.01.2024", datetime.datetime.strptime("21.01.2024", "%d.%m.%Y")),
        ("21.01.2024 11:11:12", datetime.datetime.strptime("21.01.2024 11:11:12", "%d.%m.%Y %H:%M:%S")),
        ("2024-01-21 11:11:12", datetime.datetime.strptime("2024-01-21 11:11:12", "%Y-%m-%d %H:%M:%S")),
        ("2024-01", datetime.datetime.strptime("2024-01", "%Y-%m"))
    ]
)
def test_date_converter(input_date, output_date):
    assert date_converter(input_date) == output_date
    with pytest.raises(Exception) as ex:
        date_converter("invalid date")
    assert str(ex.value) == "Неверный формат даты"


def test_get_user_settings():
    m = mock_open(read_data=""" 
        {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }"""
    )
    get_user_settings()
    with patch("builtins.open", m) as mocked_open:
        assert get_user_settings("test") == (["USD", "EUR"], ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
