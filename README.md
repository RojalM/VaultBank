# SecureBank – A Secure Banking System in Python

SecureBank is a simple yet powerful banking system written in Python. It is designed with a focus on **security**, **usability**, and **extendability**. Users can register, log in securely with hashed passwords, and manage their personal account – including deposits, withdrawals, and transaction history.

---

## 🔐 Features

- **User Authentication**
  - Secure password hashing using bcrypt
  - Account lockout after multiple failed login attempts
- **Bank Account Management**
  - Balance tracking
  - Deposits and withdrawals with validation
  - Monthly reports and transaction summaries
  - Transaction categorization and sorting
- **Persistence**
  - JSON-based storage for users and accounts
  - Transaction history retained across sessions
- **Security First**
  - Defensive programming practices
  - Protection against invalid operations and misuse

---

## 🧱 Structure

```bash
LearnProject/
│
├── Account.py          # Account logic, balance, transactions
├── User.py             # User class, extends Person
├── LoginSystem.py      # Registration, login, user management
├── Person.py           # Base class for user (can be extended)
├── users.json          # Persisted data
└── main.py             # Entry point (optional)
