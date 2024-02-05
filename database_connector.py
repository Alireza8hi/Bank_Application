import mysql.connector

global cursor
global mydb


def connect_to_mysql(my_localhost, my_username, my_password, my_database_name):
    global mydb
    mydb = mysql.connector.connect(
        host=my_localhost,
        user=my_username,
        password=my_password,
        database=my_database_name
    )
    global cursor
    cursor = mydb.cursor()
    return mydb



def call_procedure(procedure_name, *args):

    cursor.callproc(procedure_name, args=args)
    result_list = []
    result = cursor.stored_results()
    for res in result:
        result_list.append(res.fetchall())
    mydb.commit()
    return result_list[0]


def call_function(function_name, *args):
    arguments = ''
    for arg in args:
        arguments += "'" + str(arg) + "',"
    arguments = arguments[:-1]
    cursor.execute("SELECT " + function_name + "(" + arguments + ");")
    output = cursor.fetchone()[0]
    mydb.commit()
    return output


def disconnect_to_mysql():
    cursor.close()
    mydb.close()


# ----------------------------------------------------------- Procedures
# login and register actions
# user actions
def get_accounts(user_id):
    return call_procedure("all_accounts", user_id)


def get_account_information(user_id, account_number):
    return call_procedure("account_info", user_id, account_number)


def money_transfer(user_id, source_account_number, destination_account_number, amount):
    return call_procedure("money_transfer", user_id, source_account_number, destination_account_number, amount)


def get_recent_transactions(user_id, account_number, number):
    return call_procedure("get_recent_transaction", user_id, account_number, number)


def get_period_transactions(user_id, account_number, start_date, end_date):
    return call_procedure("get_period_transaction", user_id, account_number, start_date, end_date)


def get_loans(user_id):
    return call_procedure("get_loans", user_id)


def list_of_installment(user_id, loan_number):
    return call_procedure("list_of_installment", user_id, loan_number)


# admin actions
def get_users_info(user_id):
    return call_procedure("get_users_info", user_id)
# ----------------------------------------------------------- Functions
# login and  register actions


def login(username, password):
    return call_function("login", username, password)


def check_admin(user_id):
    return call_function("is_admin", user_id)


def register(username, first_name, last_name, email, number, password):
    return call_function("signup",  first_name, last_name, password, username, email, number)


def check_username(username):
    return call_function("check_username", username)


def check_phone_number(number):
    return call_function("check_phone_number", number)


def check_email(email):
    return call_function("check_email", email)


# user actions
def get_first_name(user_id):
    return call_function("get_first_name", user_id)


def get_full_name(account_number):
    return call_function("get_full_name", account_number)


def check_amount(amount, user_id, account_number):
    return call_function("check_amount", amount, user_id, account_number)


def check_account_number(account_number):
    return call_function("check_account_number", account_number)


def check_block_account(user_id, account_number):
    return call_function("check_block_account", user_id, account_number)


def block_account(user_id, account_number, reason):
    return call_function("block_account", user_id, account_number, reason)


def has_loan(user_id, account_number):
    return call_function("has_loan", user_id, account_number)


def loan_score_calculation(user_id, account_number):
    return call_function("loan_score_calculation", user_id, account_number)


def loan_application(user_id, account_number, amount, type):
    return call_function("loan_application", user_id, account_number, amount, type)


def check_loan_amount(user_id, account_number, amount):
    return call_function("check_loan_amount", user_id, account_number, amount)


def check_loan_number(user_id, loan_number):
    return call_function("check_loan_number", user_id, loan_number)


def sum_of_paid(user_id, loan_number):
    return call_function("sum_of_paid", user_id, loan_number)


def not_paid(user_id, loan_number):
    return call_function("not_paid", user_id, loan_number)


def state_loan(user_id, loan_number):
    return call_function("state_loan", user_id, loan_number)


def get_id(user_id, username):
    return call_function("get_id", user_id, username)


def get_email(user_id):
    return call_function("get_email", user_id)


def pay_installment(user_id, loan_number):
    return call_function("pay_installment", user_id, loan_number)


def check_password(user_id, password):
    return call_function("check_password", user_id, password)


def change_password(user_id, last_password, new_password):
    return call_function("change_password", user_id, last_password, new_password)
# admin actions


def add_account(user_id, user_id_for_account):
    return call_function("add_account", user_id, user_id_for_account)


def add_admin(user_id, user_id_for_admin):
    return call_function("add_admin", user_id, user_id_for_admin)


