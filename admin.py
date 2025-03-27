import sqlite3

# 指定 SQLite 数据库文件路径
db_path = r"C:\Users\Anjou\bank.db"

# 初始化数据库，添加管理员表
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")
conn.commit()
conn.close()