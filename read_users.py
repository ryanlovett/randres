# Grabs users from existing databse
import sqlite3

conn = sqlite3.connect('instance/randres.sqlite')
cur = conn.cursor()

users = cur.execute("SELECT * FROM user").fetchall()
for row in users:
	print(row)

apps = cur.execute("SELECT * FROM app").fetchall()
for row in apps:
	print(row)	

whist = cur.execute("SELECT app_id, employer, position FROM work_hist").fetchall()
for row in whist:
	print(row)	