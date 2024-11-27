import hashlib
import sqlite3
import os
from tabulate import tabulate

admin_db = sqlite3.connect("admin/user.db")
cur_admin = admin_db.cursor()

def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur_admin.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cur_admin.fetchone()
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
                print(f"Добро пожаловать, {user[1]}!")
                select_database(user[3])
            else:
                print("Неверное имя пользователя или пароль.")
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def get_databases_from_folder(folder_path):
    databases = [f for f in os.listdir(folder_path) if f.endswith('.db')]
    return databases

def select_database(role):
    folder_path = 'db'
    databases = get_databases_from_folder(folder_path)
    
    if not databases:
        print("Нет доступных баз данных.")
        return
    
    while True:
        print("\nДоступные базы данных:")
        for i, db in enumerate(databases, 1):
            print(f"{i}. {db}")
        print("0. Вернуться в главное меню")
        
        choice = input("Выберите номер базы данных для входа (или 0 для выхода): ")
        
        if choice == '0':
            break
            
        try:
            db_index = int(choice) - 1
            if 0 <= db_index < len(databases):
                db_name = databases[db_index]
                print(f"Вы вошли в базу данных: {db_name}")
                with sqlite3.connect(os.path.join(folder_path, db_name)) as db:
                    if role == 'admin':
                        admin_menu(db)
                    elif role == 'super_admin':
                        super_admin_menu(db)
                    else:
                        employee_menu(db)
            else:
                print("Неверный номер базы данных. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def admin_menu(db):
    while True:
        print("\nAdmin Menu")
        print("1. Просмотреть данные")
        print("2. Редактировать данные")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_data(db)
        elif choice == '2':
            edit_data(db)
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def super_admin_menu(db):
    while True:
        print("\nSuper Admin Menu")
        print("1. Просмотреть данные")
        print("2. Редактировать данные")
        print("3. Зарегистрировать новый аккаунт")
        print("4. Просмотреть пользователей")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_data(db)
        elif choice == '2':
            edit_data(db)
        elif choice == '3':
            register_new_account()
        elif choice == '4':
            view_users()
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def employee_menu(db):
    while True:
        print("\nEmployee Menu")
        print("1. Просмотреть данные")
        print("2. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_data(db)
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def view_data(db):
    tables = get_tables(db)
    if not tables:
        print("Нет доступных таблиц.")
        return
    
    while True:
        print("\nДоступные таблицы:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("0. Вернуться в меню")
        
        choice = input("Выберите номер таблицы для просмотра (или 0 для выхода): ")
        
        if choice == '0':
            break
            
        try:
            table_index = int(choice) - 1
            if 0 <= table_index < len(tables):
                table_name = tables[table_index]
                cur = db.cursor()
                cur.execute(f"SELECT * FROM {table_name}")
                rows = cur.fetchall()
                print(tabulate(rows, headers=[column[0] for column in cur.description], tablefmt='grid'))
            else:
                print("Неверный номер таблицы. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def get_tables(db):
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    return [table[0] for table in tables]

def edit_data(db):
    tables = get_tables(db)
    if not tables:
        print("Нет доступных таблиц для редактирования.")
        return
    
    while True:
        print("\nДоступные таблицы для редактирования:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("0. Вернуться в меню")
        
        choice = input("Выберите номер таблицы для редактирования (или 0 для выхода): ")
        
        if choice == '0':
            break
            
        try:
            table_index = int(choice) - 1
            if 0 <= table_index < len(tables):
                table_name = tables[table_index]
                print(f"Редактирование данных в таблице: {table_name}")
                add_record(db, table_name)
            else:
                print("Неверный номер таблицы. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def add_record(db, table_name):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table_name} LIMIT 1")
    columns = [column[0] for column in cur.description]
    
    new_record = {}
    for column in columns:
        value = input(f"Введите значение для {column}: ")
        new_record[column] = value
    
    columns_str = ', '.join(new_record.keys())
    placeholders = ', '.join('?' * len(new_record))
    values = tuple(new_record.values())
    
    cur.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
    db.commit()
    print("Запись успешно добавлена.")

def register_new_account():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    with sqlite3.connect("admin/user.db") as admin_db:
        cur = admin_db.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        admin_db.commit()
        print("Новый аккаунт успешно зарегистрирован.")

def view_users():
    with sqlite3.connect("admin/user.db") as admin_db:
        cur = admin_db.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        print(tabulate(rows, headers=[column[0] for column in cur.description], tablefmt='grid'))

if __name__ == "__main__":
    main()