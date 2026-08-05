# AI Usage Rules

Concrete rules, not vibes — grounded in what actually happened in this
repo (see docs/governance-worksheet.md for the evidence behind each).

1. **Never paste** `.env` values, credentials, API keys, tokens, or
   real personal/customer data into any AI tool, in any prompt, ever —
   only placeholder values from `.env.example` are shareable.
2. **Always verify** a generated file against the actual running app
   or test suite before treating it as done — specifically: run
   `python -m pytest -v` (not bare `pytest`) after any change to
   `app/`, and re-read config files (CI YAML, Dockerfile) end-to-end
   rather than skimming the first few lines, since the pytest-in-CI
   bug here was hiding in the last line of the workflow file.
3. **Record AI contributions** by noting, in the relevant `docs/`
   file, what an AI tool drafted, what I changed, and what I verified
   — as done in this review pass for the CORS finding correction and
   the `business_rules.py` deduplication.
4. **Grade AI review/security findings** (Useful/Noise/Wrong or
   Valid/False Positive/Noise) before acting on any of them — never
   apply a suggested fix straight from an AI comment without checking
   it against the actual file first (the `*`-wildcard CORS claim and
   the SQL-injection false positive in this repo are the concrete
   examples of why).
5. **Diff-check generated files for exact duplication**, not just
   correctness — a file can run perfectly with its entire contents
   copy-pasted twice (as `business_rules.py` did here) and nothing
   about "the tests pass" would catch that.
