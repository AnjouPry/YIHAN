import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import csv

# Specifies the SQLite database file path.
db_path = r"C:\Users\Anjou\bank.db"

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Share Management System")
        self.root.geometry("400x400")
        
        self.create_login_screen()
    
    def create_login_screen(self):
        """Creating a login screen."""
        self.clear_screen()
        tk.Label(self.root, text="Please enter your customer ID:").pack()
        self.customer_id_entry = tk.Entry(self.root)
        self.customer_id_entry.pack()
        
        tk.Label(self.root, text="Please enter your PIN:").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()
        
        tk.Button(self.root, text="Login", command=self.verify_login).pack()
        tk.Button(self.root, text="Manage", command=self.create_admin_login_screen).pack()
    
    def verify_login(self):
        """Verify customer ID and PIN."""
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
            messagebox.showerror("Error", "Invalid customer ID or PIN.")
    
    def create_admin_login_screen(self):
        """Create admin login screen."""
        self.clear_screen()
        tk.Label(self.root, text="Admin ID:").pack()
        self.admin_username_entry = tk.Entry(self.root)
        self.admin_username_entry.pack()
        
        tk.Label(self.root, text="Admin Password:").pack()
        self.admin_password_entry = tk.Entry(self.root, show="*")
        self.admin_password_entry.pack()
        
        tk.Button(self.root, text="Login", command=self.verify_admin_login).pack()
        tk.Button(self.root, text="Back", command=self.create_login_screen).pack()
    
    def verify_admin_login(self):
        """Verify admin login."""
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
            messagebox.showerror("Error", "Admin login failed.")

    def create_main_menu(self):
        """Create main menu."""
        self.clear_screen()
        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack()
        tk.Button(self.root, text="Deposit", command=self.deposit).pack()
        tk.Button(self.root, text="Withdraw", command=self.withdraw).pack()
        tk.Button(self.root, text="Buy Shares", command=self.buy_shares).pack()
        tk.Button(self.root, text="Sell Shares", command=self.sell_shares).pack()
        tk.Button(self.root, text="Quit", command=self.root.quit).pack()
    
    def create_admin_menu(self):
        """Create admin menu."""
        self.clear_screen()
        tk.Button(self.root, text="Add Customer", command=self.add_customer).pack()
        tk.Button(self.root, text="View Customers", command=self.view_customers).pack()
        tk.Button(self.root, text="Update Customer", command=self.update_customer).pack()
        tk.Button(self.root, text="Delete Customer", command=self.delete_customer).pack()
        tk.Button(self.root, text="Import CSV", command=self.import_csv).pack()
        tk.Button(self.root, text="Back", command=self.create_login_screen).pack()
    
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
    
    def add_customer(self):
        """Add a new customer."""
        self.clear_screen()
        tk.Label(self.root, text="Name:").pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()
        tk.Label(self.root, text="Address:").pack()
        address_entry = tk.Entry(self.root)
        address_entry.pack()
        tk.Label(self.root, text="Telephone:").pack()
        phone_entry = tk.Entry(self.root)
        phone_entry.pack()
        tk.Label(self.root, text="PIN:").pack()
        pin_entry = tk.Entry(self.root, show="*")
        pin_entry.pack()
        
        def save_customer():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (name, address, telephone, pin) VALUES (?, ?, ?, ?)",
                           (name_entry.get(), address_entry.get(), phone_entry.get(), pin_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Add customer successfully!")
            self.create_admin_menu()
        
        tk.Button(self.root, text="Save", command=save_customer).pack()
        tk.Button(self.root, text="Back", command=self.create_admin_menu).pack()
    
    def import_csv(self):
        """Import customers from CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Jump over the first line.
            for row in reader:
                cursor.execute("INSERT INTO customers (name, address, telephone, pin) VALUES (?, ?, ?, ?)",
                               (row[0], row[1], row[2], row[3]))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Import customers successfully!")
        self.create_admin_menu()
    
    def clear_screen(self):
        """Clear the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
