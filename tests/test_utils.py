import pytest
from src.utils import get_transactions_from_xls, date_converter, get_user_settings
from unittest.mock import patch, mock_open


# Тест на отсутствие файла для чтения
@patch("os.path.exists")
def test_get_transactions_from_xls_file_not_exist(mock_os_path_exists):
    mock_os_path_exists.return_value = False
    assert get_transactions_from_xls("test") == []



@patch("os.path.exists")
def test_get_transactions_from_xls(mock_os_path_exists):
    mock_os_path_exists.return_value = True
    m = mock_open(read_data=["test data"])
    with patch("builtins.open", m) as mocked_open:
