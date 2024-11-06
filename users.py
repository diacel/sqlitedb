import sqlite3
from tabulate import tabulate


with sqlite3.connect("base.db") as ton:
    cur = ton.cursor()

    cur.execute('SELECT * FROM users')

    per = cur.fetchall()

head = ["id", "username", "password", "role"]

print(tabulate(per, headers = head, tablefmt="github"))