import json
import logging
import datetime

import pandas as pd
import numpy as np
from pathlib import Path


# Настройки логгирования
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
# formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
# fh.setFormatter(formatter)
# logger.addHandler(fh)


def get_transactions_from_xls(file_path: str) -> pd.DataFrame:
    """Функция принимает на вход путь до CSV-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл не найден, функция возвращает пустой список.
    """
    try:
        transactions_df = pd.read_excel(file_path)
        print(transactions_df.head())
        print(transactions_df.info())
        # print(transactions_df.iloc[:5].to_dict(orient="list"))
        # # Приводим дату к формату "%Y-%m-%dT%H:%M:%S.%f" для совместимости с функцией convert_date из модуля widget.py
        # # transactions_df.date = transactions_df.date.str.replace("Z", ":000000")
        #
        # transactions_dict = transactions_df.to_dict(orient="records")
        #
        # print(json.dumps(transactions_dict, indent=4, ensure_ascii=False))
        # # Приводим список словарей к единому формату
        # for i in range(len(transactions_dict)):
        #     transactions_dict[i]["operationAmount"] = {
        #         "amount": transactions_dict[i].pop("amount"),
        #         "currency": {
        #             "name": transactions_dict[i].pop("currency_name"),
        #             "code": transactions_dict[i].pop("currency_code"),
        #         },
        #     }
        # logger.info(f"Получен список транзакций из файла {file_path}")

        date_cols = ['Дата операции', 'Дата платежа']
        transactions_df[date_cols] = transactions_df[date_cols].astype("datetime64[ns]")
        print(transactions_df.iloc[:3, :4])
        print(transactions_df.info())


        return transactions_df

    except FileNotFoundError:
        # logger.info(f"Файл {file_path} не найден")
        return []


def date_converter(date: str) -> datetime:
    """Функция конвертации даты, переданной строкой, в формат datetime"""

    try:
        date_dt = datetime.datetime.strptime(date, "%d.%m.%Y")
        return np.datetime64(date_dt)

    except Exception:
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        return np.datetime64(date_dt)

    except Exception:
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return np.datetime64(date_dt)

    except Exception:
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%Y-%m")
        return np.datetime64(date_dt)

    except Exception:
        pass


    raise Exception("Неверный формат даты")




if __name__ in "__main__":
#     get_transactions_from_csv(Path.cwd().parent.joinpath("data", "transactions.csv"))
    get_transactions_from_xls(Path.cwd().parent.joinpath("data", "operations.xls"))
    print(date_converter("2023-11"))
