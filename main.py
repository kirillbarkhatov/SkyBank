# from src.external_api import currency_rate, stocks_rate
from src.reports import spending_by_category

# from src.services import get_cashback_by_category
from src.utils import date_converter, get_transactions_from_xls, get_user_settings
from src.views import get_main_page_data

print(date_converter("01.01.2020"))
print(date_converter("2020-02"))
print(get_transactions_from_xls())
user_currencies, user_stocks = get_user_settings()
print(get_main_page_data("2020-07-20 13:00:00", user_currencies, user_stocks))
# print(currency_rate(user_currencies))
# print(stocks_rate(user_stocks))
spending_by_category(get_transactions_from_xls(), "Аптеки", "01.06.2020")
# print(get_cashback_by_category(get_transactions_from_xls(), 2020, 2))
