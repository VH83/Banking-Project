import os
import hashlib
import json
import random
from datetime import datetime, timedelta

userfile = 'users.txt'

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load all users
def load_users():
    if os.path.exists(userfile):
        with open(userfile, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save all users
def save_users(users):
    with open(userfile, 'w') as f:
        json.dump(users, f, indent=4)

# Check if email already exists
def user_exists(email):
    users = load_users()
    return any(user['email'].lower() == email.lower() for user in users)

# Register new user
def register():
    while True:
        firstname = input("Enter your first name in (UPPERCASE): ")
        if firstname.isalpha() and firstname.isupper():
            break
        print("Invalid first name. Only uppercase letters.")

    while True:
        lastname = input("Enter your last name (UPPERCASE): ")
        if lastname.isalpha() and lastname.isupper():
            break
        print("Invalid last name.")

    while True:
        phone = input("Enter your phone number (10 digits): ")
        if phone.isdigit() and len(phone) == 10:
            break
        print("Invalid phone number.")

    while True:
        email = input("Enter your email (must end with @gmail.com): ")
        if email.endswith("@gmail.com") and email.islower():
            if user_exists(email):
                print("Email already exists.")
            else:
                break
        else:
            print("Invalid email.")

    while True:
        password = input("Enter password (min 8 characters): ")
        if len(password) >= 8:
            break
        print("Password too short.")

    hashed_pw = hash_password(password)
    account_number = random.randint(10**11, 10**12 - 1)

    new_user = {
        'first_name': firstname,
        'last_name': lastname,
        'account_number': account_number,
        'phone': phone,
        'email': email,
        'password': hashed_pw,
        'balance': 0,
        'transactions': []
    }

    users = load_users()
    users.append(new_user)
    save_users(users)

    print(f"Registration successful! Your account number is {account_number}")

# Login function (returns user dict)
def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_pw = hash_password(password)

    users = load_users()
    for user in users:
        if user['email'].lower() == email.lower() and user['password'] == hashed_pw:
            print(f"Login successful! Welcome, {user['first_name']} {user['last_name']}")
            return user['account_number']
    print("Login failed.")
    return None

# Update user data by account number
def update_user_data(account_number, updated_user):
    users = load_users()
    for i, user in enumerate(users):
        if user['account_number'] == account_number:
            users[i] = updated_user
            break
    save_users(users)

# Deposit money
def deposit(account_number):
    users = load_users()
    for user in users:
        if user['account_number'] == account_number:
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("Amount must be positive.")
                    return
                user['balance'] += amount
                user['transactions'].append({
                    'type': 'deposit',
                    'amount': amount,
                    'date': datetime.now().isoformat()
                })
                update_user_data(account_number, user)
                print(f"Deposited ₹{amount}. New balance: ₹{user['balance']}")
                return
            except ValueError:
                print("Invalid amount.")
                return

# Withdraw money
def withdraw(account_number):
    users = load_users()
    for user in users:
        if user['account_number'] == account_number:
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("Amount must be positive.")
                    return
                if amount > user['balance']:
                    print("Insufficient balance.")
                    return
                user['balance'] -= amount
                user['transactions'].append({
                    'type': 'withdraw',
                    'amount': amount,
                    'date': datetime.now().isoformat()
                })
                update_user_data(account_number, user)
                print(f"Withdrew ₹{amount}. New balance: ₹{user['balance']}")
                return
            except ValueError:
                print("Invalid amount.")
                return

# Show balance
def show_balance(account_number):
    users = load_users()
    for user in users:
        if user['account_number'] == account_number:
            print(f"Your current balance is: ₹{user['balance']}")
            return

# View transactions from last N days
def show_transactions(account_number, days):
    users = load_users()
    for user in users:
        if user['account_number'] == account_number:
            cutoff = datetime.now() - timedelta(days=days)
            print(f"\nTransactions for the last {days} days:")
            has_transactions = False
            for txn in user['transactions']:
                txn_date = datetime.fromisoformat(txn['date'])
                if txn_date >= cutoff:
                    print(f"{txn_date.strftime('%Y-%m-%d %H:%M:%S')} - {txn['type']} - ₹{txn['amount']}")
                    has_transactions = True
            if not has_transactions:
                print("No transactions found in this period.")
            return

# Menu for logged-in user
def user_menu(account_number):
    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Show Balance")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            deposit(account_number)
        elif choice == '2':
            withdraw(account_number)
        elif choice == '3':
            show_balance(account_number)
        elif choice == '4':
            print("a. Last 7 days\nb. Last 30 days\nc. Last 90 days")
            time_choice = input("Choose an option: ")
            if time_choice == 'a':
                show_transactions(account_number, 7)
            elif time_choice == 'b':
                show_transactions(account_number, 30)
            elif time_choice == 'c':
                show_transactions(account_number, 90)
            else:
                print("Invalid option.")
        elif choice == '5':
            print("Logged out.")
            break
        else:
            print("Invalid option.")

# Main menu
def main():
    while True:
        print("\n===== WELCOME TO THE BANKING SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            account = login()
            if account:
                user_menu(account)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

# Run the app
if __name__ == "__main__":
    main()