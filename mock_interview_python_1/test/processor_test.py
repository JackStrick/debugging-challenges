import pytest
from lib.processor import TransactionProcessor

INPUT_FOLDER = "input/"


@pytest.fixture
def processor():
    return TransactionProcessor(INPUT_FOLDER + "transactions.csv")


# ── Passing tests ──────────────────────────────────────────────────────────────

def test_transaction_count(processor):
    """There are 7 rows in the CSV."""
    assert processor.get_transaction_count() == 7


def test_category_totals(processor):
    """Each category sums correctly."""
    totals = processor.get_category_totals()
    assert totals["food"] == 195.25          # 150.00 + 45.25
    assert totals["travel"] == 275.50        # 75.50 + 200.00
    assert totals["salary"] == 500.00
    assert totals["entertainment"] == 100.00
    assert totals["bonus"] == 350.00


# ── Failing tests (bugs to find and fix) ──────────────────────────────────────

def test_total_spend(processor):
    """Total of all debit transactions.
    Debits: 150.00 + 75.50 + 200.00 + 45.25 + 100.00 = 570.75
    """
    assert processor.get_total_spend() == 570.75


def test_transactions_above(processor):
    """Transactions with amount *strictly* greater than 100.
    Qualifying ids: 1 (150), 3 (500), 4 (200), 7 (350) → 4 results.
    """
    result = processor.get_transactions_above(100)
    assert len(result) == 4


def test_top_3_by_amount(processor):
    """Top 3 transactions by amount, highest first."""
    result = processor.get_top_n_by_amount(3)
    assert result[0]["amount"] == 500.00
    assert result[1]["amount"] == 350.00
    assert result[2]["amount"] == 200.00


def test_net_balance(processor):
    """Net balance = total credits − total debits.
    Credits: 500.00 + 350.00 = 850.00
    Debits:  570.75
    Net:     279.25
    """
    assert processor.get_net_balance() == 279.25
