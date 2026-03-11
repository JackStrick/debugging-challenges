# Mock Debugging Interview — Python

This is a self-practice mock for the Brex debugging interview round.

## The program

`lib/processor.py` contains a `TransactionProcessor` class that reads a CSV of
financial transactions and exposes several analysis methods. The code has
**multiple logic bugs** — your job is to find and fix all of them.

## Setup

Make sure you have Python 3 and pytest installed:

```bash
pip install pytest
```

## Running the tests

From the `mock_interview_python/` directory:

```bash
pytest
```

Some tests will pass immediately. The failing tests are your signal — each
failure points to a bug in `lib/processor.py`.

## Rules (mirror the real interview)

- No AI / GitHub Copilot
- You may use print statements, the Python docs, or a debugger
- The bugs are **logic bugs**, not syntax errors
- There are **multiple bugs** — fix all of them to get a full green suite

## Tips

- Read what each method is *supposed* to do (the docstring) vs. what it *actually* does
- Run the tests after each fix to track your progress
- Talk through your reasoning out loud — the real interview grades your approach,
  not just the final result

Good luck!
