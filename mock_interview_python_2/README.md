# Mock Debugging Interview (Hard) — Python

This is an advanced self-practice mock for a debugging interview round.

## Architecture

The codebase has two modules that work together:

- **`lib/processor.py`** — `TransactionProcessor`: loads the CSV and provides
  low-level filtering and aggregation methods.
- **`lib/analyzer.py`** — `SpendingAnalyzer`: takes a `TransactionProcessor` and
  builds higher-level spending insights on top of it.

The test file exercises both classes together.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

## Running the tests

From the `mock_interview_hard_python/` directory:

```bash
pytest
```

## Rules (mirror the real interview)

- No AI / GitHub Copilot
- You may use print statements, the Python docs, or a debugger
- The bugs are **logic bugs**, not syntax errors
- There are **multiple bugs** spread across the two files

## Tips for a deterministic approach

- Run `pytest` first and read *all* failure messages before touching any code.
- Notice which tests fail — do any share a common method in their call chain?
  If multiple tests fail for seemingly different reasons, look for a shared
  helper that all of them pass through.
- Form a written (or spoken) hypothesis about each bug before editing anything.
- Fix one bug at a time and re-run after each fix.

Good luck!
