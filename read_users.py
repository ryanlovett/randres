# Grabs users from existing databse
import squlite


conn = sqlite3.connect('instance/randres.sqlite')
cur = conn.cursor()

users = cur.exectute("SELECTION * FROM users").fetchall()
for row in users:
	print(row)
