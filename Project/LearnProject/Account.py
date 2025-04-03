from datetime import datetime
import locale
from collections import defaultdict, deque

class Account:
    def __init__(self, user):
        self.user = user  # Link to the User
        self._balance = 0  # Default balance is 
        self.transactions = [] # transaction list
        self._recent_transactions = deque(maxlen=5)

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value is None:
            raise ValueError("Balance cannot be None")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def local_currency_formatter(self):
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')  # System default
        return locale.currency(self.balance, grouping=True)
    
    def deposit(self, value):
        if value <= 0:
            raise ValueError("The value should be positive")
        self._balance += value
        print("balance has been updated sucessfully")
        self.transactions.append({
            "type": "deposit",
            "amount": value,
            "balance_after": self._balance,  # Changed from "balance"
            "timestamp": datetime.now().isoformat()
        })
    
    def withdraw(self, value):
        if value <= 0:
            raise ValueError("The value should be positive")
        if value > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= value
        self.transactions.append({
            "type": "withdrawal",  # Changed from "withdraw" for consistency
            "amount": value,
            "balance_after": self._balance,  # Changed from "balance"
            "timestamp": datetime.now().isoformat()
        })

    def view_balance(self):
        return self.local_currency_formatter()
    
    def generate_monthly_report(self, month: int, year: int):
        try:
            month = int(month)  # Convert to integer for correct comparison
            year = int(year)

            filtered_dict = defaultdict(list)

            for tr in self.transactions:
                if "timestamp" in tr and "type" in tr and "money_amount" in tr:
                    try:
                        tr_date = datetime.fromisoformat(tr["timestamp"])
                        if tr_date.month == month and tr_date.year == year:
                            filtered_dict[tr["type"]].append(tr["money_amount"])
                    except ValueError:
                        print(f"Invalid timestamp format: {tr['timestamp']}")
            
            # Convert defaultdict to normal dict
            filtered_dict = dict(filtered_dict)

            # Calculate totals safely
            total_deposit = sum(filtered_dict.get("deposit", []))
            total_withdraw = sum(filtered_dict.get("withdraw", []))

            # Return structured output
            return {
                "transactions_by_type": filtered_dict,
                "total_deposit": total_deposit,
                "total_withdraw": total_withdraw,
                "net_balance": total_deposit - total_withdraw
            }

        except Exception as e:
            print(f"Something went wrong: {e}")
            return {"error": str(e)}
        
    def categorize_transactions(self):
        categories = defaultdict(list)
        for t in self.transactions:
            categories[t["type"]].append(t["amount"])
        return categories

    def sort_transactions(self, on_what: str):
        if not self.transactions:
            return []

        if on_what not in self.transactions[0]:
            raise KeyError(f"Invalid key: {on_what}")

        self.transactions.sort(key=lambda tr: tr[on_what])
        return self.transactions

    





    


