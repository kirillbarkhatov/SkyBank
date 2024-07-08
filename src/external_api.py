import os

import requests
from dotenv import load_dotenv

load_dotenv()
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")


def currency_rate(currencies: list) -> list[dict]:
    """Функция обеспечивает обращение к внешнему API для получения текущего курса заданных валют"""

    currency_rates = []
    for currency in currencies:
        url = "https://api.apilayer.com/exchangerates_data/latest"
        params = {"base": currency, "symbols": "RUB"}
        response = requests.get(url, params=params, headers={"apikey": EXCHANGE_RATE_API_KEY})

        if response.status_code != 200:
            raise requests.RequestException
        response_data = response.json()
        currency_rates.append({"currency": currency, "rate": round(response_data["rates"]["RUB"], 2)})
    return currency_rates


def stocks_rate(stocks: list) -> list[dict]:
    """Функция обеспечивает обращение к внешнему API для получения текущих цен заданных акций"""

    stocks_rates = []
    for stock in stocks:
        # почему-то не получилось через params. Надо потом посмотреть
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={STOCKS_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.RequestException
        response_data = response.json()
        stocks_rates.append({"stock": stock, "price": round(float(response_data["Global Quote"]["05. price"]), 2)})
    return stocks_rates


def currency_converter(amount: float, currency: str) -> float:
    """Функция обеспечивает обращение к внешнему API для получения текущего курса валют
    и конвертации суммы операции в рубли
    """

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={"apikey": EXCHANGE_RATE_API_KEY})
    if response.status_code != 200:
        raise requests.RequestException
    response_data = response.json()
    amount_rub = round(amount * response_data["rates"]["RUB"], 2)
    return float(amount_rub)


print(currency_rate(["USD", "EUR", "RUB"]))
#
# print(stocks_rate(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]))
