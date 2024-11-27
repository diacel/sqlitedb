import hashlib
import sqlite3
from tabulate import tabulate

ton = sqlite3.connect("base.db")
cur = ton.cursor()

def register_user(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed_password, role))
        ton.commit()
        print("Пользователь успешно зарегистрирован.")
    except sqlite3.IntegrityError:
        print("Пользователь с таким именем уже существует.")

def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cur.fetchone()
    return user

def main():
    while True:
        print("\n1. Вход")
        print("2. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            user = authenticate_user(username, password)
            if user:
                print(f"Добро пожаловать в функциональный режим, {user[1]}!")
                sql_interface()
            else:
                print("Неверное имя пользователя или пароль.")
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def sql_interface():
    while True:
        print("\nВведите SQL команду (или 'выход' для выхода):")
        sql_command = input("SQL команда: ")
        
        if sql_command.lower() == 'выход':
            break
        elif sql_command.lower() == 'негр':
            print_help()
            continue
        elif sql_command.strip().lower() == 'select *':
            show_tables()
            continue
        
        try:
            cur.execute(sql_command)
            if sql_command.strip().upper().startswith("SELECT"):
                results = cur.fetchall()
                headers = [description[0] for description in cur.description]
                print(tabulate(results, headers=headers, tablefmt="grid"))
            else:
                ton.commit()
                print("Команда выполнена успешно.")
        except sqlite3.Error as e:
            print(f"Ошибка выполнения команды: {e}")

def show_tables():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    if tables:
        print("\nСуществующие таблицы:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("Нет существующих таблиц.")

def print_help():
    help_text = """
    Доступные команды:
    1. SELECT * FROM <таблица> - Просмотр всех записей из указанной таблицы.
    2. INSERT INTO <таблица> (...) VALUES (...) - Добавление новой записи.
    3. UPDATE <таблица> SET <поля> WHERE <условие> - Обновление записи.
    4. DELETE FROM <таблица> WHERE <условие> - Удаление записи.
    5. CREATE TABLE <имя таблицы> (...) - Создание новой таблицы.
    6. DROP TABLE <имя таблицы> - Удаление таблицы.
    7. EXIT - Выход из интерфейса SQL.
    """
    print(help_text)

if __name__ == "__main__":
    main()