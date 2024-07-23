from entities.customer import Customer
from repository.account_repository import AccountRepository
from usecase.create_account import AccountManager
from usecase.generate_account_statement import StatementManager
from usecase.manage_transaction import TransactionManager

account_repository = AccountRepository()
account_manager = AccountManager(account_repository)
transacton_manager = TransactionManager(account_repository)
statement_manager = StatementManager(account_repository)


# Create some customers
customer1 = Customer(1, "Jed Tan", "jed@pdax.com", "000000000")

# Create accounts for the customers
# Why not just take in a Customer object?
# Spec says "create_account() that takes customer_id, name, email, and phone_number as input"
account = account_manager.create_account(customer1.customer_id, customer1.name, customer1.email, customer1.phone_number)

# Make deposits and withdrawals

# Perform a deposit
transacton_manager.make_transaction(account.account_id, 500, "deposit")
print(f"After deposit, balance: {account.get_balance()}")

# Perform a withdrawal
try:
    transacton_manager.make_transaction(account.account_id, 200, "withdraw")
    print(f"After withdrawal, balance: {account.get_balance()}")
except ValueError as e:
    print(e)

# Attempt an invalid transaction
try:
    transacton_manager.make_transaction(account.account_id, 1000, "withdraw")
except ValueError as e:
    print(e)

# Generate and print the account statement
statement = statement_manager.generate_account_statement(account.account_id)
print("Account Statement:")
print(statement)

# Add and test another account for the same customer to test account retrieval by customer ID
second_account = account_manager.create_account(2, "Satoshi", "satoshi@gmail.com", "4242424242")
third_account = account_manager.create_account(2, "Satoshi", "satoshi@gmail.com", "4242424242")

account = account_repository.find_account_by_id(second_account.account_id)
print(f"Account found with account ID: {account.account_id}, Balance: {account.get_balance()}")

accounts = account_repository.find_accounts_by_customer_id(2)
print(f"Accounts found with customer ID 2: {len(accounts)}")
for acc in accounts:
    print(f"  Account ID: {acc.account_id}, Balance: {acc.get_balance()}")
