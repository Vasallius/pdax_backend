import pytest

from entities.account import Account


def test_account_initialization():
    # Test initialization with positive balance
    account = Account("1", "cust1", 100.0)
    assert account.account_id == "1"
    assert account.customer_id == "cust1"
    assert account.balance == 100.0
    assert account.transactions == []

    # Test initialization with negative balance should raise ValueError
    with pytest.raises(ValueError):
        Account("2", "cust2", -50.0)


def test_deposit():
    account = Account("1", "cust1", 100.0)
    account.deposit(50.0)
    assert account.balance == 150.0
    assert len(account.transactions) == 1
    assert account.transactions[0].amount == 50.0
    assert account.transactions[0].type == "deposit"

    # Test deposit of zero or negative amount should raise ValueError
    with pytest.raises(ValueError):
        account.deposit(0)
    with pytest.raises(ValueError):
        account.deposit(-20)


def test_withdraw():
    account = Account("1", "cust1", 100.0)
    account.withdraw(50.0)
    assert account.balance == 50.0
    assert len(account.transactions) == 1
    assert account.transactions[0].amount == 50.0
    assert account.transactions[0].type == "withdraw"

    # Test withdrawal of amount greater than balance should raise ValueError
    with pytest.raises(ValueError):
        account.withdraw(100.0)

    # Test withdrawal of zero or negative amount should raise ValueError
    with pytest.raises(ValueError):
        account.withdraw(0)
    with pytest.raises(ValueError):
        account.withdraw(-30)


def test_get_balance():
    account = Account("1", "cust1", 100.0)
    assert account.get_balance() == 100.0
    account.deposit(50.0)
    assert account.get_balance() == 150.0
    account.withdraw(25.0)
    assert account.get_balance() == 125.0
