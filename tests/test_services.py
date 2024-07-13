import pandas as pd
import pytest

from src.services import get_cashback_by_category
from tests.data_for_tests import dict_prepared


@pytest.fixture
def input_dataframe():
    return pd.DataFrame(dict_prepared)


def test_get_cashback_by_category(input_dataframe):
    assert get_cashback_by_category(input_dataframe, 2021, 12) == "{}"
