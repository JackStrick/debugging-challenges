# Debugging Challenges

Self-practice mocks for debugging interviews. Each challenge is a small codebase with **intentional logic bugs** — your job is to find and fix them using tests as your guide.

Challenges get **slightly more difficult** as you go: same style of exercise, but more moving parts and trickier bugs.

---

## Challenges (in order)

| # | Folder | Difficulty | What to expect |
|---|--------|------------|----------------|
| 1 | [mock_interview_python_1](mock_interview_python_1/) | Intro | Single module (`lib/processor.py`). Multiple logic bugs in one place. Good warm-up. |
| 2 | [mock_interview_python_2](mock_interview_python_2/) | Harder | Two modules (`processor.py` + `analyzer.py`) that work together. Bugs can be in either file; tests exercise both. |

Do them in order if you want the gradual ramp. Each folder has its own README with setup and rules.

---

## Quick start (per challenge)

1. `cd` into the challenge folder (e.g. `mock_interview_python_1`).
2. Install deps: `pip install pytest`
3. Run: `pytest`
4. Use failing tests to find and fix the bugs. No AI — docs, print, and a debugger are fair game.

Good luck.
