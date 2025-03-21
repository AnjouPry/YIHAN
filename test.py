import sqlite3

class Account:
    def __init__(self, account_number, cash_balance, share_balance, customer_id, pin):
        self.account_number = account_number
        self.cash_balance = cash_balance
        self.share_balance = share_balance
        self.customer_id = customer_id
        self.pin = pin

    def update_database(self):
        """更新账户信息到数据库"""
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE accounts SET cash_balance=?, share_balance=? WHERE account_number=?
        """, (self.cash_balance, self.share_balance, self.account_number))
        conn.commit()
        conn.close()

    def verify_pin(self, pin):
        """验证 PIN 码。"""
        return self.pin == pin

    def withdraw(self, amount, pin):
        """提款：如果资金充足，客户可以提取现金，并更新数据库。"""
        if not self.verify_pin(pin):
            return False  # PIN 验证失败
        if amount > self.cash_balance:
            return False  # 余额不足
        self.cash_balance -= amount
        self.update_database()
        return True

    def deposit(self, amount, pin):
        """存款：客户可以存款，并更新数据库。"""
        if not self.verify_pin(pin):
            return False  # PIN 验证失败
        self.cash_balance += amount
        self.update_database()
        return True

    def check_balance(self, pin):
        """余额查询：返回现金和股票余额。"""
        if not self.verify_pin(pin):
            return False  # PIN 验证失败
        return {
            "cash_balance": self.cash_balance,
            "share_balance": self.share_balance
        }

    def buy_shares(self, price_per_share, quantity, pin):
        """购买股票：如果现金余额充足，客户可以购买股票。"""
        if not self.verify_pin(pin):
            return False  # PIN 验证失败
        total_cost = price_per_share * quantity
        if total_cost > self.cash_balance:
            return False  # 资金不足
        self.cash_balance -= total_cost
        self.share_balance += quantity
        self.update_database()
        return True

    def sell_shares(self, price_per_share, quantity, pin):
        """出售股票：客户可以出售股票，并将收益存入现金余额。"""
        if not self.verify_pin(pin):
            return False  # PIN 验证失败
        if quantity > self.share_balance:
            return False  # 股票数量不足
        self.share_balance -= quantity
        self.cash_balance += price_per_share * quantity
        self.update_database()
        return True

# SQLite 数据库初始化
def initialize_database():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            telephone TEXT NOT NULL,
            pin TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY,
            cash_balance REAL NOT NULL,
            share_balance INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    conn.commit()
    conn.close()

# 运行数据库初始化函数
initialize_database()
