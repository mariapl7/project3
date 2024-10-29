import json
from datetime import datetime
from utils import (load_user_settings, calculate_date_range,
                   fetch_stock_prices, fetch_currency_rates,
                   get_greeting, get_card_info, get_top_transactions,
                   fetch_sp500_prices)


# Пример API URL для курсов валют и цен акций S&P 500
CURRENCY_API_URL = "https://api.exchangeratesapi.io/latest"  # Замените на актуальный API
SP500_API_URL = "https://api.example.com/sp500"  # Замените на актуальный API


def events_view(date_str):
    """Главная функция для получения данных о событиях."""
    try:
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

        return json.dumps(response_data)

    except Exception as e:
        return json.dumps({'error': str(e)})


def main_view(date_time_str):
    """Главная функция для страницы 'Главная'."""
    try:
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

        return json.dumps(response_data)

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    date_str = "2023-09"
    print(events_view(date_str))
    date_time_str = "2023-09-01 14:30:00"
    print(main_view(date_time_str))
