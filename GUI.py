import tkinter as tk
from tkinter import messagebox
import sqlite3

# 指定 SQLite 数据库文件路径
db_path = r"C:\Users\Anjou\bank.db"

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("银行管理系统")
        self.root.geometry("400x300")
        
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
    
    def create_main_menu(self):
        """创建主菜单界面"""
        self.clear_screen()
        tk.Button(self.root, text="查看余额", command=self.check_balance).pack()
        tk.Button(self.root, text="存款", command=self.deposit).pack()
        tk.Button(self.root, text="提款", command=self.withdraw).pack()
        tk.Button(self.root, text="购买股票", command=self.buy_shares).pack()
        tk.Button(self.root, text="出售股票", command=self.sell_shares).pack()
        tk.Button(self.root, text="退出", command=self.root.quit).pack()
    
    def check_balance(self):
        """查询账户余额"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cash_balance, share_balance FROM accounts WHERE customer_id=?", (self.customer_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            messagebox.showinfo("账户余额", f"现金余额: {result[0]}\n股票余额: {result[1]}")
        else:
            messagebox.showerror("错误", "账户未找到")
    
    def deposit(self):
        """存款功能"""
        self.transaction_screen("存款", "请输入存款金额:", self.process_deposit)
    
    def withdraw(self):
        """提款功能"""
        self.transaction_screen("提款", "请输入提款金额:", self.process_withdraw)
    
    def buy_shares(self):
        """购买股票"""
        self.transaction_screen("购买股票", "请输入购买股票数量:", self.process_buy_shares)
    
    def sell_shares(self):
        """出售股票"""
        self.transaction_screen("出售股票", "请输入出售股票数量:", self.process_sell_shares)
    
    def transaction_screen(self, title, label_text, command):
        """通用交易界面"""
        self.clear_screen()
        tk.Label(self.root, text=label_text).pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        tk.Button(self.root, text=title, command=command).pack()
        tk.Button(self.root, text="返回", command=self.create_main_menu).pack()
    
    def process_deposit(self):
        """处理存款"""
        amount = float(self.amount_entry.get())
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET cash_balance = cash_balance + ? WHERE customer_id=?", (amount, self.customer_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("成功", "存款成功")
        self.create_main_menu()
    
    def process_withdraw(self):
        """处理提款"""
        amount = float(self.amount_entry.get())
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cash_balance FROM accounts WHERE customer_id=?", (self.customer_id,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute("UPDATE accounts SET cash_balance = cash_balance - ? WHERE customer_id=?", (amount, self.customer_id))
            conn.commit()
            messagebox.showinfo("成功", "提款成功")
        else:
            messagebox.showerror("错误", "余额不足")
        conn.close()
        self.create_main_menu()
    
    def process_buy_shares(self):
        """处理购买股票"""
        quantity = int(self.amount_entry.get())
        price_per_share = 1  # 设定股票单价
        self.process_withdraw(price_per_share * quantity)
    
    def process_sell_shares(self):
        """处理出售股票"""
        quantity = int(self.amount_entry.get())
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT share_balance FROM accounts WHERE customer_id=?", (self.customer_id,))
        result = cursor.fetchone()
        if result and result[0] >= quantity:
            cursor.execute("UPDATE accounts SET share_balance = share_balance - ?, cash_balance = cash_balance + ? WHERE customer_id=?", (quantity, quantity, self.customer_id))
            conn.commit()
            messagebox.showinfo("成功", "股票出售成功")
        else:
            messagebox.showerror("错误", "股票数量不足")
        conn.close()
        self.create_main_menu()
    
    def clear_screen(self):
        """清除当前界面组件"""
        for widget in self.root.winfo_children():
            widget.destroy()

# 运行 Tkinter GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
