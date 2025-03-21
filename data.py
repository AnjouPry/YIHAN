import sqlite3

# 连接数据库（如果不存在则创建）
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# 创建 customers 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        telephone TEXT NOT NULL,
        pin TEXT NOT NULL
    )
""")

# 创建 accounts 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INTEGER PRIMARY KEY AUTOINCREMENT,
        cash_balance REAL NOT NULL,
        share_balance INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")

# 提交更改并关闭连接
conn.commit()
conn.close()
