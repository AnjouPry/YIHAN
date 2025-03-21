import sqlite3

from tkinter import Tk, Label, Entry, Button

# 定义 Customer 类

class Customer:
    def __init__(self, customer_id, name, address, telephone, pin):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.telephone = telephone
        self.pin = pin

    # ... 其他方法 ...

# 定义 Account 类

class Account:
    def __init__(self, account_number, cash_balance, share_balance, customer_id):
        self.account_number = account_number
        self.cash_balance = cash_balance
        self.share_balance = share_balance
        self.customer_id = customer_id

    def withdraw(self, amount):
        # 检查余额是否充足

        if amount > self.cash_balance:

            return False  # 余额不足

        else:

            # 更新现金余额

            self.cash_balance -= amount

            # 更新数据库

            # ... (数据库更新代码) ...

            return True

# 登录界面

def login():

    # 连接数据库

    conn = sqlite3.connect("CUBS_Investment.sqlite")

    c = conn.cursor()

    # 获取用户输入

    customer_id = customer_id_entry.get()

    pin = pin_entry.get()

    # 查询数据库，验证 PIN

    c.execute("SELECT * FROM Customer WHERE Customer_ID = ? AND Pin = ?", (customer_id, pin))

    customer = c.fetchone()

    # 如果 PIN 验证成功，显示主界面

    if customer:

        # 创建 Customer 对象

        customer_obj = Customer(*customer)

        # ... 显示主界面 ...

    else:

        # 显示错误消息

        # ...

    # 关闭数据库连接

    conn.close()

def withdraw_dialog(account):

    # ... (创建对话框代码) ...

    # 获取用户输入的金额

    amount = float(amount_entry.get())

    # 尝试提款

    if account.withdraw(amount):

        # 显示成功消息

        # ...

    else:

        # 显示余额不足消息

        # ...

    # 关闭对话框

    withdraw_window.destroy()


# 创建主窗口

root = Tk()

root.title("CUBS Investment Bank")

# 添加标签和输入框

welcome_label = Label(root, text="Welcome to CUBS Investment Bank")

welcome_label.pack()

customer_id_label = Label(root, text="Customer ID:")

customer_id_label.pack()

customer_id_entry = Entry(root)

customer_id_entry.pack()

pin_label = Label(root, text="PIN:")

pin_label.pack()

pin_entry = Entry(root)

pin_entry.pack()

# 添加登录按钮

login_button = Button(root, text="Login", command=login)

login_button.pack()

# 运行主循环

root.mainloop()

