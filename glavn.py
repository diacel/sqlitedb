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
                print(f"Добро пожаловать, {user[1]}!")
                if user[3] == 'admin':
                    admin_menu()
                elif user[3] == 'super_admin':
                    super_admin_menu()
                else:
                    employee_menu()
            else:
                print("Неверное имя пользователя или пароль.")
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def super_admin_menu():
    while True:
        print("\n1. Просмотреть данные")
        print("2. Редактировать данные")
        print("3. Зарегистрировать новый аккаунт")
        print("4. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            super_view_data()
        elif choice == '2':
            super_edit_data()
        elif choice == '3':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            
            while True:
                print("\nВыберите роль:")
                print("1. admin")
                print("2. super_admin")
                print("3. employee")
                role_choice = input("Введите номер роли: ")
                
                if role_choice == '1':
                    role = 'admin'
                    break
                elif role_choice == '2':
                    role = 'super_admin'
                    break
                elif role_choice == '3':
                    role = 'employee'
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            
            register_user(username, password, role)
        
        elif choice == '4':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def admin_menu():
    while True:
        print("\n1. Просмотреть данные")
        print("2. Редактировать данные")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_data()
        elif choice == '2':
            edit_data()
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def employee_menu():
    while True:
        print("\n1. Просмотреть данные")
        print("2. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_data()
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def view_data():
    tables = ['driver', 'vehicle', 'violation', 'insurance', 'maintenance']
    
    while True:
        print("\nДоступные таблицы:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("0. Вернуться в главное меню")
        
        choice = input("Выберите номер таблицы для просмотра (или 0 для выхода): ")
        
        if choice == '0':
            break
        
        try:
            table_index = int(choice) - 1
            if 0 <= table_index < len(tables):
                table = tables[table_index]
                
                print(f"\nТаблица: {table}")
                
                cur.execute(f"PRAGMA table_info({table})")
                headers = [col[1] for col in cur.fetchall()]
                
                cur.execute(f"SELECT * FROM {table}")
                data = cur.fetchall()
                
                print(tabulate(data, headers=headers, tablefmt="grid"))
                
                input("Нажмите Enter для продолжения...")
            else:
                print("Неверный номер таблицы. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def edit_data():
    tables = ['driver', 'vehicle', 'violation', 'insurance', 'maintenance']
    
    while True:
        print("\nРедактирование данных")
        print("\nДоступные таблицы:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("0. Вернуться в главное меню")
        
        choice = input("Выберите номер таблицы для редактирования (или 0 для выхода): ")
        
        if choice == '0':
            break
            
        try:
            table_index = int(choice) - 1
            if 0 <= table_index < len(tables):
                table = tables[table_index]
                edit_table(table)
            else:
                print("Неверный номер таблицы. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def edit_table(table):
    while True:
        print(f"\nРедактирование таблицы {table}")
        print("1. Просмотреть текущие данные")
        print("2. Добавить новую запись")
        print("3. Изменить существующую запись")
        print("4. Удалить запись")
        print("0. Вернуться назад")
        
        choice = input("Выберите действие: ")
        
        if choice == '0':
            break
        elif choice == '1':
            cur.execute(f"PRAGMA table_info({table})")
            headers = [col[1] for col in cur.fetchall()]
            cur.execute(f"SELECT * FROM {table}")
            data = cur.fetchall()
            print(tabulate(data, headers=headers, tablefmt="grid"))
        
        elif choice == '2':
            cur.execute(f"PRAGMA table_info({table})")
            columns = cur.fetchall()
            values = []
            
            print("\nВведите значения для новой записи:")
            for col in columns[1:]:
                col_name = col[1]
                col_type = col[2]
                while True:
                    value = input(f"{col_name} ({col_type}): ")
                    if value.strip(): 
                        values.append(value)
                        break
                    print("Значение не может быть пустым!")
            
            placeholders = ','.join(['?' for _ in values])
            columns_str = ','.join([col[1] for col in columns[1:]])
            
            try:
                cur.execute(f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})", values)
                ton.commit()
                print("Запись успешно добавлена!")
            except sqlite3.Error as e:
                print(f"Ошибка при добавлении записи: {e}")
        
        elif choice == '3':
            id_to_edit = input("Введите ID записи для редактирования: ")
            try:
                cur.execute(f"SELECT * FROM {table} WHERE id = ?", (id_to_edit,))
                record = cur.fetchone()
                
                if record:
                    cur.execute(f"PRAGMA table_info({table})")
                    columns = cur.fetchall()
                    updates = []
                    values = []
                    
                    print("\nВведите новые значения (оставьте пустым, чтобы не менять):")
                    for i, col in enumerate(columns[1:], 1):
                        col_name = col[1]
                        current_value = record[i]
                        new_value = input(f"{col_name} (текущее значение: {current_value}): ")
                        
                        if new_value.strip():
                            updates.append(f"{col_name} = ?")
                            values.append(new_value)
                    
                    if updates:
                        values.append(id_to_edit) 
                        update_query = f"UPDATE {table} SET {', '.join(updates)} WHERE id = ?"
                        cur.execute(update_query, values)
                        ton.commit()
                        print("Запись успешно обновлена!")
                    else:
                        print("Не было внесено никаких изменений.")
                else:
                    print("Запись с указанным ID не найдена.")
            except sqlite3.Error as e:
                print(f"Ошибка при обновлении записи: {e}")
        
        elif choice == '4':
            id_to_delete = input("Введите ID записи для удаления: ")
            try:
                cur.execute(f"SELECT * FROM {table} WHERE id = ?", (id_to_delete,))
                if cur.fetchone():
                    confirm = input("Вы уверены, что хотите удалить эту запись? (да/нет): ")
                    if confirm.lower() == 'да':
                        cur.execute(f"DELETE FROM {table} WHERE id = ?", (id_to_delete,))
                        ton.commit()
                        print("Запись успешно удалена!")
                    else:
                        print("Удаление отменено.")
                else:
                    print("Запись с указанным ID не найдена.")
            except sqlite3.Error as e:
                print(f"Ошибка при удалении записи: {e}")
        
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")

def super_view_data():
    tables = ['users', 'driver', 'vehicle', 'violation', 'insurance', 'maintenance']
    
    while True:
        print("\nДоступные таблицы:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("0. Вернуться в главное меню")
        
        choice = input("Выберите номер таблицы для просмотра (или 0 для выхода): ")
        
        if choice == '0':
            break
        
        try:
            table_index = int(choice) - 1
            if 0 <= table_index < len(tables):
                table = tables[table_index]
                
                print(f"\nТаблица: {table}")
                
                cur.execute(f"PRAGMA table_info({table})")
                headers = [col[1] for col in cur.fetchall()]
                
                cur.execute(f"SELECT * FROM {table}")
                data = cur.fetchall()
                
                print(tabulate(data, headers=headers, tablefmt="grid"))
                
                input("Нажмите Enter для продолжения...")
            else:
                print("Неверный номер таблицы. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def super_edit_data():
    tables = ['users', 'driver', 'vehicle', 'violation', 'insurance', 'maintenance']
    
    while True:
        print("\nРедактирование данных")
        print("\nДоступные таблицы:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print("0. Вернуться в главное меню")
        
        choice = input("Выберите номер таблицы для редактирования (или 0 для выхода): ")
        
        if choice == '0':
            break
            
        try:
            table_index = int(choice) - 1
            if 0 <= table_index < len(tables):
                table = tables[table_index]
                edit_table(table)
            else:
                print("Неверный номер таблицы. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

if __name__ == "__main__":
    main()
