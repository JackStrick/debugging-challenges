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

    def get_transaction_count(self):
        """Returns the total number of transactions."""
        return len(self.transactions)

    def get_total_spend(self):
        """Returns the total amount of all debit transactions."""
        total = 0
        for t in self.transactions:
            print(t)
            print(total)
            if t["type"] == "credit":
                total += t["amount"]
        return total

    def get_transactions_above(self, threshold):
        """Returns all transactions with an amount strictly greater than threshold."""
        return [t for t in self.transactions if t["amount"] >= threshold]

    def get_top_n_by_amount(self, n):
        """Returns the top N transactions sorted by amount in descending order."""
        sorted_txns = sorted(self.transactions, key=lambda t: t["amount"])
        return sorted_txns[:n]

    def get_category_totals(self):
        """Returns a dict mapping each category to the total amount for that category."""
        totals = {}
        for t in self.transactions:
            cat = t["category"]
            if cat not in totals:
                totals[cat] = 0
            totals[cat] += t["amount"]
        return totals

    def get_net_balance(self):
        """Returns total credits minus total debits."""
        credits = sum(t["amount"] for t in self.transactions if t["type"] == "credit")
        debits = sum(t["amount"] for t in self.transactions if t["type"] == "debit")
        return debits - credits
