import pytest
import pandas as pd
from src.services import get_events, get_cashback_categories


def test_get_events():
    data = {
        'event_name': ['event1', 'event2'],
        'event_date': ['2023-09-01', '2023-09-02']
    }
    df = pd.DataFrame(data)

    result = get_events(df)

    expected_result = {
        'events': [
            {'event_name': 'event1', 'event_date': '2023-09-01'},
            {'event_name': 'event2', 'event_date': '2023-09-02'}
        ]
    }
    assert result == expected_result


@pytest.mark.parametrize("year, month, transactions, expected_categories", [
    (2023, 9, [
        {'date': '2023-09-01', 'category': 'electronics'},
        {'date': '2023-09-02', 'category': 'clothing'},
        {'date': '2023-08-30', 'category': 'groceries'}
    ], []),
    (2023, 9, [
        {'date': '2023-09-01', 'category': 'electronics'},
        {'date': '2023-09-02', 'category': 'cashback'},
        {'date': '2023-09-15', 'category': 'clothing'}
    ], []),
])
def test_get_cashback_categories(year, month, transactions, expected_categories):
    result = get_cashback_categories(year, month, transactions)
    assert result == {'cashback_categories': expected_categories}


def test_get_cashback_categories_with_conditions():
    year = 2023
    month = 9
    transactions = [
        {'date': '2023-09-01', 'category': 'electronics'},
        {'date': '2023-09-02', 'category': 'clothing'},
        {'date': '2023-09-05', 'category': 'groceries'},
        {'date': '2023-09-15', 'category': 'electronics'},
    ]

    expected_categories = ['electronics', 'electronics']

    result = get_cashback_categories(year, month, transactions)
    assert result == {'cashback_categories': expected_categories}
