import sqlite3

# 指定 SQLite 数据库文件路径
db_path = r"C:\Users\Anjou\bank.db"

# 连接数据库（如果不存在则创建）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

'''# 创建 customers 表
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
""")'''

# 创建 stocks 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_name TEXT NOT NULL,
        stock_symbol TEXT NOT NULL UNIQUE,
        stock_price REAL NOT NULL
    )
""")

# 插入示例股票数据
stocks_data = [
    ("Apple Inc.", "AAPL", 150.0),
    ("Microsoft Corp.", "MSFT", 280.0),
    ("Tesla Inc.", "TSLA", 750.0),
    ("Amazon.com Inc.", "AMZN", 3300.0),
    ("Google LLC", "GOOGL", 2800.0)
]

cursor.executemany("""
    INSERT OR IGNORE INTO stocks (stock_name, stock_symbol, stock_price) VALUES (?, ?, ?)
""", stocks_data)

# 提交更改并关闭连接
conn.commit()
conn.close()
