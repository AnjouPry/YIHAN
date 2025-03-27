import sqlite3

# 指定 SQLite 数据库文件路径
db_path = r"C:\Users\Anjou\bank.db"

# 初始化数据库，添加管理员表
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

admin_data = [
    (1, 'admin', 'admin123'),
    (2, 'manager', 'manager456'),
    (3, 'supervisor', 'super789')
]

cursor.executemany("""
    INSERT OR IGNORE INTO admins (admin_id, username, password)
    VALUES (?, ?, ?)
""", admin_data)

conn.commit()
conn.close()