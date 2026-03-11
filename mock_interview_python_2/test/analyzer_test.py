import pytest
from lib.processor import TransactionProcessor
from lib.analyzer import SpendingAnalyzer

INPUT_FOLDER = "input/"


@pytest.fixture
def processor():
    return TransactionProcessor(INPUT_FOLDER + "transactions.csv")


@pytest.fixture
def analyzer(processor):
    return SpendingAnalyzer(processor)


# ── Passing tests ──────────────────────────────────────────────────────────────

def test_monthly_summary_totals(analyzer):
    """Totals across all debits and credits, no threshold filtering."""
    summary = analyzer.get_monthly_summary()
    assert summary["debit_total"] == 700.00
    assert summary["credit_total"] == 1000.00
    assert summary["net"] == 300.00


def test_category_spend(processor):
    """Total debit spend per category — no threshold involved."""
    assert processor.get_category_spend("travel") == 350.00
    assert processor.get_category_spend("food") == 150.00
    assert processor.get_category_spend("entertainment") == 100.00


# ── Failing tests (bugs to find and fix) ──────────────────────────────────────

def test_large_transactions(analyzer):
    """All transactions (any type) with amount >= 100.
    Qualifying ids: 1(100), 2(150), 3(600), 4(200), 6(100), 7(400), 8(100) → 7 results.
    """
    result = analyzer.get_large_transactions(100)
    assert len(result) == 7


def test_debits_above_threshold(processor):
    """Debit transactions with amount >= 100.
    Qualifying ids: 1(100), 2(150), 4(200), 6(100), 8(100) → 5 results.
    """
    result = processor.get_debits(min_amount=100)
    assert len(result) == 5


def test_top_spending_categories(analyzer):
    """Top 2 categories by debit spend, highest first."""
    result = analyzer.get_top_spending_categories(2)
    assert result[0]["category"] == "travel"
    assert result[0]["total"] == 350.00
    assert result[1]["category"] == "food"
    assert result[1]["total"] == 150.00


def test_is_over_budget_at_limit(analyzer):
    """Spending that exactly meets the budget should count as over budget."""
    # food total debit = 150.00; at-budget means over
    assert analyzer.is_over_budget("food", 150.00) is True


def test_savings_rate(analyzer):
    """Savings rate = (net / credit_total) * 100.
    net = 300.00, credit_total = 1000.00 → 30.0%
    """
    assert analyzer.get_savings_rate() == 30.0
