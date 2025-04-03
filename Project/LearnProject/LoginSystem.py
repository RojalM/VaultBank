import datetime
from LearnProject.User import * 
import bcrypt
import json  

class LoginSystem:
    def __init__(self):
        self.users = {}  # here we store for now User/ password
        self.current_user = None  # tracks logged in user
        self.load_users()  # Load users automatically on initialization

    def hash_password(self, password: str):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)
    
    def register(self, username: str, password: str):
        if username in self.users:
            raise ValueError("Username already exists")
        
        hashed_password = self.hash_password(password)
        
        self.users[username] = {
            "password": hashed_password,
            "user": User(username),
            "failed_attempts": 0,
            "locked": False
        }
        print(f"User {username} registered successfully!")
        self.current_user = self.users[username]["user"]  # Auto-login after registration
        self.save_users()
        return self.current_user

    def login(self, username: str, password: str):
        if username not in self.users:
            raise ValueError("User does not exist")
        
        user_data = self.users[username]
        
        if user_data["locked"]:
            raise ValueError("Account locked due to multiple failed attempts. Please contact support.")
                
        if bcrypt.checkpw(password.encode(), user_data["password"]):
            user_data["failed_attempts"] = 0
            print(f"Welcome back, {username}!")
            self.current_user = user_data["user"]
            self.save_users()
            return self.current_user
        else:
            user_data["failed_attempts"] += 1
            remaining_attempts = 5 - user_data["failed_attempts"]
            
            if user_data["failed_attempts"] >= 5:
                user_data["locked"] = True
                raise ValueError("Too many failed attempts. Account locked!")
            
            raise ValueError(f"Invalid password. {remaining_attempts} attempts remaining")
        
    def logout(self):
        if self.current_user:
            print(f"Goodbye, {self.current_user.name}!")
            self.current_user = None
        else:
            print("No user is currently logged in")

    def is_authenticated(self):
        return self.current_user is not None

    def save_users(self):
        """
        Securely save user data to JSON file
        """
        data = {}
        for username, user_data in self.users.items():
            # Convert account data to serializable format
            account = user_data["user"].account
            transactions = [
            {
                "type": t["type"],
                "amount": t["amount"],
                "balance_after": t["balance_after"],
                "timestamp": t["timestamp"].isoformat()  # Already correct
            }
            for t in account.transactions
            ]
            
            data[username] = {
                "name": user_data["user"].name,
                "password": user_data["password"].decode('utf-8'),  # bcrypt hash to string
                "locked": user_data["locked"],
                "failed_attempts": user_data["failed_attempts"],
                "account": {
                    "balance": account.balance,
                    "transactions": transactions
                }
            }

        try:
            with open("users.json", "w") as f:
                json.dump(data, f, indent=2, default=str)
        except (IOError, PermissionError) as e:
            print(f"Warning: Could not save user data - {e}")
    
    def load_users(self):
        """
        Load users from JSON file and reconstruct objects
        """
        try:
            with open("users.json", "r") as f:
                data = json.load(f)
                
                for username, user_data in data.items():
                    # 1. Create User with saved name
                    user = User(user_data["name"])
                    
                    # 2. Restore account balance
                    user.account._balance = user_data["account"]["balance"]
                    
                    # 3. Restore transactions
                    user.account.transactions = [
                        {
                            "type": t["type"],
                            "amount": t["amount"],
                            "balance_after": t["balance_after"],
                            "timestamp": datetime.fromisoformat(t["timestamp"])
                        }
                        for t in user_data["account"]["transactions"]
                    ]
                    
                    # 4. Restore other user attributes if they exist
                    if "email" in user_data:
                        user.email = user_data["email"]
                    
                    # Recreate login system data
                    self.users[username] = {
                        "user": user,
                        "password": user_data["password"].encode('utf-8'),  # convert back to bytes
                        "locked": user_data["locked"],
                        "failed_attempts": user_data["failed_attempts"]
                    }
                    
        except FileNotFoundError:
            print("No existing user data found. Starting fresh.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Corrupted user data file - {e}")
        except Exception as e:
            print(f"Warning: Could not load user data - {e}")


        
