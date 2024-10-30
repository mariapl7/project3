import json
import pytest
from src.views import events_view


@pytest.fixture
def mock_user_settings(mocker):
    """Фикстура для мок данных пользовательских настроек."""
    mock_settings = {
        'user_currencies': ['USD', 'EUR'],
        'user_stocks': ['AAPL', 'GOOGL']
    }
    mocker.patch('your_module.load_user_settings', return_value=mock_settings)
    return mock_settings


@pytest.fixture
def mock_fetch_currency_rates(mocker):
    """Фикстура для мока получения курсов валют."""
    mocker.patch('your_module.fetch_currency_rates', return_value={'USD': 1.0, 'EUR': 0.85})


@pytest.fixture
def mock_fetch_stock_prices(mocker):
    """Фикстура для мока получения цен акций."""
    mocker.patch('your_module.fetch_stock_prices', return_value={'AAPL': 150.0, 'GOOGL': 2800.0})


@pytest.mark.parametrize("date_str, expected_start, expected_end", [
    ("15.09.2023", "2023-09-01", "2023-09-15"),
    ("01.01.2021", "2021-01-01", "2021-01-01"),
])
def test_events_view(date_str, expected_start, expected_end):
    """Тест для функции events_view."""
    response = events_view(date_str)
    response_data = json.loads(response)

    assert response_data['date_range']['start'] == expected_start
    assert response_data['date_range']['end'] == expected_end
    assert response_data['currency_rates'] == {'USD': 1.0, 'EUR': 0.85}
    assert response_data['stock_prices'] == {'AAPL': 150.0, 'GOOGL': 2800.0}


def test_events_view_load_user_settings_error(mocker):
    """Тест для случая, когда load_user_settings выбрасывает ошибку."""
    mocker.patch('your_module.load_user_settings', side_effect=Exception("Failed to load settings"))

    response = events_view("15.09.2023")
    response_data = json.loads(response)

    assert 'error' in response_data
    assert response_data['error'] == "Failed to load settings"


def test_events_view_currency_rates_error(mocker):
    """Тест для случая, когда fetch_currency_rates выбрасывает ошибку."""
    mocker.patch('your_module.fetch_currency_rates', side_effect=Exception("Failed to fetch currency rates"))

    response = events_view("15.09.2023")
    response_data = json.loads(response)

    assert 'error' in response_data
    assert response_data['error'] == "Failed to fetch currency rates"


def test_events_view_stock_prices_error(mocker):
    """Тест для случая, когда fetch_stock_prices выбрасывает ошибку."""
    mocker.patch('your_module.fetch_stock_prices', side_effect=Exception("Failed to fetch stock prices"))

    response = events_view("15.09.2023")
    response_data = json.loads(response)

    assert 'error' in response_data
    assert response_data['error'] == "Failed to fetch stock prices"
