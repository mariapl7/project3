import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from pandas import DataFrame
import os

# Установите уровень логирования
logging.basicConfig(level=logging.INFO)


def load_data(filepath: str) -> DataFrame:
    """Загружает данные из Excel и преобразует даты в datetime."""
    if not os.path.isfile(filepath):
        logging.error(f'Файл не найден: {filepath}')
        return None

    transactions_df = pd.read_excel(filepath, engine='openpyxl')

    # Преобразуем поля дат в datetime
    transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'])
    transactions_df['Дата платежа'] = pd.to_datetime(transactions_df['Дата платежа'])

    return transactions_df


def calculate_weekly_expenses(transactions_df: DataFrame) -> DataFrame:
    """Расчет еженедельных расходов по категориям"""
    if transactions_df is None:
        return None

    weekly_expenses = (
        transactions_df.groupby('weekday')['Сумма операции'].sum()
    )

    return weekly_expenses


def expenses_by_weekday(transactions_df: DataFrame, date: str = None) -> str:
    """Отчет о тратах по дням недели."""
    try:
        if transactions_df is None or transactions_df.empty:
            return json.dumps({'error': 'Нет данных для анализа'})

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        reference_date = datetime.strptime(date, "%Y-%m-%d")

        # Добавляем столбец с днем недели
        transactions_df['weekday'] = transactions_df['Дата операции'].dt.day_name()
        weekly_expenses = (
            transactions_df.groupby('weekday')['Сумма операции'].sum()
            .reset_index()
            .sort_values('weekday')
        )

        # Формируем ответ
        response_data = {
            'weekly_expenses': weekly_expenses.to_dict(orient='records'),
            'reference_date': reference_date.strftime("%Y-%m-%d")
        }
        return json.dumps(response_data)
    except Exception as e:
        logging.error(f"Error in expenses_by_weekday: {e}")
        return json.dumps({'error': str(e)})


def expenses_by_workday_or_weekend(transactions_df: DataFrame, category: str, reference_date: str) -> str:
    """Отчет о тратах в рабочий/выходной день по категории."""
    try:
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
        end_date = reference_date
        start_date = reference_date - timedelta(days=90)

        # Фильтруем по категории и датам
        filtered_df = transactions_df[(transactions_df['Категория'] == category) &
                                      (transactions_df['Дата операции'] >= start_date) &
                                      (transactions_df['Дата операции'] <= end_date)]

        # Разделяем траты на рабочие и выходные дни
        filtered_df['is_workday'] = filtered_df['Дата операции'].dt.dayofweek < 5
        workday_expenses = filtered_df[filtered_df['is_workday']]['Сумма операции'].sum()
        weekend_expenses = filtered_df[~filtered_df['is_workday']]['Сумма операции'].sum()

        # Формируем ответ
        response_data = {
            'category': category,
            'workday_expenses': workday_expenses,
            'weekend_expenses': weekend_expenses,
            'period': {
                'start': start_date.strftime("%Y-%m-%d"),
                'end': end_date.strftime("%Y-%m-%d")
            }
        }
        return json.dumps(response_data)
    except Exception as e:
        logging.error(f"Error in expenses_by_workday_or_weekend: {e}")
        return json.dumps({'error': str(e)})


# Пример использования
if __name__ == '__main__':
    # Загрузка данных из Excel
    filepath = r'C:\Users\miplo\PycharmProjects\pythonProject3\data\operations.xlsx'
    df_transactions = load_data(filepath)
