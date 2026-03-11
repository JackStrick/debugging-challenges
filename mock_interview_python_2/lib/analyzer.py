from lib.processor import TransactionProcessor


class SpendingAnalyzer:
    def __init__(self, processor: TransactionProcessor):
        self.processor = processor

    def get_monthly_summary(self):
        """Returns a dict with debit_total, credit_total, and net (credits - debits)."""
        debits = self.processor.get_debits()
        credits = self.processor.get_credits()
        debit_total = sum(t["amount"] for t in debits)
        credit_total = sum(t["amount"] for t in credits)
        return {
            "debit_total": debit_total,
            "credit_total": credit_total,
            "net": credit_total - debit_total,
        }

    def get_large_transactions(self, threshold):
        """Returns all transactions (any type) with amount >= threshold."""
        return self.processor._filter(self.processor.transactions, min_amount=threshold)

    def get_top_spending_categories(self, n):
        """Returns the top N categories by total debit spend, highest first.

        Each entry is a dict with keys 'category' and 'total'.
        """
        debits = self.processor.get_debits()
        category_totals = {}
        for t in debits:
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0) + t["amount"]
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1])
        return [{"category": cat, "total": amt} for cat, amt in sorted_cats[:n]]

    def is_over_budget(self, category, budget):
        """Returns True if spending in category meets or exceeds budget."""
        spend = self.processor.get_category_spend(category)
        return spend > budget

    def get_savings_rate(self):
        """Returns savings as a percentage of total credits (0–100).

        Savings = net (credits minus debits).
        savings_rate = (net / credit_total) * 100
        """
        summary = self.get_monthly_summary()
        if summary["credit_total"] == 0:
            return 0.0
        return (summary["debit_total"] / summary["credit_total"]) * 100
