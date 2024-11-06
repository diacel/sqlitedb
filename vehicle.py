import sqlite3
from tabulate import tabulate


with sqlite3.connect("base.db") as ton:
    cur = ton.cursor()

    cur.execute('SELECT * FROM vehicle')

    per = cur.fetchall()

head = ["id", "brand", "model", "vin", "license_plate", "driver_id"]

print(tabulate(per, headers = head, tablefmt="github"))