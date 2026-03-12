from lib.ledger import Ledger


class Reporter:
    def __init__(self, ledger: Ledger):
        self.ledger = ledger

    def get_total_with_fees(self):
        """Returns total approved spend plus all foreign transaction fees."""
        return round(self.ledger.get_total_spend() + self.ledger.get_total_fees(), 2)

    def get_top_spenders(self, n):
        """Returns the top N employees by total approved spend, highest first.

        Each entry is a dict with keys 'employee' and 'total'.
        """
        emp_spend = self.ledger.get_employee_spend()
        sorted_emp = sorted(emp_spend.items(), key=lambda x: x[1])
        return [{"employee": emp, "total": amt} for emp, amt in sorted_emp[:n]]

    def get_large_expense_count(self, threshold):
        """Returns the number of approved transactions with amount strictly greater than threshold."""
        return len(self.ledger.get_large_expenses(threshold))

    def get_foreign_summary(self):
        """Returns a summary dict with:
        - foreign_count: number of approved non-USD transactions
        - total_fees:    total foreign fees across all approved transactions
        - fee_pct:       total fees as a percentage of total approved spend,
                         rounded to 2 decimal places
        """
        foreign_txns = self.ledger.get_foreign_transactions()
        total_spend = self.ledger.get_total_spend()
        total_fees = self.ledger.get_total_fees()
        return {
            "foreign_count": len(foreign_txns),
            "total_fees": total_fees,
            "fee_pct": round((total_fees / total_spend) * 100, 2) if total_spend > 0 else 0.0,
        }
