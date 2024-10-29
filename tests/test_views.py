from src.views import load_transactions, profitable_categories


def test_profitable_categories():
    df = load_transactions('test_operations.xls')
    result = profitable_categories(df, 50)
    assert 'Категория 1' in result  # Замените на ожидаемое значение