from LearnProject.Person import Person
from LearnProject.Account import Account

class User(Person):  
    def __init__(self, name):
        super().__init__(name)  # Initialize from Person
        self.account = Account(self)  # Create an account linked to this User

    def welcome_message(self):
        return f"Welcome {self.name}, your balance is {self.account.local_currency_formatter()}"
