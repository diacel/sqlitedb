import sqlite3
from tabulate import tabulate


with sqlite3.connect("base.db") as ton:
    cur = ton.cursor()

    cur.execute('SELECT * FROM maintenance')

    per = cur.fetchall()

head = ["id", "vehicle_id", "maintenance_date", "description", "cost",]

print(tabulate(per, headers = head, tablefmt="github"))