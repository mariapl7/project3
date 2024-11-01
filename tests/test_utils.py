import json
import pytest
from unittest import mock
from datetime import datetime
from src.utils import load_user_settings, calculate_date_range


@pytest.fixture
def mock_user_settings(mocker):
    """Фикстура для мока данных пользовательских настроек."""
    mock_data = {
        "setting_1": "value_1",
        "setting_2": "value_2"
    }
    mocker.patch('builtins.open', mock.mock_open(read_data=json.dumps(mock_data)))
    return mock_data


def test_load_user_settings(mock_user_settings):
    """Тест для функции load_user_settings."""
    settings = load_user_settings('dummy.json')
    assert settings == mock_user_settings


def test_load_user_settings_file_not_found(mocker):
    """Тест для случая, когда файл не найден."""
    mocker.patch('builtins.open', side_effect=FileNotFoundError)

    with pytest.raises(FileNotFoundError):
        load_user_settings('non_existent_file.json')


def test_calculate_date_range():
    """Тест для функции calculate_date_range."""
    date_str = "15.09.2023"
    start_date, end_date = calculate_date_range(date_str)

    assert start_date == datetime(2023, 9, 1)
    assert end_date == datetime(2023, 9, 15)


def test_calculate_date_range_invalid_format():
    """Тест для функции calculate_date_range с неправильным форматом даты."""
    with pytest.raises(ValueError):
        calculate_date_range("2023-09-15")
