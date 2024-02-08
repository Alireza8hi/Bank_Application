import database_connector
import tkinter as tk
from tkinter import ttk
import hashlib
from datetime import datetime, date

import email_phone_number

global root


def on_closing():
    database_connector.disconnect_to_mysql()
    root.destroy()


def go_back(parent_page, page):
    parent_page.deiconify()
    page.destroy()


def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry('{width}x{height}+{x}+{y}'.format(width=width, height=height, x=x, y=y))


def login_page(parent_page):
    parent_page.withdraw()
    login_window = tk.Toplevel(parent_page)
    login_window.title("صفحه ورود")
    center_window(login_window, 300, 200)

    username_label = tk.Label(login_window, text="نام کاربری:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="رمز عبور:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="ورود",
                             command=lambda: login(login_window, username_entry.get(),
                                                   password_entry.get()))
    login_button.config(width=8)
    login_button.pack(pady=10)

    back_button = tk.Button(login_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, login_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    login_window.protocol("WM_DELETE_WINDOW", on_closing)


def register_page(parent_page):
    parent_page.withdraw()
    register_window = tk.Toplevel(parent_page)
    register_window.title("صفحه ثبت نام")
    center_window(register_window, 400, 300)

    button_frame1 = tk.Frame(register_window)
    button_frame1.pack()

    button_frame2 = tk.Frame(register_window)
    button_frame2.pack()

    button_frame3 = tk.Frame(register_window)
    button_frame3.pack()

    button_frame4 = tk.Frame(register_window)
    button_frame4.pack()

    button_frame5 = tk.Frame(register_window)
    button_frame5.pack()

    button_frame6 = tk.Frame(register_window)
    button_frame6.pack()

    button_frame7 = tk.Frame(register_window)
    button_frame7.pack()

    username_label = tk.Label(button_frame1, text="نام کاربری:")
    username_label.pack()
    username_entry = tk.Entry(button_frame1)
    username_entry.pack()

    first_name_label = tk.Label(button_frame2, text="نام:")
    first_name_label.pack(side=tk.RIGHT, padx=50)
    first_name_entry = tk.Entry(button_frame3)
    first_name_entry.pack(side=tk.RIGHT, padx=10)

    last_name_label = tk.Label(button_frame2, text="نام خانوادگی:")
    last_name_label.pack(side=tk.LEFT, padx=50)
    last_name_entry = tk.Entry(button_frame3)
    last_name_entry.pack(side=tk.LEFT, padx=10)

    password_label = tk.Label(button_frame4, text="رمز عبور:")
    password_label.pack(side=tk.RIGHT, padx=50)
    password_entry = tk.Entry(button_frame5, show="*")
    password_entry.pack(side=tk.RIGHT, padx=10)

    r_password_label = tk.Label(button_frame4, text="تکرار رمز عبور:")
    r_password_label.pack(side=tk.LEFT, padx=50)
    r_password_entry = tk.Entry(button_frame5, show="*")
    r_password_entry.pack(side=tk.LEFT, padx=10)

    phone_number_label = tk.Label(button_frame6, text="شماره همراه:")
    phone_number_label.pack(side=tk.RIGHT, padx=50)
    phone_number_entry = tk.Entry(button_frame7)
    phone_number_entry.pack(side=tk.RIGHT, padx=10)

    email_label = tk.Label(button_frame6, text="آدرس ایمیل:")
    email_label.pack(side=tk.LEFT, padx=50)
    email_entry = tk.Entry(button_frame7)
    email_entry.pack(side=tk.LEFT, padx=10)

    register_button = tk.Button(register_window, text="ثبت نام",
                                command=lambda: register(register_window, username_entry.get(), first_name_entry.get(),
                                                         last_name_entry.get(), password_entry.get(),
                                                         r_password_entry.get(), phone_number_entry.get(),
                                                         email_entry.get()))
    register_button.config(width=8)
    register_button.pack(pady=10)

    back_button = tk.Button(register_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, register_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    register_window.protocol("WM_DELETE_WINDOW", on_closing)


def admin_select_page(parent_page, user_id):
    def go_to_user_page():
        message_window.destroy()
        user_page(parent_page, user_id)

    def go_to_admin_page():
        message_window.destroy()
        admin_page(parent_page, user_id)

    parent_page.withdraw()

    message_window = tk.Toplevel(parent_page)
    message_window.title("صفحه انتخاب پنل")
    center_window(message_window, 200, 120)

    message_label = tk.Label(message_window, text="پنل مورد نظر را انتخاب کنید!")
    message_label.pack()

    user_page_button = tk.Button(message_window, text="پنل کاربری", command=go_to_user_page)
    user_page_button.config(width=8)
    user_page_button.pack()

    admin_page_button = tk.Button(message_window, text="پنل مدیریت", command=go_to_admin_page)
    admin_page_button.config(width=8)
    admin_page_button.pack()

    back_button = tk.Button(message_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, message_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    message_window.protocol("WM_DELETE_WINDOW", on_closing)


def login(parent_page, username, password):
    hash_object = hashlib.sha256()
    password_bytes = password.encode('utf-8')
    hash_object.update(password_bytes)
    hashed_password = hash_object.hexdigest()
    user_id = database_connector.login(username, hashed_password)
    if user_id == None:
        user_id = 0
    is_admin = database_connector.check_admin(user_id)
    if not len(username) or not len(password):
        error_label = tk.Label(parent_page, text="نام کاربری و رمز عبور را وارد کنید!")
        error_label.pack()
    elif user_id == 0:
        error_label = tk.Label(parent_page, text="نام کاربری یا رمز عبور صحیح نیست!")
        error_label.pack()
    elif is_admin:
        admin_select_page(parent_page, user_id)
    else:
        user_page(parent_page, user_id)


def register(parent_page, username, first_name, last_name, password, r_password, phone_number, email):
    check_username = database_connector.check_username(username)
    check_phone_number = database_connector.check_phone_number(phone_number)
    check_email = database_connector.check_email(email)

    if not len(username) or not len(first_name) or not len(last_name) or not len(password) or not len(
            r_password) or not len(phone_number) or not len(email):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif len(password) < 8:
        error_label = tk.Label(parent_page, text="طول رمزعبور باید حداقل 8 کارکتر باشد!")
        error_label.pack()
    elif password != r_password:
        error_label = tk.Label(parent_page, text="رمز عبور ها یکسان نیست!")
        error_label.pack()
    elif not check_username:
        error_label = tk.Label(parent_page, text="این نام کاربری قبلا استفاده شده است!")
        error_label.pack()
    elif not check_phone_number:
        error_label = tk.Label(parent_page, text="شماره وارد شده نامعتبر است!")
        error_label.pack()
    elif not check_email:
        error_label = tk.Label(parent_page, text="ایمیل وارد شده نامعتبر است!")
        error_label.pack()
    else:
        hash_object = hashlib.sha256()
        password_bytes = password.encode('utf-8')
        hash_object.update(password_bytes)
        hashed_password = hash_object.hexdigest()
        done = database_connector.register(username, first_name, last_name, email, phone_number, hashed_password)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 150, 50)

            message_label = tk.Label(message_window, text="ثبت نام با موفقیت انجام شد!")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            root.destroy()
            root_page()
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در ثبت نام پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def get_accounts_page(parent_page, user_id):
    parent_page.withdraw()
    get_accounts_window = tk.Toplevel(parent_page)
    get_accounts_window.title("صفحه دریافت لیست تمام حساب ها")
    center_window(get_accounts_window, 1450, 400)

    table = tk.ttk.Treeview(get_accounts_window)

    table["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")

    table.heading("col1", text="شماره حساب")
    table.heading("col2", text="تاریخ ایجاد")
    table.heading("col3", text="موجودی")
    table.heading("col4", text="وام فعال")
    table.heading("col5", text="تاریخ مسدودیت")
    table.heading("col6", text="دلیل مسدودیت")

    data = database_connector.get_accounts(user_id)

    for x in range(len(data)):
        data[x] = list(data[x])
        if data[x][3] is None:
            data[x][3] = "ندارد"
        else:
            data[x][3] = "دارد"
        if data[x][4] is None:
            data[x][4] = "--"
            data[x][5] = "--"

    for record in data:
        table.insert("", tk.END, values=record)

    print(table)
    table.pack()

    back_button = tk.Button(get_accounts_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, get_accounts_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    get_accounts_window.protocol("WM_DELETE_WINDOW", on_closing)


def transaction(user_window, parent_page, source_account_number, destination_account_number, amount, user_id):
    if not len(source_account_number) or not len(destination_account_number) or not len(amount):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif not source_account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب مبدا نامعتبر است!")
        error_label.pack()
    elif not destination_account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب مقصد نامعتبر است!")
        error_label.pack()
    elif not database_connector.check_account_number(source_account_number):
        error_label = tk.Label(parent_page, text="شماره حساب مبدا نامعتبر است!")
        error_label.pack()
    elif not database_connector.check_account_number(destination_account_number):
        error_label = tk.Label(parent_page, text="شماره حساب مقصد نامعتبر است!")
        error_label.pack()
    elif not amount.isnumeric() or int(amount) <= 0:
        error_label = tk.Label(parent_page, text="مقدار پول نامعتبر است!")
        error_label.pack()
    elif not database_connector.check_amount(amount, user_id, source_account_number):
        error_label = tk.Label(parent_page, text="مقدار پول نامعتبر است!")
        error_label.pack()
    elif not database_connector.check_block_account(user_id, source_account_number):
        error_label = tk.Label(parent_page, text="شماره حساب مبدا مسدود است!")
        error_label.pack()
    elif not database_connector.check_block_account(user_id, destination_account_number):
        error_label = tk.Label(parent_page, text="شماره حساب مقصد مسدود است!")
        error_label.pack()
    elif source_account_number == destination_account_number:
        error_label = tk.Label(parent_page, text="شماره حساب مبدا و مقصد یکسان است!")
        error_label.pack()
    else:
        done = database_connector.money_transfer(user_id, source_account_number, destination_account_number, amount)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 150, 260)

            source_name = database_connector.get_full_name(source_account_number)
            destination_name = database_connector.get_full_name(destination_account_number)

            message_label = tk.Label(message_window, text="انتقال وجه با موفقیت انجام شد")
            message_label.pack()
            message_label = tk.Label(message_window, text="شماره حساب مبدا:")
            message_label.pack()
            message_label = tk.Label(message_window, text=f"{source_account_number}")
            message_label.pack()
            message_label = tk.Label(message_window, text="نام واریز کننده:")
            message_label.pack()
            message_label = tk.Label(message_window, text=f"{source_name}")
            message_label.pack()
            message_label = tk.Label(message_window, text="شماره حساب مقصد:")
            message_label.pack()
            message_label = tk.Label(message_window, text=f"{destination_account_number}")
            message_label.pack()
            message_label = tk.Label(message_window, text="نام دریافت کننده:")
            message_label.pack()
            message_label = tk.Label(message_window, text=f"{destination_name}")
            message_label.pack()
            message_label = tk.Label(message_window, text="مبلغ واریزی:")
            message_label.pack()
            message_label = tk.Label(message_window, text=f"{amount}")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            go_back(user_window, parent_page)
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در انتقال وجه پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def transaction_page(user_window, user_id):
    user_window.withdraw()
    transaction_window = tk.Toplevel(user_window)
    transaction_window.title("صفحه انتقال وجه")
    center_window(transaction_window, 300, 200)

    source_account_number_label = tk.Label(transaction_window, text="شماره حساب مبدا:")
    source_account_number_label.pack()
    source_account_number_entry = tk.Entry(transaction_window)
    source_account_number_entry.pack()

    destination_account_number_label = tk.Label(transaction_window, text="شماره حساب مقصد:")
    destination_account_number_label.pack()
    destination_account_number_entry = tk.Entry(transaction_window)
    destination_account_number_entry.pack()

    amount_label = tk.Label(transaction_window, text="مقدار پول:")
    amount_label.pack()
    amount_entry = tk.Entry(transaction_window)
    amount_entry.pack()

    transaction_button = tk.Button(transaction_window,
                                   text="تایید پرداخت",
                                   command=lambda: transaction(user_window, transaction_window,
                                                               source_account_number_entry.get(),
                                                               destination_account_number_entry.get(),
                                                               amount_entry.get(), user_id))
    transaction_button.config(width=8)
    transaction_button.pack()

    back_button = tk.Button(transaction_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(user_window, transaction_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    transaction_window.protocol("WM_DELETE_WINDOW", on_closing)


def result_transactions_page(parent_page, result):
    parent_page.withdraw()
    show_transactions_window = tk.Toplevel(parent_page)
    show_transactions_window.title("صفحه نمایش گردش حساب اخیر")
    center_window(show_transactions_window, 1050, 400)

    table = tk.ttk.Treeview(show_transactions_window)

    table["columns"] = ("col1", "col2", "col3", "col4")

    table.heading("col1", text="شماره حساب مبدا")
    table.heading("col2", text="شماره حساب مقصد")
    table.heading("col3", text="مقدار وجه")
    table.heading("col4", text="تاریخ انتقال")

    for record in result:
        table.insert("", tk.END, values=record)

    print(table)
    table.pack()

    back_button = tk.Button(show_transactions_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, show_transactions_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    show_transactions_window.protocol("WM_DELETE_WINDOW", on_closing)


def recent_transactions(parent_page, account_number, number, user_id):
    if not len(account_number) or not len(number):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif not account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
        error_label.pack()
    elif not (number.isnumeric()) or int(number) <= 0:
        error_label = tk.Label(parent_page, text="تعداد تراکنش وارد شده نامعتبر است!")
        error_label.pack()
    else:
        check_account_number = database_connector.check_account_number(account_number)
        if not check_account_number:
            error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
            error_label.pack()
        result = database_connector.get_recent_transactions(user_id, account_number, number)

        result_transactions_page(parent_page, result)


def get_recent_transactions_page(user_window, user_id):
    user_window.withdraw()
    recent_transactions_window = tk.Toplevel(user_window)
    recent_transactions_window.title("صفحه گردش حساب اخیر")
    center_window(recent_transactions_window, 300, 200)

    account_number_label = tk.Label(recent_transactions_window, text="شماره حساب مورد نظر:")
    account_number_label.pack()
    account_number_entry = tk.Entry(recent_transactions_window)
    account_number_entry.pack()

    recent_transactions_label = tk.Label(recent_transactions_window, text="تعداد تراکنش های اخیر برای مشاهده:")
    recent_transactions_label.pack()
    recent_transactions_entry = tk.Entry(recent_transactions_window)
    recent_transactions_entry.pack()

    recent_transactions_button = tk.Button(recent_transactions_window,
                                           text="تایید",
                                           command=lambda: recent_transactions(recent_transactions_window,
                                                                               account_number_entry.get(),
                                                                               recent_transactions_entry.get(),
                                                                               user_id))
    recent_transactions_button.config(width=8)
    recent_transactions_button.pack()

    back_button = tk.Button(recent_transactions_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(user_window, recent_transactions_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    recent_transactions_window.protocol("WM_DELETE_WINDOW", on_closing)


def period_transactions(parent_page, account_number, start_date, end_date, user_id):
    if not len(account_number) or not len(start_date) or not len(end_date):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif not account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
        error_label.pack()
    else:
        check_account_number = database_connector.check_account_number(account_number)
        start_date_check = start_date.split("/")
        end_date_check = end_date.split("/")
        len_dates_check = len(start_date_check) == 3 and len(end_date_check) == 3
        numeric_dates_check = start_date_check[0].isnumeric() and end_date_check[0].isnumeric() and start_date_check[
            1].isnumeric() and end_date_check[1].isnumeric() and start_date_check[2].isnumeric() and end_date_check[
                                 2].isnumeric()
        if not check_account_number:
            error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
            error_label.pack()
        elif not len_dates_check or not numeric_dates_check or not int(start_date_check[0]) > 0 or not 12 >= int(start_date_check[1]) > 0 or not 31 >= int(start_date_check[2]) > 0 or not int(end_date_check[0]) > 0 or not 12 >= int(end_date_check[1]) > 0 or not 31 >= int(end_date_check[2]) > 0:
            error_label = tk.Label(parent_page, text="تاریخ وارد شده نامعتبر است!")
            error_label.pack()
        else:
            start_date = datetime.strptime(start_date, "%Y/%m/%d").date()
            end_date = datetime.strptime(end_date, "%Y/%m/%d").date()
            result = database_connector.get_period_transactions(user_id, account_number, start_date, end_date)
            result_transactions_page(parent_page, result)


def get_period_transactions_page(user_window, user_id):
    user_window.withdraw()
    period_transactions_window = tk.Toplevel(user_window)
    period_transactions_window.title("صفحه گردش حساب اخیر")
    center_window(period_transactions_window, 300, 200)

    account_number_label = tk.Label(period_transactions_window, text="شماره حساب مورد نظر:")
    account_number_label.pack()
    account_number_entry = tk.Entry(period_transactions_window)
    account_number_entry.pack()

    start_date_transactions_label = tk.Label(period_transactions_window, text="تاریخ شروع(yyyy/mm/dd):")
    start_date_transactions_label.pack()
    start_date_transactions_entry = tk.Entry(period_transactions_window)
    start_date_transactions_entry.pack()

    end_date_transactions_label = tk.Label(period_transactions_window, text="تاریخ پایان(yyyy/mm/dd):")
    end_date_transactions_label.pack()
    end_date_transactions_entry = tk.Entry(period_transactions_window)
    end_date_transactions_entry.pack()

    period_transactions_button = tk.Button(period_transactions_window,
                                           text="تایید",
                                           command=lambda: period_transactions(period_transactions_window,
                                                                               account_number_entry.get(),
                                                                               start_date_transactions_entry.get(),
                                                                               end_date_transactions_entry.get(),
                                                                               user_id))
    period_transactions_button.config(width=8)
    period_transactions_button.pack()

    back_button = tk.Button(period_transactions_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(user_window, period_transactions_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    period_transactions_window.protocol("WM_DELETE_WINDOW", on_closing)


def block_account(user_window, parent_page, account_number, reason, user_id):
    if not len(account_number) or not len(reason):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif not account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
        error_label.pack()
    else:
        check_account_number = database_connector.check_account_number(account_number)
        check_block_account = database_connector.check_block_account(user_id, account_number)
        if not check_account_number:
            error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
            error_label.pack()
        elif not check_block_account:
            error_label = tk.Label(parent_page, text="این حساب از قبل مسدود شده است!")
            error_label.pack()

        done = database_connector.block_account(user_id, account_number, reason)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 200, 50)

            message_label = tk.Label(message_window, text="مسدود کردن حساب با موفقیت انجام شد!")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            go_back(user_window, parent_page)
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def block_account_page(user_window, user_id):
    user_window.withdraw()
    block_account_window = tk.Toplevel(user_window)
    block_account_window.title("صفحه مسدود کردن حساب")
    center_window(block_account_window, 300, 200)

    account_number_label = tk.Label(block_account_window, text="شماره حساب مورد نظر:")
    account_number_label.pack()
    account_number_entry = tk.Entry(block_account_window)
    account_number_entry.pack()

    reason_label = tk.Label(block_account_window, text="دلیل مسدود کردن حساب:")
    reason_label.pack()
    reason_entry = tk.Entry(block_account_window)
    reason_entry.pack()

    block_button = tk.Button(block_account_window,
                             text="تایید",
                             command=lambda: block_account(user_window, block_account_window,
                                                           account_number_entry.get(), reason_entry.get(), user_id))
    block_button.config(width=8)
    block_button.pack()

    back_button = tk.Button(block_account_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(user_window, block_account_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    block_account_window.protocol("WM_DELETE_WINDOW", on_closing)


def get_loans_page(parent_page, user_id):
    parent_page.withdraw()
    show_loans_window = tk.Toplevel(parent_page)
    show_loans_window.title("صفحه نمایش لیست وام ها")
    center_window(show_loans_window, 1450, 400)

    table = tk.ttk.Treeview(show_loans_window)

    table["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")

    table.heading("col1", text="شماره وام")
    table.heading("col2", text="مقدار وام")
    table.heading("col3", text="تاریخ گرفتن وام")
    table.heading("col4", text="تعداد اقساط")
    table.heading("col5", text="تعداد اقساط پرداخت شده")
    table.heading("col6", text="وضعیت وام")

    result = database_connector.get_loans(user_id)

    for x in range(len(result)):
        result[x] = list(result[x])
        if result[x][5] == 1:
            result[x][5] = "پرداخت نشده"
        else:
            result[x][5] = "پرداخت شده"

    for record in result:
        table.insert("", tk.END, values=record)

    print(table)
    table.pack()

    back_button = tk.Button(show_loans_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, show_loans_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    show_loans_window.protocol("WM_DELETE_WINDOW", on_closing)


def loan_score(parent_page, account_number, user_id):
    if not len(account_number):
        error_label = tk.Label(parent_page, text="شماره حساب وارد نشده است!")
        error_label.pack()
    elif not account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
        error_label.pack()
    else:
        check_account_number = database_connector.check_account_number(account_number)
        if not check_account_number:
            error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
            error_label.pack()
        amount = database_connector.loan_score_calculation(user_id, account_number)
        if amount is not None:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 150, 70)

            message_label = tk.Label(message_window, text=f"امتیاز وام شما:\n{amount}")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def loan_score_page(parent_window, user_id):
    parent_window.withdraw()
    loan_score_window = tk.Toplevel(parent_window)
    loan_score_window.title("صفحه امتیاز وام")
    center_window(loan_score_window, 300, 200)

    account_number_label = tk.Label(loan_score_window, text="شماره حساب مورد نظر:")
    account_number_label.pack()
    account_number_entry = tk.Entry(loan_score_window)
    account_number_entry.pack()

    loan_score_button = tk.Button(loan_score_window,
                                  text="تایید", command=lambda: loan_score(loan_score_window,
                                                                           account_number_entry.get(), user_id))
    loan_score_button.config(width=8)
    loan_score_button.pack()

    back_button = tk.Button(loan_score_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, loan_score_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    loan_score_window.protocol("WM_DELETE_WINDOW", on_closing)


def loan_application(loans_window, parent_page, type, account_number, amount, user_id):
    if not len(account_number) or not len(amount):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif not account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده معتبر نیست!")
        error_label.pack()
    elif not (amount.isnumeric()) or int(amount) <= 0:
        error_label = tk.Label(parent_page, text="مقدار درخواستی قابل قبول نیست!")
        error_label.pack()
    elif not database_connector.check_account_number(account_number):
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده معتبر نیست!")
        error_label.pack()
    elif not database_connector.check_loan_amount(user_id, account_number, amount):
        error_label = tk.Label(parent_page, text="مقدار درخواستی قابل قبول نیست!")
        error_label.pack()
    elif not database_connector.check_block_account(user_id, account_number):
        error_label = tk.Label(parent_page, text="شماره حساب مسدود است!")
        error_label.pack()
    elif database_connector.has_loan(user_id, account_number):
        error_label = tk.Label(parent_page, text="این حساب از قبل دارای وام فعال میباشد!")
        error_label.pack()
    else:
        done = database_connector.loan_application(user_id, account_number, amount, type)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 170, 50)

            message_label = tk.Label(message_window, text="وام شما با موفقیت پرداخت شد!")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            go_back(loans_window, parent_page)
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def loan_application_page(parent_window, user_id):
    parent_window.withdraw()
    loan_application_window = tk.Toplevel(parent_window)
    loan_application_window.title("صفحه درخواست وام")
    center_window(loan_application_window, 400, 300)

    account_number_label = tk.Label(loan_application_window, text="شماره حساب مورد نظر:")
    account_number_label.pack()
    account_number_entry = tk.Entry(loan_application_window)
    account_number_entry.pack()

    loan_score_button = tk.Button(loan_application_window,
                                  text="محاسبه امتیاز وام", command=lambda: loan_score(loan_application_window,
                                                                                       account_number_entry.get(),
                                                                                       user_id))
    loan_score_button.config(width=15)
    loan_score_button.pack()

    amount_label = tk.Label(loan_application_window, text="مبلغ درخواستی وام:")
    amount_label.pack()
    amount_entry = tk.Entry(loan_application_window)
    amount_entry.pack()

    loan1_button = tk.Button(loan_application_window,
                             text="وام 6 ماهه(15 درصد سود)",
                             command=lambda: loan_application(parent_window, loan_application_window, 1,
                                                              account_number_entry.get(), amount_entry.get(), user_id))
    loan1_button.config(width=20)
    loan1_button.pack()

    loan2_button = tk.Button(loan_application_window,
                             text="وام 12 ماهه(20 درصد سود)",
                             command=lambda: loan_application(parent_window, loan_application_window, 2,
                                                              account_number_entry.get(), amount_entry.get(), user_id))
    loan2_button.config(width=20)
    loan2_button.pack()

    loan3_button = tk.Button(loan_application_window,
                             text="وام 18 ماهه(25 درصد سود)",
                             command=lambda: loan_application(parent_window, loan_application_window, 3,
                                                              account_number_entry.get(), amount_entry.get(), user_id))
    loan3_button.config(width=20)
    loan3_button.pack()

    back_button = tk.Button(loan_application_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, loan_application_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    loan_application_window.protocol("WM_DELETE_WINDOW", on_closing)


def result_installments_page(parent_page, result, result2, result3):
    parent_page.withdraw()
    show_installments_window = tk.Toplevel(parent_page)
    show_installments_window.title("صفحه نمایش اقساط")
    center_window(show_installments_window, 1050, 400)

    table = tk.ttk.Treeview(show_installments_window)

    table["columns"] = ("col1", "col2", "col3", "col4")

    table.heading("col1", text="شماره قسط")
    table.heading("col2", text="وضعیت پرداخت")
    table.heading("col3", text="مقدار وجه قسط")
    table.heading("col4", text="تاریخ پرداخت")

    for x in range(len(result)):
        result[x] = list(result[x])
        if result[x][1] == 1:
            result[x][1] = "پرداخت شده"
        else:
            result[x][1] = "پرداخت نشده"

    for record in result:
        table.insert("", tk.END, values=record)

    print(table)
    table.pack()

    button_frame1 = tk.Frame(show_installments_window)
    button_frame1.pack()

    if result2 is None:
        result2 = 0

    paid_label = tk.Label(button_frame1, text=f"مجموع رقم پرداختی:\n{result2}")
    paid_label.pack(side=tk.RIGHT)

    if result3 is None:
        result3 = 0

    not_paid_label = tk.Label(button_frame1, text=f"مقدار پرداختی باقی مانده:\n{result3}")
    not_paid_label.pack(side=tk.LEFT)

    back_button = tk.Button(show_installments_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, show_installments_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    show_installments_window.protocol("WM_DELETE_WINDOW", on_closing)


def installment(parent_page, loan_number, user_id):
    if not len(loan_number):
        error_label = tk.Label(parent_page, text="شماره وام وارد نشده است!")
        error_label.pack()
    elif not loan_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره وام وارد شده نامعتبر است!")
        error_label.pack()
    else:
        check_loan_number = database_connector.check_loan_number(user_id, loan_number)
        if not check_loan_number:
            error_label = tk.Label(parent_page, text="شماره وام وارد شده نامعتبر است!")
            error_label.pack()

        result = database_connector.list_of_installment(user_id, loan_number)
        result2 = database_connector.sum_of_paid(user_id, loan_number)
        result3 = database_connector.not_paid(user_id, loan_number)

        for i, x in enumerate(result):
            result[i] = list(result[i])
            result[i].insert(0, i + 1)
            result[i] = tuple(result[i])

        result_installments_page(parent_page, result, result2, result3)


def list_of_installment_page(parent_window, user_id):
    parent_window.withdraw()
    installment_window = tk.Toplevel(parent_window)
    installment_window.title("صفحه اقساط وام")
    center_window(installment_window, 300, 200)

    loan_number_label = tk.Label(installment_window, text="شماره وام مورد نظر:")
    loan_number_label.pack()
    loan_number_entry = tk.Entry(installment_window)
    loan_number_entry.pack()

    installment_button = tk.Button(installment_window,
                                   text="تایید", command=lambda: installment(installment_window,
                                                                             loan_number_entry.get(), user_id))
    installment_button.config(width=8)
    installment_button.pack()

    back_button = tk.Button(installment_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, installment_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    installment_window.protocol("WM_DELETE_WINDOW", on_closing)


def pay_installment(loans_window, parent_page, loan_number, user_id):
    if not len(loan_number):
        error_label = tk.Label(parent_page, text="شماره وام را وارد کنید!")
        error_label.pack()
    elif not loan_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره وام وارد شده نامعتبر است!")
        error_label.pack()
    else:
        check_loan_number = database_connector.check_loan_number(user_id, loan_number)
        state_loan = database_connector.state_loan(user_id, loan_number)
        check_installments = database_connector.list_of_installment(user_id, loan_number)
        for x in check_installments:
            if date.today() == x[2]:
                check_installments = False
                break
        if not check_loan_number:
            error_label = tk.Label(parent_page, text="شماره وام وارد شده نامعتبر است!")
            error_label.pack()
        elif not state_loan:
            error_label = tk.Label(parent_page, text="قسط های این وام پرداخت شده است!")
            error_label.pack()
        elif check_installments is False:
            error_label = tk.Label(parent_page, text="قسط امروز را پرداخت کرده اید!")
            error_label.pack()
        else:
            done = database_connector.pay_installment(user_id, loan_number)
            if done:
                def close_window():
                    message_window.destroy()

                message_window = tk.Tk()
                center_window(message_window, 200, 50)

                message_label = tk.Label(message_window, text="پرداخت قسط با موفقیت انجام شد!")
                message_label.pack()

                button_ok = tk.Button(message_window, text="تایید", command=close_window)
                button_ok.pack()

                go_back(loans_window, parent_page)
            else:
                def close_window():
                    warning_window.destroy()

                warning_window = tk.Tk()
                center_window(warning_window, 150, 70)

                warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
                warning_label.pack()

                button_ok = tk.Button(warning_window, text="تایید", command=close_window)
                button_ok.pack()


def pay_installment_page(parent_window, user_id):
    parent_window.withdraw()
    pay_installment_window = tk.Toplevel(parent_window)
    pay_installment_window.title("صفحه پرداخت قسط")
    center_window(pay_installment_window, 300, 200)

    loan_number_label = tk.Label(pay_installment_window, text="شماره وام مورد نظر:")
    loan_number_label.pack()
    loan_number_entry = tk.Entry(pay_installment_window)
    loan_number_entry.pack()

    pay_installment_button = tk.Button(pay_installment_window,
                                       text="پرداخت قسط", command=lambda: pay_installment(parent_window,
                                                                                          pay_installment_window,
                                                                                          loan_number_entry.get(),
                                                                                          user_id))
    pay_installment_button.config(width=10)
    pay_installment_button.pack()

    back_button = tk.Button(pay_installment_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, pay_installment_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    pay_installment_window.protocol("WM_DELETE_WINDOW", on_closing)


def loans_page(parent_page, user_id):
    parent_page.withdraw()
    loans_window = tk.Toplevel(parent_page)
    loans_window.title("صفحه وام ها")
    center_window(loans_window, 400, 300)

    get_loans_button = tk.Button(loans_window, text="دریافت لیست وام ها",
                                 command=lambda: get_loans_page(loans_window, user_id))
    get_loans_button.config(width=15)
    get_loans_button.pack()

    loan_score_button = tk.Button(loans_window, text="محاسبه امتیاز وام",
                                  command=lambda: loan_score_page(loans_window, user_id))
    loan_score_button.config(width=15)
    loan_score_button.pack()

    loan_application_transactions_button = tk.Button(loans_window, text="درخواست وام",
                                                     command=lambda: loan_application_page(loans_window, user_id))
    loan_application_transactions_button.config(width=15)
    loan_application_transactions_button.pack()

    list_of_installment_button = tk.Button(loans_window, text="نمایش اقساط وام",
                                           command=lambda: list_of_installment_page(loans_window, user_id))
    list_of_installment_button.config(width=15)
    list_of_installment_button.pack()

    pay_installment_button = tk.Button(loans_window, text="پرداخت قسط وام",
                                       command=lambda: pay_installment_page(loans_window, user_id))
    pay_installment_button.config(width=15)
    pay_installment_button.pack()

    back_button = tk.Button(loans_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, loans_window))
    back_button.config(width=8)
    back_button.pack(pady=20)

    loans_window.protocol("WM_DELETE_WINDOW", on_closing)


def change_password(user_window, parent_page, last_password, new_password, r_new_password, user_id):
    hash_object = hashlib.sha256()
    password_bytes = last_password.encode('utf-8')
    hash_object.update(password_bytes)
    hashed_password = hash_object.hexdigest()

    hash_object2 = hashlib.sha256()
    password_bytes2 = new_password.encode('utf-8')
    hash_object2.update(password_bytes2)
    hashed_password2 = hash_object2.hexdigest()

    if not len(last_password) or not len(new_password) or not len(r_new_password):
        error_label = tk.Label(parent_page, text="اطلاعات لازم وارد نشده است!")
        error_label.pack()
    elif len(new_password) < 8:
        error_label = tk.Label(parent_page, text="طول رمزعبور باید حداقل 8 کارکتر باشد!")
        error_label.pack()
    elif new_password != r_new_password:
        error_label = tk.Label(parent_page, text="رمز عبور ها یکسان نیست!")
        error_label.pack()
    elif not database_connector.check_password(user_id, hashed_password):
        error_label = tk.Label(parent_page, text="رمز عبور قبلی صحیح نیست!")
        error_label.pack()
    else:
        done = database_connector.change_password(user_id, hashed_password, hashed_password2)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 200, 50)

            message_label = tk.Label(message_window, text="تغییر رمز عبور با موفقیت انجام شد!")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            go_back(user_window, parent_page)
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def change_password_page(user_window, user_id):
    user_window.withdraw()
    change_password_window = tk.Toplevel(user_window)
    change_password_window.title("صفحه تغییر رمز عبور")
    center_window(change_password_window, 300, 200)

    last_password_label = tk.Label(change_password_window, text="رمز عبود قبلی:")
    last_password_label.pack()
    last_password_entry = tk.Entry(change_password_window)
    last_password_entry.pack()

    new_password_label = tk.Label(change_password_window, text="رمز عبود جدید:")
    new_password_label.pack()
    new_password_entry = tk.Entry(change_password_window)
    new_password_entry.pack()

    r_new_password_label = tk.Label(change_password_window, text="تکرار رمز عبود جدید:")
    r_new_password_label.pack()
    r_new_password_entry = tk.Entry(change_password_window)
    r_new_password_entry.pack()

    transaction_button = tk.Button(change_password_window,
                                   text="تایید",
                                   command=lambda: change_password(user_window, change_password_window,
                                                                   last_password_entry.get(),
                                                                   new_password_entry.get(),
                                                                   r_new_password_entry.get(), user_id))
    transaction_button.config(width=8)
    transaction_button.pack()

    back_button = tk.Button(change_password_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(user_window, change_password_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    change_password_window.protocol("WM_DELETE_WINDOW", on_closing)


def user_page(parent_page, user_id):
    parent_page.withdraw()
    user_window = tk.Toplevel(parent_page)
    user_window.title("صفحه کاربر")

    check_admin = database_connector.check_admin(user_id)

    if check_admin:
        center_window(user_window, 400, 340)
    else:
        center_window(user_window, 400, 300)

    first_name = database_connector.get_first_name(user_id)
    user_label = tk.Label(user_window, text=f"{first_name} خوش آمدید!")
    user_label.pack()

    get_accounts_button = tk.Button(user_window, text="دریافت لیست تمام حساب ها",
                                    command=lambda: get_accounts_page(user_window, user_id))
    get_accounts_button.config(width=24)
    get_accounts_button.pack()

    transaction_button = tk.Button(user_window, text="انتقال وجه",
                                   command=lambda: transaction_page(user_window, user_id))
    transaction_button.config(width=24)
    transaction_button.pack()

    get_recent_transactions_button = tk.Button(user_window, text="گردش حساب اخیر",
                                               command=lambda: get_recent_transactions_page(user_window, user_id))
    get_recent_transactions_button.config(width=24)
    get_recent_transactions_button.pack()

    get_period_transactions_button = tk.Button(user_window, text="نمایش گردش حساب بین دو تاریخ",
                                               command=lambda: get_period_transactions_page(user_window, user_id))
    get_period_transactions_button.config(width=24)
    get_period_transactions_button.pack()

    block_account_button = tk.Button(user_window, text="مسدود کردن حساب",
                                     command=lambda: block_account_page(user_window, user_id))
    block_account_button.config(width=24)
    block_account_button.pack()

    loans_button = tk.Button(user_window, text="وام ها", command=lambda: loans_page(user_window, user_id))
    loans_button.config(width=24)
    loans_button.pack()

    change_password_button = tk.Button(user_window, text="تغییر رمز عبور",
                                       command=lambda: change_password_page(user_window, user_id))
    change_password_button.config(width=24)
    change_password_button.pack()

    def change_panel():
        user_window.withdraw()
        admin_page(parent_page, user_id)

    if check_admin:
        change_panel_button = tk.Button(user_window, text="تغییر پنل", fg="white", bg="green", command=change_panel)
        change_panel_button.config(width=8)
        change_panel_button.pack(pady=20)

    back_button = tk.Button(user_window, text="بازگشت", bg="orange", command=lambda: go_back(parent_page, user_window))
    back_button.config(width=8)
    back_button.pack(pady=20)

    user_window.protocol("WM_DELETE_WINDOW", on_closing)


def add_account(admin_window, parent_page, username, user_id):
    user_id2 = database_connector.get_id(user_id, username)
    if not len(username):
        error_label = tk.Label(parent_page, text="نام کاربری وارد نشده است!")
        error_label.pack()
    elif user_id2 is None:
        error_label = tk.Label(parent_page, text="نام کاربری وارد شده نامعتبر است!")
        error_label.pack()
    else:
        done = database_connector.add_account(user_id, user_id2)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 200, 50)

            message_label = tk.Label(message_window, text="افزودن حساب با موفقیت انجام شد!")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            go_back(admin_window, parent_page)
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def add_account_page(admin_window, user_id):
    admin_window.withdraw()
    add_account_window = tk.Toplevel(admin_window)
    add_account_window.title("صفحه افزودن حساب")
    center_window(add_account_window, 300, 200)

    username_label = tk.Label(add_account_window, text="نام کاربری یوزر مورد نظر:")
    username_label.pack()
    username_entry = tk.Entry(add_account_window)
    username_entry.pack()

    add_account_button = tk.Button(add_account_window,
                                   text="تایید",
                                   command=lambda: add_account(admin_window, add_account_window,
                                                               username_entry.get(), user_id))
    add_account_button.config(width=8)
    add_account_button.pack()

    back_button = tk.Button(add_account_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(admin_window, add_account_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    add_account_window.protocol("WM_DELETE_WINDOW", on_closing)


def add_admin(admin_window, parent_page, username, user_id):
    user_id2 = database_connector.get_id(user_id, username)
    if user_id2 is None:
        user_id2 = 0
    check_admin = database_connector.check_admin(user_id2)
    if not len(username):
        error_label = tk.Label(parent_page, text="نام کاربری را وارد کنید!")
        error_label.pack()
    elif user_id2 == 0:
        error_label = tk.Label(parent_page, text="نام کاربری وارد شده نامعتبر است!")
        error_label.pack()
    elif check_admin:
        error_label = tk.Label(parent_page, text="این کاربر ادمین است!")
        error_label.pack()
    else:
        done = database_connector.add_admin(user_id, user_id2)
        if done:
            def close_window():
                message_window.destroy()

            message_window = tk.Tk()
            center_window(message_window, 200, 50)

            message_label = tk.Label(message_window, text="افزودن ادمین با موفقیت انجام شد!")
            message_label.pack()

            button_ok = tk.Button(message_window, text="تایید", command=close_window)
            button_ok.pack()

            go_back(admin_window, parent_page)
        else:
            def close_window():
                warning_window.destroy()

            warning_window = tk.Tk()
            center_window(warning_window, 150, 70)

            warning_label = tk.Label(warning_window, text="مشکلی در عملیات پیش آمد!\n دوباره امتحان کنید.")
            warning_label.pack()

            button_ok = tk.Button(warning_window, text="تایید", command=close_window)
            button_ok.pack()


def add_admin_page(admin_window, user_id):
    admin_window.withdraw()
    add_admin_window = tk.Toplevel(admin_window)
    add_admin_window.title("صفحه افزودن ادمین")
    center_window(add_admin_window, 300, 200)

    username_label = tk.Label(add_admin_window, text="نام کاربری یوزر مورد نظر:")
    username_label.pack()
    username_entry = tk.Entry(add_admin_window)
    username_entry.pack()

    add_admin_button = tk.Button(add_admin_window,
                                 text="تایید",
                                 command=lambda: add_admin(admin_window, add_admin_window, username_entry.get(),
                                                           user_id))
    add_admin_button.config(width=8)
    add_admin_button.pack()

    back_button = tk.Button(add_admin_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(admin_window, add_admin_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    add_admin_window.protocol("WM_DELETE_WINDOW", on_closing)


def get_users_info_page(parent_page, user_id):
    parent_page.withdraw()
    get_users_info_window = tk.Toplevel(parent_page)
    get_users_info_window.title("صفحه نمایش اطلاعات کاربران")
    center_window(get_users_info_window, 1250, 400)

    table = tk.ttk.Treeview(get_users_info_window)

    table["columns"] = ("col1", "col2", "col3", "col4", "col5")

    table.heading("col1", text="نام کاربری")
    table.heading("col2", text="نام")
    table.heading("col3", text="نام خانوادگی")
    table.heading("col4", text="ایمیل")
    table.heading("col5", text="شماره همراه")

    data = database_connector.get_users_info(user_id)
    for record in data:
        table.insert("", tk.END, values=record)

    print(table)
    table.pack()

    back_button = tk.Button(get_users_info_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, get_users_info_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    get_users_info_window.protocol("WM_DELETE_WINDOW", on_closing)


def get_user_accounts(parent_page, username, user_id):
    user_id2 = database_connector.get_id(user_id, username)
    if not len(username):
        error_label = tk.Label(parent_page, text="نام کاربری را وارد کنید!")
        error_label.pack()
    elif user_id2 is None:
        error_label = tk.Label(parent_page, text="نام کاربری وارد شده نامعتبر است!")
        error_label.pack()
    else:
        get_accounts_page(parent_page, user_id2)


def get_user_accounts_page(parent_window, user_id):
    parent_window.withdraw()
    get_user_accounts_window = tk.Toplevel(parent_window)
    get_user_accounts_window.title("صفحه حساب های هر کاربر")
    center_window(get_user_accounts_window, 300, 200)

    user_name_label = tk.Label(get_user_accounts_window, text="نام کاربری کاربر مورد نظر:")
    user_name_label.pack()
    user_name_entry = tk.Entry(get_user_accounts_window)
    user_name_entry.pack()

    get_user_accounts_button = tk.Button(get_user_accounts_window,
                                         text="تایید", command=lambda: get_user_accounts(get_user_accounts_window,
                                                                                         user_name_entry.get(),
                                                                                         user_id))
    get_user_accounts_button.config(width=8)
    get_user_accounts_button.pack()

    back_button = tk.Button(get_user_accounts_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, get_user_accounts_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    get_user_accounts_window.protocol("WM_DELETE_WINDOW", on_closing)


def show_account_info(result):
    def close_window():
        message_window.destroy()

    message_window = tk.Tk()
    center_window(message_window, 150, 450)

    message_label = tk.Label(message_window, text="شماره حساب:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][0]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="نام صاحب حساب:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][1]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="نام خانوادگی صاحب حساب:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][2]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="ایمیل صاحب حساب:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][3]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="شماره همراه صاحب حساب:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][4]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="تاریخ افتتاح:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][5]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="موجودی:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{result[0][6]}")
    message_label.pack()

    message_label = tk.Label(message_window, text="شماره وام فعال:")
    message_label.pack()
    active_loan_state = result[0][7]
    if result[0][7] is None:
        active_loan_state = "وام فعالی وجود ندارد"
    message_label = tk.Label(message_window, text=f"{active_loan_state}")
    message_label.pack()

    block_date = result[0][8]
    block_reason = result[0][9]
    if result[0][8] is None:
        block_date = "--"
        block_reason = "--"

    message_label = tk.Label(message_window, text="تاریخ مسدودیت:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{block_date}")
    message_label.pack()

    message_label = tk.Label(message_window, text="دلیل مسدودیت:")
    message_label.pack()
    message_label = tk.Label(message_window, text=f"{block_reason}")
    message_label.pack()

    button_ok = tk.Button(message_window, text="تایید", command=close_window)
    button_ok.pack()


def get_account_info(parent_page, account_number, user_id):
    if not len(account_number):
        error_label = tk.Label(parent_page, text="شماره حساب وارد نشده است!")
        error_label.pack()
    elif not account_number.isnumeric():
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
        error_label.pack()
    elif not database_connector.check_account_number(account_number):
        error_label = tk.Label(parent_page, text="شماره حساب وارد شده نامعتبر است!")
        error_label.pack()
    else:
        result = database_connector.get_account_information(user_id, account_number)

        show_account_info(result)


def get_account_info_page(parent_window, user_id):
    parent_window.withdraw()
    get_account_info_window = tk.Toplevel(parent_window)
    get_account_info_window.title("صفحه مشخصات حساب")
    center_window(get_account_info_window, 300, 200)

    account_number_label = tk.Label(get_account_info_window, text="شماره حساب مورد نظر:")
    account_number_label.pack()
    account_number_entry = tk.Entry(get_account_info_window)
    account_number_entry.pack()

    get_account_info_button = tk.Button(get_account_info_window,
                                        text="تایید", command=lambda: get_account_info(get_account_info_window,
                                                                                       account_number_entry.get(),
                                                                                       user_id))
    get_account_info_button.config(width=8)
    get_account_info_button.pack()

    back_button = tk.Button(get_account_info_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, get_account_info_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    get_account_info_window.protocol("WM_DELETE_WINDOW", on_closing)


def get_user_loans(parent_page, username, user_id):
    user_id2 = database_connector.get_id(user_id, username)
    if not len(username):
        error_label = tk.Label(parent_page, text="نام کاربری را وارد کنید!")
        error_label.pack()
    elif user_id2 is None:
        error_label = tk.Label(parent_page, text="نام کاربری وارد شده نامعتبر است!")
        error_label.pack()
    else:
        get_loans_page(parent_page, user_id2)


def get_user_loans_page(parent_window, user_id):
    parent_window.withdraw()
    get_user_loans_window = tk.Toplevel(parent_window)
    get_user_loans_window.title("صفحه وام های هر کاربر")
    center_window(get_user_loans_window, 300, 200)

    user_name_label = tk.Label(get_user_loans_window, text="نام کاربری کاربر مورد نظر:")
    user_name_label.pack()
    user_name_entry = tk.Entry(get_user_loans_window)
    user_name_entry.pack()

    get_user_loans_button = tk.Button(get_user_loans_window,
                                      text="تایید", command=lambda: get_user_loans(get_user_loans_window,
                                                                                   user_name_entry.get(),
                                                                                   user_id))
    get_user_loans_button.config(width=8)
    get_user_loans_button.pack()

    back_button = tk.Button(get_user_loans_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_window, get_user_loans_window))
    back_button.config(width=8)
    back_button.pack(pady=10)

    get_user_loans_window.protocol("WM_DELETE_WINDOW", on_closing)


def admin_page(parent_page, user_id):
    parent_page.withdraw()
    admin_window = tk.Toplevel(parent_page)
    admin_window.title("صفحه ادمین")
    center_window(admin_window, 400, 330)

    first_name = database_connector.get_first_name(user_id)
    admin_label = tk.Label(admin_window, text=f"{first_name} خوش آمدید!")
    admin_label.pack()

    add_account_button = tk.Button(admin_window, text="افزودن حساب",
                                   command=lambda: add_account_page(admin_window, user_id))
    add_account_button.config(width=20)
    add_account_button.pack()

    add_admin_button = tk.Button(admin_window, text="افزودن ادمین",
                                 command=lambda: add_admin_page(admin_window, user_id))
    add_admin_button.config(width=20)
    add_admin_button.pack()

    get_user_info_button = tk.Button(admin_window, text="اطلاعات کاربران",
                                     command=lambda: get_users_info_page(admin_window, user_id))
    get_user_info_button.config(width=20)
    get_user_info_button.pack()

    get_user_accounts_button = tk.Button(admin_window, text="لیست حساب های هر کاربر",
                                         command=lambda: get_user_accounts_page(admin_window, user_id))
    get_user_accounts_button.config(width=20)
    get_user_accounts_button.pack()

    get_account_info_button = tk.Button(admin_window, text="اطلاعات حساب ها",
                                        command=lambda: get_account_info_page(admin_window, user_id))
    get_account_info_button.config(width=20)
    get_account_info_button.pack()

    get_user_loans_button = tk.Button(admin_window, text="لیست  وام های هر کاربر",
                                      command=lambda: get_user_loans_page(admin_window, user_id))
    get_user_loans_button.config(width=20)
    get_user_loans_button.pack()

    def change_panel():
        admin_window.withdraw()
        user_page(parent_page, user_id)

    change_panel_button = tk.Button(admin_window, text="تغییر پنل", fg="white", bg="green", command=change_panel)
    change_panel_button.config(width=8)
    change_panel_button.pack(pady=20)

    back_button = tk.Button(admin_window, text="بازگشت", bg="orange",
                            command=lambda: go_back(parent_page, admin_window))
    back_button.config(width=8)
    back_button.pack(pady=20)

    admin_window.protocol("WM_DELETE_WINDOW", on_closing)


def root_page():
    def close_window():
        root.destroy()

    global root
    root = tk.Tk()
    root.title("همراه بانک")

    body_width = 300
    body_height = 200
    center_window(root, body_width, body_height)

    background_image = tk.PhotoImage(file="IMAGES/geen_background.gif")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label = tk.Label(root, text="همراه بانک")
    label.pack()

    register_button = tk.Button(root, text="ثبت نام", fg="white", bg="green",
                                command=lambda: register_page(root))
    register_button.config(width=8)
    register_button.pack(pady=10)

    login_button = tk.Button(root, text="ورود", fg="white", bg="green", command=lambda: login_page(root))
    login_button.config(width=8)
    login_button.pack(pady=10)

    exit_button = tk.Button(root, text="خروج", fg="white", bg="red", command=close_window)
    exit_button.config(width=8)
    exit_button.pack(side=tk.BOTTOM, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
