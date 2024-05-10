import uuid


class Account:
    def __init__(self, account_id, customer_id, balance):
        self.account_id = account_id
        self.customer_id = customer_id
        # self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_balance(self):
        return self.balance


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number


class UseCase:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, customer_id, name, email, phone_number):
        account_id = str(uuid.uuid4())
        new_account = Account(account_id, customer_id, 0)
        self.account_repository.save_account(new_account)
        return new_account


class AccountRepository:
    def __init__(self):
        self.accounts = {}  # Key: account_id, Value: Account object

    def save_account(self, account):
        """Stores the account in the repository."""
        self.accounts[account.account_id] = account
        return account

    def find_account_by_id(self, account_id):
        """Finds an account by account_id."""
        return self.accounts.get(account_id)

    def find_accounts_by_customer_id(self, customer_id):
        """Finds all accounts belonging to a specific customer_id."""
        return [account for account in self.accounts.values() if account.customer_id == customer_id]


repo = AccountRepository()
use_case = UseCase(repo)

customer1 = Customer(1, "Jed", "jed@pdax.com", "00000")
customer2 = Customer(1, "Jed", "jed@pdax.com", "10101")
account1 = use_case.create_account(customer1.customer_id, customer1.name, customer1.email, customer1.phone_number)
account2 = use_case.create_account(customer2.customer_id, customer2.name, customer2.email, customer2.phone_number)


print(repo.find_accounts_by_customer_id(1))
