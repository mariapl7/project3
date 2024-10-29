import json
import requests
import logging
import pandas as pd
from datetime import datetime, timedelta


def load_user_settings(filename='user_settings.json'):
    """Загружает пользовательские настройки из JSON файла."""
    with open(filename, 'r') as f:
        return json.load(f)


def calculate_date_range(date_str):
    """Вычисляет начальную и конечную даты для анализа."""
    end_date = datetime.strptime(date_str, "%d.%m.%Y")
    start_date = end_date.replace(day=1)
    return start_date, end_date


def fetch_currency_rates(currencies):
    """Получает курсы валют для заданных валют из API."""
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = {currency: data['rates'].get(currency) for currency in currencies}
        return rates
    else:
        logging.error("Ошибка получения курсов валют: %s", response.status_code)
        return {}


def fetch_stock_prices(stocks):
    """Получает цены акций для заданных акций из API."""
    stock_prices = {}
    for stock in stocks:
        url = f"https://api.example.com/stock/{stock}"  # Замените на актуальный API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            stock_prices[stock] = data.get('currentPrice', None)  # Используйте get для избежания KeyError
        else:
            logging.error("Ошибка получения данных по акции %s: %s", stock, response.status_code)
    return stock_prices


# Настройки логирования
logging.basicConfig(level=logging.INFO)


def get_greeting(current_datetime):
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_datetime.hour
    if hour < 6:
        return "Доброй ночи"
    elif hour < 12:
        return "Доброе утро"
    elif hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_card_info(transactions):
    """Возвращает информацию о картах: последние 4 цифры, сумма расходов и кешбэк."""
    card_summary = {}
    for transaction in transactions:
        card_last_digits = transaction['card_number'][-4:]
        amount = transaction['amount']

        if card_last_digits not in card_summary:
            card_summary[card_last_digits] = {
                'total_spent': 0,
                'cashback': 0
            }

        card_summary[card_last_digits]['total_spent'] += amount
        card_summary[card_last_digits]['cashback'] += amount // 100

    return card_summary


def get_top_transactions(transactions, top_n=5):
    """Возвращает топ-N транзакций по сумме платежа."""
    sorted_transactions = sorted(transactions, key=lambda x: x['amount'], reverse=True)
    return sorted_transactions[:top_n]


def fetch_sp500_prices(api_url):
    """Получает стоимость акций из S&P 500."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Ошибка получения данных по S&P 500: %s", response.status_code)
        return {}


def parse_date_range(date_str, period='M'):
    """Возвращает начальную и конечную даты для заданного диапазона."""
    date = datetime.strptime(date_str, "%Y-%m-%d")

    if period == 'W':
        start_date = date - timedelta(days=date.weekday())
        end_date = date
    elif period == 'M':
        start_date = date.replace(day=1)
        end_date = date
    elif period == 'Y':
        start_date = date.replace(month=1, day=1)
        end_date = date
    elif period == 'ALL':
        start_date = datetime.min
        end_date = date
    else:
        raise ValueError("Некорректный период - допустимые значения: W, M, Y, ALL")

    return start_date, end_date


def calculate_expenses(transactions, start_date, end_date):
    """Подсчитывает общие расходы и сортирует их по категориям."""
    expenses = [t for t in transactions if start_date <= datetime.strptime(t['date'], "%Y-%m-%d") <= end_date]

    total_expenses = sum(t['amount'] for t in expenses)

    categories = pd.DataFrame(expenses).groupby('category')['amount'].sum().reset_index()
    categories = categories.sort_values(by='amount', ascending=False)

    if len(categories) > 6:
        others_sum = categories['amount'].sum() - categories['amount'].head(6).sum()
        categories = categories.head(6).append({'category': 'Остальное', 'amount': others_sum}, ignore_index=True)

    return round(total_expenses), categories


def calculate_income(incomes, start_date, end_date):
    """Подсчитывает общие поступления и сортирует их по категориям."""
    incomes_filtered = [t for t in incomes if start_date <= datetime.strptime(t['date'], "%Y-%m-%d") <= end_date]

    total_income = sum(i['amount'] for i in incomes_filtered)

    categories = pd.DataFrame(incomes_filtered).groupby('category')['amount'].sum().reset_index()
    categories = categories.sort_values(by='amount', ascending=False)

    return round(total_income), categories
