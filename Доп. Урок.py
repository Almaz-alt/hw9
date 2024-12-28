import sqlite3


def create_db():
    # Создаем или открываем базу данных
    conn = sqlite3.connect('store_db.sqlite')
    cursor = conn.cursor()

    # Создаем таблицу stores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        store_id INTEGER PRIMARY KEY,
        title TEXT
    )""")

    # Создаем таблицу products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        title TEXT,
        category TEXT,
        price REAL,
        stock_quantity INTEGER,
        store_id INTEGER,
        FOREIGN KEY(store_id) REFERENCES stores(store_id)
    )""")

    # Вставляем тестовые данные в таблицу stores
    cursor.execute("INSERT INTO stores (title) VALUES ('Asia')")
    cursor.execute("INSERT INTO stores (title) VALUES ('Globus')")
    cursor.execute("INSERT INTO stores (title) VALUES ('Spar')")

    # Вставляем тестовые данные в таблицу products
    cursor.execute(
        "INSERT INTO products (title, category, price, stock_quantity, store_id) VALUES ('Chocolate', 'Food products', 10.5, 129, 1)")
    cursor.execute(
        "INSERT INTO products (title, category, price, stock_quantity, store_id) VALUES ('Milk', 'Dairy', 1.5, 200, 1)")
    cursor.execute(
        "INSERT INTO products (title, category, price, stock_quantity, store_id) VALUES ('Apple', 'Fruits', 2.0, 50, 2)")
    cursor.execute(
        "INSERT INTO products (title, category, price, stock_quantity, store_id) VALUES ('Bread', 'Bakery', 1.2, 150, 3)")

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("База данных создана и данные добавлены.")


# Создание базы данных и таблиц
create_db()

import sqlite3


# Функция для подключения к базе данных
def connect_to_db():
    try:
        # Подключаемся к SQLite базе данных
        conn = sqlite3.connect('store_db.sqlite')
        print("Соединение с базой данных установлено.")
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None


# Функция для получения списка магазинов
def get_stores(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT store_id, title FROM stores")
    stores = cursor.fetchall()
    return stores


# Функция для получения продуктов для выбранного магазина
def get_products_by_store(conn, store_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, category, price, stock_quantity
        FROM products
        WHERE store_id = ?
    """, (store_id,))
    products = cursor.fetchall()
    return products


# Основная программа
def main():
    # Подключение к базе данных
    conn = connect_to_db()

    if conn is None:
        return

    while True:
        # Отображаем список магазинов
        print("Вы можете отобразить список продуктов по выбранному id магазина из")
        print("перечня магазинов ниже, для выхода из программы введите цифру 0:")

        # Получаем список магазинов
        stores = get_stores(conn)

        if not stores:
            print("Нет данных о магазинах в базе данных.")
            break

        for store in stores:
            print(f"{store[0]}. {store[1]}")

        # Ввод id магазина
        try:
            store_id = int(input("Введите id магазина: "))
        except ValueError:
            print("Ошибка: введите числовой id.")
            continue

        # Выход из программы
        if store_id == 0:
            print("Выход из программы.")
            break

        # Получаем и отображаем продукты для выбранного магазина
        products = get_products_by_store(conn, store_id)

        if products:
            for product in products:
                print(f"Название продукта: {product[0]}")
                print(f"Категория: {product[1]}")
                print(f"Цена: {product[2]}")
                print(f"Количество на складе: {product[3]}")
                print("-" * 30)
        else:
            print("Нет продуктов в выбранном магазине.")

    # Закрываем соединение с базой данных
    conn.close()


if __name__ == "__main__":
    main()

# Соединение с базой данных установлено.
# Вы можете отобразить список продуктов по выбранному id магазина из
# перечня магазинов ниже, для выхода из программы введите цифру 0:
# 1. Asia
# 2. Globus
# 3. Spar
# Введите id магазина: 1
# Название продукта: Chocolate
# Категория: Food products
# Цена: 10.5
# Количество на складе: 129
# ------------------------------
# Название продукта: Milk
# Категория: Dairy
# Цена: 1.5
# Количество на складе: 200
# ------------------------------
# Введите id магазина: 0
# Выход из программы.