import datetime
import uuid
from abc import ABC, abstractmethod


class AccountRepositoryInterface(ABC):
    @abstractmethod
    def save_account(self, account):
        pass

    @abstractmethod
    def find_account_by_id(self, account_id):
        pass

    @abstractmethod
    def find_accounts_by_customer_id(self, customer_id):
        pass


class Account:
    def __init__(self, account_id, customer_id, balance, transactions=None):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.account_id = account_id
        self.customer_id = customer_id
        self.balance = balance
        self.transactions = transactions if transactions is not None else []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(Transaction(self.account_id, amount, "deposit"))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(Transaction(self.account_id, amount, "withdraw"))


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number


class Transaction:
    def __init__(self, account_id, amount, type):
        self.account_id = account_id
        self.amount = amount
        self.type = type


class UseCase:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, customer_id, name, email, phone_number):
        account_id = str(uuid.uuid4())
        new_account = Account(account_id, customer_id, 0)
        self.account_repository.save_account(new_account)
        return new_account

    def make_transaction(self, account_id, amount, transaction_type):
        account = self.account_repository.find_account_by_id(account_id)
        if account is None:
            raise ValueError("Account not found")

        if transaction_type == "deposit":
            account.deposit(amount)
        elif transaction_type == "withdraw":
            try:
                account.withdraw(amount)
            except ValueError:
                raise ValueError("Insufficient funds")
        else:
            raise ValueError("Invalid transaction type")

        self.account_repository.save_account(account)
        return account

    def generate_account_statement(self, account_id):
        account = self.account_repository.find_account_by_id(account_id)
        if account is None:
            raise ValueError("Account not found")

        statement = ""
        for transaction in account.transactions:
            statement += f"{transaction.amount} {transaction.type}\n"

        return statement


class AccountRepository(AccountRepositoryInterface):
    def __init__(self):
        self.accounts = {}

    def save_account(self, account):
        self.accounts[account.account_id] = account
        return account

    def find_account_by_id(self, account_id):
        return self.accounts.get(account_id)

    def find_accounts_by_customer_id(self, customer_id):
        return [account for account in self.accounts.values() if account.customer_id == customer_id]


repo = AccountRepository()
use_case = UseCase(repo)

# customer1 = Customer(1, "Jed", "jed@pdax.com", "00000")
# customer2 = Customer(1, "Jed", "jed@pdax.com", "10101")
# account2 = use_case.create_account(customer2.customer_id, customer2.name, customer2.email, customer2.phone_number)
# account1 = use_case.create_account(customer1.customer_id, customer1.name, customer1.email, customer1.phone_number)

# Create some customers
customer1 = Customer(1, "John Doe", "john@example.com", "12345")
customer2 = Customer(2, "Jane Smith", "jane@example.com", "67890")

# Create accounts for the customers
account1 = use_case.create_account(customer1.customer_id, customer1.name, customer1.email, customer1.phone_number)
account2 = use_case.create_account(customer2.customer_id, customer2.name, customer2.email, customer2.phone_number)

# Make deposits and withdrawals
use_case.make_transaction(account1.account_id, 100, "deposit")
use_case.make_transaction(account2.account_id, 500, "deposit")
use_case.make_transaction(account1.account_id, 50, "withdraw")
use_case.make_transaction(account2.account_id, 200, "withdraw")

# Generate account statements
statement1 = use_case.generate_account_statement(account1.account_id)
# statement2 = use_case.generate_account_statement(account2.account_id)

# Print the statements
print(statement1)
# print(statement2)

# Find accounts by customer ID
# accounts_for_customer1 = repo.find_accounts_by_customer_id(customer1.customer_id)
# print(accounts_for_customer1)

# print(repo.find_accounts_by_customer_id(1))
