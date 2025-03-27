import sqlite3

# 指定 SQLite 数据库文件路径
db_path = r"C:\Users\Anjou\bank.db"

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 插入示例客户数据
customers_data = [
    ("Alice Johnson", "123 Main St, Springfield", "(021)12345678", "1111"),
    ("Bob Smith", "456 Oak St, Metropolis", "(021)87654321", "2222"),
    ("Charlie Brown", "789 Pine St, Gotham", "(021)55555555", "3333")
]

cursor.executemany("""
    INSERT INTO customers (name, address, telephone, pin) VALUES (?, ?, ?, ?)
""", customers_data)

# 获取插入的 customer_id
cursor.execute("SELECT customer_id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]

# 确保有足够的 customer_id
if len(customer_ids) >= 3:
    accounts_data = [
        (1000.0, 50, customer_ids[0]),
        (2000.0, 100, customer_ids[1]),
        (500.0, 20, customer_ids[2])
    ]

    cursor.executemany("""
        INSERT INTO accounts (cash_balance, share_balance, customer_id) VALUES (?, ?, ?)
    """, accounts_data)

# 提交更改并关闭连接
conn.commit()
conn.close()
