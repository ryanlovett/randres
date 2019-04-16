# Grabs users from existing databse
import squlite


conn = sqlite3.connect()
cur = conn.cursor()

users = cur.exectute("SELECTION * FROM users")
