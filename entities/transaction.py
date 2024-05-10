class Transaction:
    def __init__(self, account_id: str, amount: float, type: str):
        self.account_id: str = account_id
        self.amount: float = amount
        self.type: str = type
