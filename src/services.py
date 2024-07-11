import json

import pandas as pd

from src.utils import get_transactions_from_xls


def get_cashback_by_category(data: pd.DataFrame, year: int, month: int) -> str:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кешбэка
    """

    month_data = data.loc[(data["Дата операции"].dt.month == month) & (data["Дата операции"].dt.year == year)]
    print(month_data)
    print(month_data.loc[month_data["Кэшбэк"] != 0])
    cashback_month_data = month_data.loc[month_data["Кэшбэк"] != ""]
    cashback_grouped = month_data.groupby("Категория")["Кэшбэк"].sum().sort_values(ascending=False).loc[lambda x: x > 0]
    print()
    cashback = json.dumps(cashback_grouped.to_dict(),
        indent=4,
        ensure_ascii=False
    )
    print(cashback)


if __name__ == "__main__":
    df = get_transactions_from_xls()
    print(df)
    get_cashback_by_category(df, 2020, 2)