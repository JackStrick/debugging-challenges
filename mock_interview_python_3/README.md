# Expense Report System

This codebase processes employee expense transactions for a company with
international operations. Employees submit expenses in various currencies,
and the system tracks spend, applies foreign transaction fees, flags large
expenses for review, and generates per-employee reports.

## Architecture

### `lib/rules.py`
Pure functions that encode business logic. No I/O, no state.

- `is_foreign_transaction(transaction)` — returns True if the transaction
  currency is not USD.
- `compute_foreign_fee(transaction)` — returns the 3% foreign transaction fee
  for non-USD transactions, 0.0 for USD transactions.
- `is_large_expense(transaction, threshold)` — returns True if the transaction
  amount is strictly greater than the threshold.

### `lib/ledger.py`
The `Ledger` class holds a list of transactions and provides filtered views
and aggregations. It delegates business-rule decisions to `rules.py`.

- `get_approved()` — all transactions with status `approved`.
- `get_total_spend()` — sum of all approved transaction amounts.
- `get_employee_spend()` — dict of employee → total approved spend.
- `get_total_fees()` — total foreign fees across all approved transactions.
- `get_foreign_transactions()` — approved transactions in a non-USD currency.
- `get_large_expenses(threshold)` — approved transactions strictly above threshold.

Also exports `load_transactions(file_path)` to parse the CSV.

### `lib/reporter.py`
The `Reporter` class takes a `Ledger` and builds higher-level summaries.

- `get_total_with_fees()` — total approved spend plus all foreign fees.
- `get_top_spenders(n)` — top N employees by spend, highest first.
- `get_large_expense_count(threshold)` — count of approved transactions
  strictly above threshold.
- `get_foreign_summary()` — dict with `foreign_count`, `total_fees`,
  and `fee_pct` (fees as % of total spend).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

## Running the tests

```bash
pytest
```

## Rules

- No AI / GitHub Copilot
- Logic bugs only — no syntax errors
- Multiple bugs are present
- You have 60 minutes — start the clock when you run pytest for the first time
