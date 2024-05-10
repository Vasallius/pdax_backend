import uuid
from abc import ABC, abstractmethod

from entities.account import Account


class AccountManagerInterface(ABC):
    def __init__(self, account_repository):
        self.account_repository = account_repository

    @abstractmethod
    def create_account(self, customer_id: str, name: str, email: str, phone_number: str) -> "Account":
        pass


class AccountManager(AccountManagerInterface):
    def create_account(self, customer_id: str, name: str, email: str, phone_number: str) -> "Account":
        account_id = str(uuid.uuid4())
        new_account = Account(account_id, customer_id, 0)
        self.account_repository.save_account(new_account)
        return new_account
