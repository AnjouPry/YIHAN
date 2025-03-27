import sqlite3

db_path = r"C:\Users\Anjou\bank.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")
print("Customers:", cursor.fetchall())

cursor.execute("SELECT * FROM accounts")
print("Accounts:", cursor.fetchall())

conn.close()
