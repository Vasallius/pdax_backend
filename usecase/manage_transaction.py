from abc import ABC, abstractmethod

from entities.account import Account


class TransactionManagerInterface(ABC):
    @abstractmethod
    def make_transaction(self, account_id: str, amount: float, transaction_type: str) -> "Account":
        pass


class TransactionManager(TransactionManagerInterface):
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
