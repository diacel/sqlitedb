import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

ton = sqlite3.connect("base.db")
cur = ton.cursor()

def register_user(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed_password, role))
        ton.commit()
        messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")

def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cur.fetchone()
    return user

def main():
    root = tk.Tk()
    root.title("Система управления пользователями")
    root.geometry("400x300")

    def login():
        username = username_entry.get()
        password = password_entry.get()
        user = authenticate_user(username, password)
        if user:
            messagebox.showinfo("Добро пожаловать", f"Добро пожаловать, {user[1]}!")
            if user[3] == 'admin':
                admin_menu()
            elif user[3] == 'super_admin':
                super_admin_menu()
            else:
                employee_menu()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")

    def admin_menu():
        menu_window = tk.Toplevel(root)
        menu_window.title("Admin Menu")
        tk.Button(menu_window, text="Просмотреть данные", command=lambda: view_data(['driver', 'vehicle', 'violation', 'insurance', 'maintenance'])).pack()
        tk.Button(menu_window, text="Редактировать данные", command=lambda: edit_data(['driver', 'vehicle', 'violation', 'insurance', 'maintenance'])).pack()
        tk.Button(menu_window, text="Выход", command=menu_window.destroy).pack()

    def super_admin_menu():
        menu_window = tk.Toplevel(root)
        menu_window.title("Super Admin Menu")
        tk.Button(menu_window, text="Просмотреть данные", command=lambda: view_data(['users', 'driver', 'vehicle', 'violation', 'insurance', 'maintenance'])).pack()
        tk.Button(menu_window, text="Редактировать данные", command=lambda: edit_data(['users', 'driver', 'vehicle', 'violation', 'insurance', 'maintenance'])).pack()
        tk.Button(menu_window, text="Зарегистрировать новый аккаунт", command=register_new_account).pack()
        tk.Button(menu_window, text="Выход", command=menu_window.destroy).pack()

    def employee_menu():
        menu_window = tk.Toplevel(root)
        menu_window.title("Employee Menu")
        tk.Button(menu_window, text="Просмотреть данные", command=lambda: view_data(['driver', 'vehicle', 'violation', 'insurance', 'maintenance'])).pack()
        tk.Button(menu_window, text="Выход", command=menu_window.destroy).pack()

    def view_data(tables):
        menu_window = tk.Toplevel(root)
        menu_window.title("Выбор таблицы")

        def show_table_data(table_name, filter_text=""):
            query = f"SELECT * FROM {table_name}"
            if filter_text:
                query += f" WHERE {filter_text}"
            cur.execute(query)
            data = cur.fetchall()
            headers = [col[1] for col in cur.execute(f"PRAGMA table_info({table_name})").fetchall()]
            show_table(headers, data)


        for table in tables:
            button = tk.Button(menu_window, text=f"Просмотреть {table}", command=lambda t=table: show_table_data(t))
            button.pack(pady=5)

        tk.Button(menu_window, text="Закрыть", command=menu_window.destroy).pack(pady=10)

    def show_table(headers, data):
        table_window = tk.Toplevel(root)
        table_window.title("Данные")
        tree = ttk.Treeview(table_window, columns=headers, show='headings')
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor='center')
        for row in data:
            tree.insert('', 'end', values=row)
        tree.pack(expand=True, fill='both')

    def edit_data(tables):
        table_name = simpledialog.askstring("Редактирование данных", "Введите имя таблицы (или выберите из: " + ", ".join(tables) + "):")
        if table_name in tables:
            edit_table(table_name)
        else:
            messagebox.showerror("Ошибка", "Неверное имя таблицы.")

    def edit_table(table):
        action = simpledialog.askstring("Редактирование", "Выберите действие: 1. Добавить 2. Изменить 3. Удалить")
        if action == '1':
            add_entry(table)
        elif action == '2':
            update_entry(table)
        elif action == '3':
            delete_entry(table)
        else:
            messagebox.showerror("Ошибка", "Неверный выбор действия.")

    def add_entry(table):
        values = simpledialog.askstring("Добавление записи", "Введите значения через запятую:")
        if values:
            cur.execute(f"INSERT INTO {table} VALUES ({', '.join(['?'] * len(values.split(',')))})", values.split(','))
            ton.commit()
            messagebox.showinfo("Успех", "Запись успешно добавлена.")

    def update_entry(table):
        id_value = simpledialog.askstring("Обновление записи", "Введите ID записи для обновления:")
        new_values = simpledialog.askstring("Обновление записи", "Введите новые значения через запятую:")
        if id_value and new_values:
            cur.execute(f"UPDATE {table} SET {', '.join([f'column_name = ?' for column_name in new_values.split(',')])} WHERE id = ?", (*new_values.split(','), id_value))
            ton.commit()
            messagebox.showinfo("Успех", "Запись успешно обновлена.")

    def delete_entry(table):
        id_value = simpledialog.askstring("Удаление записи", "Введите ID записи для удаления:")
        if id_value:
            cur.execute(f"DELETE FROM {table} WHERE id = ?", (id_value,))
            ton.commit()
            messagebox.showinfo("Успех", "Запись успешно удалена.")

    def register_new_account():
        def select_role(role):
            username = username_entry.get()
            password = password_entry.get()
            if username and password:
                register_user(username, password, role)
                role_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, введите имя пользователя и пароль.")

        role_window = tk.Toplevel(root)
        role_window.title("Регистрация нового аккаунта")

        tk.Label(role_window, text="Введите имя пользователя:").pack()
        username_entry = tk.Entry(role_window)
        username_entry.pack()

        tk.Label(role_window, text="Введите пароль:").pack()
        password_entry = tk.Entry(role_window, show='*')
        password_entry.pack()

        tk.Button(role_window, text="Admin", command=lambda: select_role('admin')).pack()
        tk.Button(role_window, text="Super Admin", command=lambda: select_role('super_admin')).pack()
        tk.Button(role_window, text="Employee", command=lambda: select_role('employee')).pack()

        tk.Button(role_window, text="Отмена", command=role_window.destroy).pack()

    username_label = tk.Label(root, text="Имя пользователя:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(root, show='*')
    password_entry.pack()

    tk.Button(root, text="Вход", command=login).pack()
    tk.Button(root, text="Выход", command=root.quit).pack()

    root.mainloop()

if __name__ == "__main__":
    main()