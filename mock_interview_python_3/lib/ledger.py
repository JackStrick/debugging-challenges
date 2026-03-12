import csv

from lib.rules import compute_foreign_fee, is_large_expense


def load_transactions(file_path):
    """Loads transactions from a CSV file and returns them as a list of dicts."""
    transactions = []
    with open(file_path, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "id": int(row["id"]),
                "employee": row["employee"],
                "amount": float(row["amount"]),
                "currency": row["currency"],
                "category": row["category"],
                "status": row["status"],
            })
    return transactions


class Ledger:
    def __init__(self, transactions):
        self.transactions = transactions

    def get_approved(self):
        """Returns all transactions with status 'approved'."""
        return [t for t in self.transactions if t["status"] == "approved"]

    def get_total_spend(self):
        """Returns the sum of all approved transaction amounts."""
        return sum(t["amount"] for t in self.get_approved())

    def get_employee_spend(self):
        """Returns a dict mapping each employee to their total approved spend."""
        result = {}
        for t in self.get_approved():
            emp = t["employee"]
            result[emp] = result.get(emp, 0) + t["amount"]
        return result

    def get_total_fees(self):
        """Returns the total foreign transaction fees across all approved transactions."""
        return round(sum(compute_foreign_fee(t) for t in self.get_approved()), 2)

    def get_foreign_transactions(self):
        """Returns all approved transactions made in a non-USD currency."""
        return [t for t in self.get_approved() if t["currency"] == "USD"]

    def get_large_expenses(self, threshold):
        """Returns all approved transactions with amount strictly greater than threshold."""
        return [t for t in self.get_approved() if is_large_expense(t, threshold)]
