# Governance Retrospective

A review of what was shared with AI tools and what was received back
across this course, with risk classifications and the rules that came
out of it (rules are in docs/ai-usage.md).

## What I shared with AI

| What I shared | Risk level | Reason |
|---|---|---|
| Task Tracker source code (`app/`, `tests/`) | Low | Course-only sample code, no secrets, nothing proprietary. |
| Test output and stack traces (e.g. the `ModuleNotFoundError` from bare `pytest`) | Low | Local error output about a public, well-known Python import-path issue — no sensitive paths or data in the trace. |
| Dockerfile, CI YAML, README snippets | Low | Public-pattern config files; nothing environment-specific or secret. |
| `.env.example` (template only, placeholder values) | Low | Contains only placeholder keys (`PORT`, `APP_ENV`), never real values. |
| Real `.env` values, credentials, tokens | N/A — never shared | This is a non-negotiable (see docs/ai-usage.md rule 1); I never pasted real secrets into any AI tool this course. |

## What I received from AI

| What I received | Notes |
|---|---|
| Backend models, validators, route handlers (`app/models.py`, `app/main.py`) | Accepted after reading and testing; I can explain every field and validator. |
| Status-transition business rule (`app/business_rules.py`) | Accepted, but I found a copy-paste duplication bug in the file during this review pass — a reminder that "it ran fine" isn't the same as "I read the diff." Fixed after finding it, not before. |
| CI workflow (`.github/workflows/ci.yml`) and Dockerfile | Initial draft had a real bug: it ran bare `pytest -v` in CI while `requirements.txt` didn't even include `pytest`/`httpx`. I'd already documented the `ModuleNotFoundError` root cause in release-evidence.md but hadn't gone back and fixed the workflow file itself to match — caught and fixed in this pass. |
| Security findings (AI security audit) | One finding (CORS `allow_origins="*"`) was flatly wrong — the code uses a specific whitelist, not a wildcard. Caught by re-reading `app/main.py` directly instead of trusting the finding. |
| Frontend Kanban board logic (`frontend/index.html`) | Accepted; understand the fetch calls and state handling. |
| Refactoring / documentation suggestions | Mixed — some accepted (docstrings), some rejected (e.g. an AI suggestion to add JWT auth middleware, out of scope). |

## Line-by-line trace

Block traced: `app/business_rules.py::validate_status_transition`.

- `if (current, new) not in VALID_TRANSITIONS:` — membership check against
  a frozenset of allowed `(from, to)` pairs; this is the entire rule.
- `allowed = sorted({...})` — rebuilds a human-readable list of allowed
  transitions purely for the error message; removing it wouldn't break
  the validation, only make the 422 detail less useful.
- `raise HTTPException(status_code=422, detail=...)` — FastAPI catches
  this and turns it into a JSON 422 response automatically; if this
  line were removed, an invalid transition would silently succeed.

I could explain every line here without hesitation. The one thing I
could *not* explain before this review was why the file had every one
of those lines duplicated — that turned out to be a copy-paste error,
not a deliberate pattern, and I removed the duplicate block.

## Pattern changes — what I'll keep doing, what I'll stop

- **Keep:** running the actual test suite before treating any AI
  change as done, not just eyeballing the diff.
- **Stop:** accepting a documented "root cause found" (like the pytest
  import-path bug) as equivalent to "fixed everywhere it applies." The
  finding and the fix live in different files (a doc and a workflow
  YAML) and I let them drift out of sync.
- **Start:** re-reading generated files for exact duplication, not just
  correctness — `business_rules.py` ran correctly with the whole file
  doubled, which is exactly the kind of "looks fine, isn't" the course
  keeps warning about.

Concrete rules from this retrospective are written up in
`docs/ai-usage.md`.
