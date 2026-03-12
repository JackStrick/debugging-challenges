# Expense Processing Pipeline

This codebase implements a multi-stage pipeline for processing employee expense
transactions. The company operates internationally, so transactions can be charged
in multiple currencies and attract foreign transaction fees.

## Data Model

The pipeline moves data through three object types:

```
Transaction  →  ProcessedTransaction  →  EmployeeSummary
  (raw CSV)       (+ fee, net_amount,      (aggregated per
                    is_reimbursable)          employee)
```

## Architecture

### `lib/models.py`
Defines the three data classes above. No I/O, no business logic — pure data
containers and derived fields.

### `lib/processor.py`
Loads the CSV into `Transaction` objects and transforms each one into a
`ProcessedTransaction`. Contains the business rules for fee calculation
and reimbursability.

- `load_transactions(file_path)` — parses CSV → list of `Transaction`
- `process_all(transactions)` — applies rules → list of `ProcessedTransaction`

### `lib/aggregator.py`
Groups `ProcessedTransaction` objects by employee and builds one
`EmployeeSummary` per employee.

- `group_by_employee(processed)` — returns dict of employee_id → [ProcessedTransaction]
- `build_summaries(processed)` — returns list of `EmployeeSummary`

### `lib/reporter.py`
Produces company-level reports from a list of `EmployeeSummary` objects.

- `get_total_company_spend(summaries)` — sum of all net_amounts
- `get_top_spenders(summaries, n)` — top N employees by total_spend
- `get_reimbursable_summary(summaries)` — counts of reimbursable transactions
- `get_fee_report(summaries)` — total fees and highest-fee employee

## Business Rules

- **Foreign fee**: 3% of the transaction amount, applied to any non-USD transaction.
- **net_amount**: the full cost to the company = transaction amount + foreign fee.
- **Reimbursable**: a transaction is reimbursable only when its status is `approved`
  and its amount is greater than zero. Transactions with status `pending` or `denied`
  are not reimbursable.

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
- Multiple bugs are present across multiple files
- Start a 60-minute timer when you first run pytest
