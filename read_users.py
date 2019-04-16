# Grabs users from existing databse
import sqlite3


conn = sqlite3.connect('instance/randres.sqlite')
cur = conn.cursor()

users = cur.execute("SELECT * FROM user").fetchall()
for row in users:
	print(row)
