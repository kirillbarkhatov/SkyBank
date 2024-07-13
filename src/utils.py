import json
import logging
import datetime

import pandas as pd
import numpy as np
from pathlib import Path


# Настройки логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_transactions_from_xls(file_path: str = "data/operations.xls") -> pd.DataFrame | list:
    """Функция принимает на вход путь до CSV-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл не найден, функция возвращает пустой список.
    """
    logger.info(f"Вызвана функция получения транзакций из файла {file_path}")
    try:
        transactions_df = pd.read_excel(file_path)
        transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        transactions_df["Дата платежа"] = pd.to_datetime(transactions_df["Дата платежа"], format="%d.%m.%Y")
        logger.info(f"Файл {file_path} найден, данные о транзакциях получены")
        return transactions_df

    except FileNotFoundError:
        logger.info(f"Файл {file_path} не найден")
        return []


def date_converter(date: str) -> datetime:
    """Функция конвертации даты, переданной строкой, в формат datetime"""

    logger.info(f"Вызвана функция распознавания и конвертации даты {date}")
    try:
        date_dt = datetime.datetime.strptime(date, "%d.%m.%Y")
        logger.info(f"Дата в формате %d.%m.%Y успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        logger.info(f"Дата в формате %d.%m.%Y %H:%M:%S успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        logger.info(f"Дата в формате %Y-%m-%d %H:%M:%S успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%Y-%m")
        logger.info(f"Дата в формате %Y-%m успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    logger.error("Неверный формат даты")
    raise Exception("Неверный формат даты")


def get_user_settings(path: str = "user_settings.json") -> tuple:
    """ Возвращает список валют и список акций из json с настройками пользователя"""

    logger.info(f"Вызвана функция получения настроек пользователя из {path}")
    with open(path) as file:
        user_settings = json.load(file)
        logger.info(f"Успешно получены настройки пользователя")
    return user_settings["user_currencies"], user_settings["user_stocks"]

