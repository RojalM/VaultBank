# Example Usage
import locale
from LearnProject.User import User
from LearnProject.LoginSystem import *
import getpass
from datetime import datetime

class Main:
    def __init__(self):
        self.auth_system = LoginSystem()
        self.run_program()

    def run_program(self):
        while True:
            if not self.auth_system.is_authenticated():
                self.login_menu()
            else:
                self.menu_system()

    def login_menu(self):
        print("\n" + "="*20)
        print("Login System")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("="*20)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        try:
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register()
            elif choice == "3":
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_login(self):
        print("\nLogin")
        username = input("Username: ").strip()
        password = getpass.getpass(prompt = 'Enter the password: ')
        
        try:
            user = self.auth_system.login(username, password)
            print(user.welcome_message())
        except ValueError as e:
            print(f"Login failed: {e}")

    def handle_register(self):
        print("\nRegistration")
        username = input("Choose a username: ").strip()
        password = getpass.getpass(prompt = 'Enter the password: ')
        confirm_password = getpass.getpass(prompt = 'Enter the password: ')
        
        if password != confirm_password:
            print("Error: Passwords don't match")
            return
        
        try:
            user = self.auth_system.register(username, password)
            print(user.welcome_message())
        except ValueError as e:
            print(f"Registration failed: {e}")

    def menu_system(self):
        user = self.auth_system.current_user
        account = user.account

        while True:
            print("\n" + "="*20)
            print(f"Main Menu - Welcome {user.name}")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. View Balance")
            print("4. Transaction History")
            print("5. Logout")
            print("="*20)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            try:
                if choice == "1":
                    amount = float(input("Enter deposit amount: "))
                    account.deposit(amount)
                elif choice == "2":
                    amount = float(input("Enter withdrawal amount: "))
                    account.withdraw(amount)
                elif choice == "3":
                    print(f"Current balance: {account.view_balance()}")
                elif choice == "4":
                    if not account.transactions:
                        print("\nNo transactions yet!")
                        continue

                    headers = ["Date", "Amount", "Balance"]
                    print(f"\n{headers[0]:<10} | {headers[1]:<10} | {headers[2]}")
                    print("-"*35)

                    for idx, txn in enumerate(account.transactions, 1):
                        # Fixed date parsing
                        date_str = txn["timestamp"]
                        date_obj = datetime.strptime(date_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
                        date = date_obj.strftime("%m/%d/%Y")
                        
                        amount = locale.currency(txn["amount"], grouping=True)
                        balance = locale.currency(txn["balance_after"], grouping=True)
                        
                        print(f"{idx}. {date:<10} | {amount:<10} | {balance}")
                elif choice == "5":
                    self.auth_system.logout()
                    return
                else:
                    print("Invalid choice. Please enter 1-5.")
                    
            except ValueError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    Main()