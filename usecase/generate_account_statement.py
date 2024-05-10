from abc import ABC, abstractmethod


class StatementManagerInterface(ABC):

    def __init__(self, account_repository):
        self.account_repository = account_repository

    @abstractmethod
    def generate_account_statement(self, account_id: str) -> str:
        pass


class StatementManager(StatementManagerInterface):
    def generate_account_statement(self, account_id: str) -> str:
        account = self.account_repository.find_account_by_id(account_id)
        if account is None:
            raise ValueError("Account not found")

        statement = ""
        for transaction in account.transactions:
            statement += f"{transaction.amount} {transaction.type}\n"

        return statement
