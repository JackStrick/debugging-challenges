import csv


class TransactionProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.transactions = self._load_transactions()

    def _load_transactions(self):
        transactions = []
        with open(self.file_path, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append({
                    "id": int(row["id"]),
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "type": row["type"],
                })
        return transactions

    def _filter(self, transactions, tx_type=None, min_amount=None, categories=None):
        """Filters a list of transactions.

        Args:
            tx_type:    if provided, only include transactions matching this type.
            min_amount: if provided, only include transactions with amount >= min_amount.
            categories: if provided, only include transactions whose category is in this list.
        """
        result = transactions
        if tx_type is not None:
            result = [t for t in result if t["type"] == tx_type]
        if min_amount is not None:
            result = [t for t in result if t["amount"] > min_amount]
        if categories is not None:
            result = [t for t in result if t["category"] in categories]
        return result

    def get_debits(self, min_amount=None):
        """Returns all debit transactions, optionally filtered to amount >= min_amount."""
        return self._filter(self.transactions, tx_type="debit", min_amount=min_amount)

    def get_credits(self, min_amount=None):
        """Returns all credit transactions, optionally filtered to amount >= min_amount."""
        return self._filter(self.transactions, tx_type="credit", min_amount=min_amount)

    def get_category_spend(self, category):
        """Returns the total debit amount for a single category."""
        txns = self._filter(self.transactions, tx_type="debit", categories=[category])
        return sum(t["amount"] for t in txns)
