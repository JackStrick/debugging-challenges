import pytest
from lib.processor import load_transactions, process_all
from lib.aggregator import build_summaries
from lib.reporter import (
    get_total_company_spend,
    get_top_spenders,
    get_reimbursable_summary,
    get_fee_report,
)

INPUT_FOLDER = "input/"


@pytest.fixture
def raw_transactions():
    return load_transactions(INPUT_FOLDER + "transactions.csv")


@pytest.fixture
def processed(raw_transactions):
    return process_all(raw_transactions)


@pytest.fixture
def summaries(processed):
    return build_summaries(processed)


def test_case_1(raw_transactions, processed):
    original = raw_transactions[2]
    result = processed[2]
    assert result.transaction is original
    assert result.fee == 0.0
    assert result.net_amount == 50.00
    assert result.is_reimbursable is True


def test_case_2(summaries):
    total_fees = round(sum(s.total_fees for s in summaries), 2)
    assert total_fees == 8.10


def test_case_3(summaries):
    assert get_total_company_spend(summaries) == 3273.10


def test_case_4(summaries):
    result = get_top_spenders(summaries, 2)
    assert result[0].employee_id == "carol"
    assert result[1].employee_id == "alice"


def test_case_5(summaries):
    result = get_reimbursable_summary(summaries)
    assert result["total_reimbursable_count"] == 8
    assert result["employees_with_reimbursable"] == 3


def test_case_6(summaries):
    result = get_fee_report(summaries)
    assert result["total_fees"] == 8.10
    assert result["highest_fee_payer"] == "bob"


def test_case_7(summaries):
    by_employee = {s.employee_id: s for s in summaries}
    assert "alice" in by_employee
    assert "bob" in by_employee
    assert "carol" in by_employee
    assert by_employee["alice"].total_spend == 1220.00
    assert by_employee["carol"].total_spend == 1730.00
