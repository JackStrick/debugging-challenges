import pytest
from lib.ledger import Ledger, load_transactions
from lib.reporter import Reporter

INPUT_FOLDER = "input/"


@pytest.fixture
def ledger():
    transactions = load_transactions(INPUT_FOLDER + "transactions.csv")
    return Ledger(transactions)


@pytest.fixture
def reporter(ledger):
    return Reporter(ledger)


def test_case_1(ledger):
    assert ledger.get_total_spend() == 3100.00


def test_case_2(ledger):
    spend = ledger.get_employee_spend()
    assert spend["alice"] == 1100.00
    assert spend["bob"] == 270.00
    assert spend["carol"] == 1730.00


def test_case_3(reporter):
    assert reporter.get_total_with_fees() == 3108.10


def test_case_4(reporter):
    assert reporter.get_large_expense_count(500) == 2


def test_case_5(ledger):
    result = ledger.get_large_expenses(500)
    assert len(result) == 2


def test_case_6(reporter):
    summary = reporter.get_foreign_summary()
    assert summary["foreign_count"] == 2
    assert summary["total_fees"] == 8.10
    assert summary["fee_pct"] == 0.26


def test_case_7(reporter):
    result = reporter.get_top_spenders(2)
    assert result[0]["employee"] == "carol"
    assert result[1]["employee"] == "alice"
