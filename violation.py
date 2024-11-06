import sqlite3
from tabulate import tabulate


with sqlite3.connect("base.db") as ton:
    cur = ton.cursor()

    cur.execute('SELECT * FROM violation')

    per = cur.fetchall()

head = ["id", "dt_violation", "city", "description", "license_plate", "fine_amount", "driver_id", "vehicle_id"]

print(tabulate(per, headers = head, tablefmt="github"))