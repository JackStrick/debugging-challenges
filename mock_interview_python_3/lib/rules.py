FOREIGN_FEE_RATE = 0.03  # 3% fee applied to all non-USD transactions


def is_foreign_transaction(transaction):
    """Returns True if the transaction was charged in a non-USD currency."""
    return transaction["currency"] != "USD"


def compute_foreign_fee(transaction):
    """Returns the foreign transaction fee for the given transaction.

    The fee is 3% of the transaction amount, applied only to non-USD transactions.
    Returns 0.0 for USD transactions. Result is rounded to 2 decimal places.
    """
    if not is_foreign_transaction(transaction):
        return 0.0
    return round(transaction["amount"] * FOREIGN_FEE_RATE, 2)


def is_large_expense(transaction, threshold):
    """Returns True if the transaction amount is strictly greater than threshold."""
    return transaction["amount"] >= threshold
