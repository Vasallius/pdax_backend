import uuid


class Account:
    def __init__(self, account_id, customer_id, balance):
        self.account_id = account_id
        self.customer_id = customer_id
        # self.account_number = account_number
        self.balance = balance


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number


class UseCase:
    @staticmethod
    def create_account(customer_id, name, email, phone_number):
        account_id = str(uuid.uuid4())
        return Account(account_id, customer_id, 0)


class AccountRepository:

    def __init__(self):
        self.accounts = {}

    def save_account(self, account):
        self.accounts.append(account)
        return account

    def find_account_by_id(self, account_id):
        return self.accounts.get(account_id)

    def find_accounts_by_customer_id(self, customer_id):
        return [account for account in self.accounts if account.customer_id == customer_id]
