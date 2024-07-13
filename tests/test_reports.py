import pytest
from src.reports import spending_by_category, save_report
from tests.data_for_tests import dict_prepared
import pandas as pd
from unittest.mock import patch


@pytest.fixture
def input_dataframe():
    return pd.DataFrame(dict_prepared)


def test_get_cashback_by_category(input_dataframe):
    assert spending_by_category(input_dataframe, "Супермаркеты", "31.12.2021") == None
