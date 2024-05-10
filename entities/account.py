from typing import List, Optional


from entities.transaction import Transaction


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
