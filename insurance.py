import sqlite3
from tabulate import tabulate


with sqlite3.connect("base.db") as ton:
    cur = ton.cursor()

    cur.execute('SELECT * FROM insurance')

    per = cur.fetchall()

head = ["id", "policy_number", "provider", "start_date", "end_date", "vehicle_id"]

print(tabulate(per, headers = head, tablefmt="github"))