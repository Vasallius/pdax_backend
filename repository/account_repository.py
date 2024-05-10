from abc import ABC, abstractmethod
from typing import List, Optional

from entities.account import Account


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
