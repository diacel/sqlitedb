import sqlite3
from tabulate import tabulate


with sqlite3.connect("base.db") as ton:
    cur = ton.cursor()

    cur.execute('SELECT * FROM driver')

    per = cur.fetchall()

head = ["id", "full_name", "birth_date", "city", "license_number", "license_issue_date", "license_expiration_date",]

print(tabulate(per, headers = head, tablefmt="github"))