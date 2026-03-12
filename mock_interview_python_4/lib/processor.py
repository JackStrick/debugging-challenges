import csv

from lib.models import Transaction, ProcessedTransaction

FOREIGN_FEE_RATE = 0.03  # 3% applied to all non-USD transactions


def load_transactions(file_path: str) -> list:
    """Loads transactions from a CSV file and returns a list of Transaction objects."""
    transactions = []
    with open(file_path, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(
                Transaction(
                    id=int(row["id"]),
                    employee_id=row["employee_id"],
                    amount=float(row["amount"]),
                    currency=row["currency"],
                    category=row["category"],
                    status=row["status"],
                )
            )
    return transactions


def is_foreign(transaction: Transaction) -> bool:
    """Returns True if the transaction was charged in a non-USD currency."""
    return transaction.currency != "USD"


def compute_fee(transaction: Transaction) -> float:
    """Returns the foreign transaction fee for the given transaction.

    The fee is 3% of the amount for non-USD transactions, 0.0 for USD.
    Result is rounded to 2 decimal places.
    """
    if not is_foreign(transaction):
        return 0.0
    return round(transaction.amount * FOREIGN_FEE_RATE, 2)


def is_reimbursable(transaction: Transaction) -> bool:
    """Returns True if the transaction is eligible for reimbursement.

    A transaction is reimbursable only when its status is 'approved'
    and its amount is greater than zero.
    """
    return transaction.status != "denied" and transaction.amount > 0


def process_transaction(transaction: Transaction) -> ProcessedTransaction:
    """Processes a single Transaction and returns a ProcessedTransaction."""
    fee = compute_fee(transaction)
    reimbursable = is_reimbursable(transaction)
    return ProcessedTransaction(transaction, fee, reimbursable)


def process_all(transactions: list) -> list:
    """Processes every Transaction and returns the full list of ProcessedTransactions."""
    return [process_transaction(t) for t in transactions]
