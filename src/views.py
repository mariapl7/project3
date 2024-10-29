from datetime import datetime
from utils import get_greeting, get_card_info, get_top_transactions, fetch_sp500_prices
from flask import Flask, jsonify
from utils import load_user_settings, calculate_date_range, fetch_stock_prices
from utils import fetch_currency_rates, parse_date_range,  calculate_expenses
from utils import calculate_income

app = Flask(__name__)


@app.route('/api/events/<date_str>', methods=['GET'])
def events_view(date_str):
    """Главная функция для получения данных о событиях."""
    # Загружаем пользовательские настройки
    user_settings = load_user_settings()
    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']

    # Вычисляем диапазон дат
    start_date, end_date = calculate_date_range(date_str)

    # Получаем курсы валют и цены акций
    currency_rates = fetch_currency_rates(user_currencies)
    stock_prices = fetch_stock_prices(user_stocks)

    # Формируем JSON-ответ
    response_data = {
        'date_range': {
            'start': start_date.strftime("%Y-%m-%d"),
            'end': end_date.strftime("%Y-%m-%d")
        },
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)


# Пример API URL для курсов валют и цен акций S&P 500
CURRENCY_API_URL = "https://api.exchangeratesapi.io/latest"  # Замените на актуальный API
SP500_API_URL = "https://api.example.com/sp500"  # Замените на актуальный API


def main_view(date_time_str):
    """Главная функция для страницы 'Главная'."""
    # Преобразование строки в datetime-объект
    current_datetime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Генерация приветствия
    greeting = get_greeting(current_datetime)

    # Пример данных о транзакциях
    transactions = [
        {'card_number': '1234567812345678', 'amount': 1400},
        {'card_number': '8765432187654321', 'amount': 3000},
        {'card_number': '1234567812345678', 'amount': 600},
        {'card_number': '8765432187654321', 'amount': 500},
        {'card_number': '1111222233334444', 'amount': 850},
    ]

    # Получение информации по картам
    card_info = get_card_info(transactions)
    top_transactions = get_top_transactions(transactions)

    # Получение данных по курсам валют и ценам акций
    currency_rates = fetch_currency_rates(CURRENCY_API_URL)
    sp500_prices = fetch_sp500_prices(SP500_API_URL)

    # Формирование JSON-ответа
    response_data = {
        'greeting': greeting,
        'card_info': card_info,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'sp500_prices': sp500_prices,
    }

    return jsonify(response_data)


def events_view(date_str, period='M'):
    """Главная функция для страницы 'События'."""
    # Получаем диапазон дат
    start_date, end_date = parse_date_range(date_str, period)

    # Пример данных о транзакциях
    transactions = [
        {'date': '2023-09-01', 'amount': 100, 'category': 'Еда'},
        {'date': '2023-09-10', 'amount': 200, 'category': 'Транспорт'},
        {'date': '2023-09-15', 'amount': 150, 'category': 'Кафе'},
        {'date': '2023-09-20', 'amount': 300, 'category': 'Развлечения'},
        {'date': '2023-09-25', 'amount': 50, 'category': 'Еда'},
    ]

    incomes = [
        {'date': '2023-09-05', 'amount': 500, 'category': 'Зарплата'},
        {'date': '2023-09-15', 'amount': 100, 'category': 'Подарки'},
    ]

    # Расчет расходов и доходов
    total_expenses, expense_categories = calculate_expenses(transactions, start_date, end_date)
    total_income, income_categories = calculate_income(incomes, start_date, end_date)

    # Получение данных по курсам валют и ценам акций
    currency_rates = fetch_currency_rates(CURRENCY_API_URL)
    sp500_prices = fetch_sp500_prices(SP500_API_URL)

    # Формирование JSON-ответа
    response_data = {
        'total_expenses': total_expenses,
        'expenses_by_category': expense_categories.to_dict(orient='records'),
        'total_income': total_income,
        'income_by_category': income_categories.to_dict(orient='records'),
        'currency_rates': currency_rates,
        'sp500_prices': sp500_prices,
    }

    return jsonify(response_data)
