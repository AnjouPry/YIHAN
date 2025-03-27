import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import csv

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

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("银行管理系统")
        self.root.geometry("400x400")
        
        self.create_login_screen()
    
    def create_login_screen(self):
        """创建登录界面"""
        self.clear_screen()
        tk.Label(self.root, text="请输入您的客户 ID:").pack()
        self.customer_id_entry = tk.Entry(self.root)
        self.customer_id_entry.pack()
        
        tk.Label(self.root, text="请输入 PIN:").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()
        
        tk.Button(self.root, text="登录", command=self.verify_login).pack()
        tk.Button(self.root, text="管理员登录", command=self.create_admin_login_screen).pack()
    
    def verify_login(self):
        """验证客户 ID 和 PIN"""
        customer_id = self.customer_id_entry.get()
        pin = self.pin_entry.get()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id=? AND pin=?", (customer_id, pin))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.customer_id = customer_id
            self.create_main_menu()
        else:
            messagebox.showerror("错误", "无效的客户 ID 或 PIN")
    
    def create_admin_login_screen(self):
        """创建管理员登录界面"""
        self.clear_screen()
        tk.Label(self.root, text="管理员用户名:").pack()
        self.admin_username_entry = tk.Entry(self.root)
        self.admin_username_entry.pack()
        
        tk.Label(self.root, text="管理员密码:").pack()
        self.admin_password_entry = tk.Entry(self.root, show="*")
        self.admin_password_entry.pack()
        
        tk.Button(self.root, text="登录", command=self.verify_admin_login).pack()
        tk.Button(self.root, text="返回", command=self.create_login_screen).pack()
    
    def verify_admin_login(self):
        """验证管理员用户名和密码"""
        username = self.admin_username_entry.get()
        password = self.admin_password_entry.get()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.create_admin_menu()
        else:
            messagebox.showerror("错误", "管理员登录失败")
    
    def create_admin_menu(self):
        """创建管理员菜单"""
        self.clear_screen()
        tk.Button(self.root, text="添加客户", command=self.add_customer).pack()
        tk.Button(self.root, text="查看客户", command=self.view_customers).pack()
        tk.Button(self.root, text="更新客户", command=self.update_customer).pack()
        tk.Button(self.root, text="删除客户", command=self.delete_customer).pack()
        tk.Button(self.root, text="导入 CSV", command=self.import_csv).pack()
        tk.Button(self.root, text="返回", command=self.create_login_screen).pack()
    
    def import_csv(self):
        """从 CSV 文件导入客户数据"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            for row in reader:
                cursor.execute("INSERT INTO customers (name, address, telephone, pin) VALUES (?, ?, ?, ?)",
                               (row[0], row[1], row[2], row[3]))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("成功", "CSV 数据导入成功")
        self.create_admin_menu()
    
    def clear_screen(self):
        """清除当前界面组件"""
        for widget in self.root.winfo_children():
            widget.destroy()

# 运行 Tkinter GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
