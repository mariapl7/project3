import json
from datetime import datetime
import logging

def get_events(df):
    """Обрабатывает DataFrame и возвращает события в формате JSON."""
    events = df.to_dict(orient='records')  # Преобразование DataFrame в список словарей
    return {'events': events}

def get_cashback_categories(year, month, transactions):
    """Возвращает выгодные категории повышенного кешбэка."""
    categories = []
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
        if transaction_date.year == year and transaction_date.month == month:
            # Ваши условия и логика для определения категории
            pass
    return {'cashback_categories': categories}

def get_invest_piggy_bank(month, transactions, limit):
    """Рассчитывает общую сумму для сервисов Инвесткопилки."""
    total_investments = 0
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
        if transaction_date.month == month:
            total_investments += transaction['amount']  # Логика для суммирования инвестиций
    total_investments = round(total_investments, limit)  # Округление
    return {'total_investments': total_investments}

def simple_search(query, transactions):
    """Поиск транзакций по заданному запросу."""
    results = [txn for txn in transactions if query.lower() in txn['description'].lower()]
    return {'results': results}

def search_by_phone(transactions, phone_number):
    """Поиск транзакций по телефонным номерам."""
    results = [txn for txn in transactions if txn.get('phone') == phone_number]
    return {'phone_results': results}

def search_transfers_to_individuals(transactions):
    """Поиск переводов физическим лицам."""
    results = [txn for txn in transactions if txn['type'] == 'transfer' and txn['recipient_type'] == 'individual']
    return {'transfer_results': results}