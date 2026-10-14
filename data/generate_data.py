import sqlite3
import random
from datetime import datetime, timedelta


def init_db():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # Сбрасываем старые таблицы, если они были, для чистоты перезапуска
    cursor.execute("DROP TABLE IF EXISTS clients")
    cursor.execute("DROP TABLE IF EXISTS balances")
    cursor.execute("DROP TABLE IF EXISTS transactions_aggr")

    # Создаем таблицы заново
    cursor.execute('''
    CREATE TABLE clients (
        client_id INTEGER PRIMARY KEY,
        age INTEGER,
        gender TEXT,
        registration_date TEXT,
        credit_score INTEGER,
        has_credit_card INTEGER,
        is_churned INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE balances (
        client_id INTEGER PRIMARY KEY,
        current_balance REAL,
        estimated_salary REAL,
        products_count INTEGER,
        FOREIGN KEY(client_id) REFERENCES clients(client_id)
    )''')

    cursor.execute('''
    CREATE TABLE transactions_aggr (
        client_id INTEGER PRIMARY KEY,
        tx_count_3m INTEGER,
        tx_amount_3m REAL,
        complaints_3m INTEGER,
        FOREIGN KEY(client_id) REFERENCES clients(client_id)
    )''')

    conn.commit()
    return conn


def generate_mock_data(num_records=5000):
    conn = init_db()
    cursor = conn.cursor()

    # Вспомогательные данные для генерации дат регистрации (за последние 5 лет)
    start_date = datetime(2021, 1, 1)

    clients_data = []
    balances_data = []
    tx_data = []

    for client_id in range(1, num_records + 1):
        # 1. Сначала определяем, уйдет ли клиент (балансируем классы ~20% оттока)
        # Это нужно, чтобы настроить зависимость других признаков от целевой переменной
        is_churned = 1 if random.random() < 0.20 else 0

        # 2. Демография и профиль (Таблица clients)
        # Бизнес-логика: люди среднего возраста (35-50) в банках уходят чуть чаще
        if is_churned:
            age = random.randint(35, 55)
            credit_score = random.randint(450, 700)  # у уходящих рейтинг часто чуть ниже
        else:
            age = random.randint(18, 75)
            credit_score = random.randint(550, 850)

        gender = random.choice(['M', 'F'])
        has_credit_card = 1 if random.random() < 0.7 else 0

        random_days = random.randint(0, 1800)
        reg_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

        clients_data.append((client_id, age, gender, reg_date, credit_score, has_credit_card, is_churned))

        # 3. Финансы (Таблица balances)
        estimated_salary = round(random.uniform(30000, 250000), 2)

        # Бизнес-логика: если клиент уходит, у него скорее всего осталось мало денег на счете
        # или он пользуется слишком большим/малым количеством продуктов (активно забирает средства)
        if is_churned:
            current_balance = round(random.uniform(0, 50000), 2)
            products_count = random.choice([1, 4])  # либо 1 (почти все закрыл), либо 4 (перегружен)
        else:
            current_balance = round(random.uniform(20000, 1000000), 2)
            products_count = random.choice([1, 2, 3])

        balances_data.append((client_id, current_balance, estimated_salary, products_count))

        # 4. Активность (Таблица transactions_aggr)
        # Бизнес-логика: уходящие клиенты совершают мало транзакций и чаще жалуются
        if is_churned:
            tx_count_3m = random.randint(0, 8)
            tx_amount_3m = round(random.uniform(0, tx_count_3m * 1500), 2)
            complaints_3m = 1 if random.random() < 0.4 else 0  # 40% уходящих имели жалобы
        else:
            tx_count_3m = random.randint(10, 80)
            tx_amount_3m = round(random.uniform(tx_count_3m * 500, tx_count_3m * 3000), 2)
            complaints_3m = 1 if random.random() < 0.05 else 0  # только 5% лояльных жалуются

        tx_data.append((client_id, tx_count_3m, tx_amount_3m, complaints_3m))

    # Массовая вставка данных для высокой скорости работы
    cursor.executemany("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)", clients_data)
    cursor.executemany("INSERT INTO balances VALUES (?, ?, ?, ?)", balances_data)
    cursor.executemany("INSERT INTO transactions_aggr VALUES (?, ?, ?, ?)", tx_data)

    conn.commit()
    conn.close()
    print(f"База данных успешно создана! Сгенерировано строк: {num_records}")


if __name__ == '__main__':
    generate_mock_data(5000)
