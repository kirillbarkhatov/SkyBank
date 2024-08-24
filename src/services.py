import json
import logging

import pandas as pd

# Настройки логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_cashback_by_category(transactions: pd.DataFrame, year: int, month: int) -> str:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кешбэка
    """

    logger.info(f"Вызвана функция get_cashback_by_category с параметрами {year}, {month}")
    month_data = transactions.loc[
        (transactions["Дата операции"].dt.month == month) & (transactions["Дата операции"].dt.year == year)
    ]
    cashback_grouped = (
        month_data.groupby("Категория")["Кэшбэк"].sum().sort_values(ascending=False).loc[lambda x: x > 0]
    )

    cashback = json.dumps(cashback_grouped.to_dict(), indent=4, ensure_ascii=False)
    return cashback
