import uuid
from abc import ABC, abstractmethod
from typing import List, Optional


class AccountRepositoryInterface(ABC):
    @abstractmethod
    def save_account(self, account: "Account") -> "Account":
        pass

    @abstractmethod
    def find_account_by_id(self, account_id: str) -> Optional["Account"]:
        pass

    @abstractmethod
    def find_accounts_by_customer_id(self, customer_id: str) -> List["Account"]:
        pass


class Account:
    def __init__(
        self, account_id: str, customer_id: str, balance: float, transactions: Optional[List["Transaction"]] = None
    ):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.account_id: str = account_id
        self.customer_id: str = customer_id
        self.balance: float = balance
        self.transactions: List["Transaction"] = transactions if transactions is not None else []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(Transaction(self.account_id, amount, "deposit"))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(Transaction(self.account_id, amount, "withdraw"))

    def get_balance(self) -> float:
        return self.balance


class Customer:
    def __init__(self, customer_id: str, name: str, email: str, phone_number: str):
        self.customer_id: str = customer_id
        self.name: str = name
        self.email: str = email
        self.phone_number: str = phone_number


class Transaction:
    def __init__(self, account_id: str, amount: float, type: str):
        self.account_id: str = account_id
        self.amount: float = amount
        self.type: str = type


class UseCase:
    def __init__(self, account_repository: "AccountRepository"):
        self.account_repository: "AccountRepository" = account_repository

    def create_account(self, customer_id: str, name: str, email: str, phone_number: str) -> "Account":
        account_id = str(uuid.uuid4())
        new_account = Account(account_id, customer_id, 0)
        self.account_repository.save_account(new_account)
        return new_account

    def make_transaction(self, account_id: str, amount: float, transaction_type: str) -> "Account":
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

    def generate_account_statement(self, account_id: str) -> str:
        account = self.account_repository.find_account_by_id(account_id)
        if account is None:
            raise ValueError("Account not found")

        statement = ""
        for transaction in account.transactions:
            statement += f"{transaction.amount} {transaction.type}\n"

        return statement


class AccountRepository(AccountRepositoryInterface):
    def __init__(self):
        self.accounts: dict[str, "Account"] = {}

    def save_account(self, account: "Account") -> "Account":
        self.accounts[account.account_id] = account
        return account

    def find_account_by_id(self, account_id: str) -> Optional["Account"]:
        return self.accounts.get(account_id)

    def find_accounts_by_customer_id(self, customer_id: str) -> List["Account"]:
        return [account for account in self.accounts.values() if account.customer_id == customer_id]


account_repository = AccountRepository()
use_case = UseCase(account_repository)


# Create some customers
customer1 = Customer(1, "Jed Tan", "jed@pdax.com", "000000000")

# Create accounts for the customers
account = use_case.create_account(customer1.customer_id, customer1.name, customer1.email, customer1.phone_number)

# Make deposits and withdrawals
# Perform a deposit
use_case.make_transaction(account.account_id, 500, "deposit")
print(f"After deposit, balance: {account.get_balance()}")

# Perform a withdrawal
try:
    use_case.make_transaction(account.account_id, 200, "withdraw")
    print(f"After withdrawal, balance: {account.get_balance()}")
except ValueError as e:
    print(e)

# Attempt an invalid transaction
try:
    use_case.make_transaction(account.account_id, 1000, "withdraw")
except ValueError as e:
    print(e)

# Generate and print the account statement
statement = use_case.generate_account_statement(account.account_id)
print("Account Statement:")
print(statement)

# Add and test another account for the same customer to test account retrieval by customer ID
second_account = use_case.create_account(2, "Satoshi", "satoshi@gmail.com", "4242424242")
third_account = use_case.create_account(2, "Satoshi", "satoshi@gmail.com", "4242424242")

account = account_repository.find_account_by_id(second_account.account_id)
print(f"Account found with account ID: {account.account_id}, Balance: {account.get_balance()}")

accounts = account_repository.find_accounts_by_customer_id(2)
print(f"Accounts found with customer ID 2: {len(accounts)}")
for acc in accounts:
    print(f"  Account ID: {acc.account_id}, Balance: {acc.get_balance()}")
