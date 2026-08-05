# Security Review

Read-only AI audit of this repo, graded and reconciled with a manual
scan. No code was changed as part of this review (see AGENTS.md
guardrails — code fixes require explicit approval and are logged
separately in docs/final-ai-review.md if applied).

## AI findings

| Finding | File evidence | Grade | Reason |
|---|---|---|---|
| No authentication or ownership checks on task endpoints | `app/main.py` — all routes are unauthenticated | Valid | Intentional scope decision for a learning project (see CLAUDE.md do-not rules), but it's a real production risk if this code were ever deployed as-is. Documented, not fixed. |
| `title`/`description` have no enforced maximum beyond the 200-char title check | `app/models.py` — `description: Optional[str] = ""` has no length validator | Valid | `title` is capped at 200 chars, but `description` has no cap at all. A client could POST an arbitrarily large description and grow the in-memory store unbounded. Worth a length validator. |
| CORS `allow_origins` includes `"null"` | `app/main.py` CORSMiddleware config | Valid | See docs/final-ai-review.md — corrected from an earlier draft that mistakenly claimed a `*` wildcard. The real, narrower finding is the `"null"` origin, which is a reasonable local-dev convenience but shouldn't ship to production. |
| SQL injection risk in storage layer | (AI-suggested, no file cited) | False Positive | There is no SQL anywhere in this project — `app/storage.py` is a plain Python dict. This finding doesn't apply to this codebase. |
| "Validate all user input" | (AI-suggested, generic) | Noise | Technically true of every API ever built. Not actionable without naming a specific field, endpoint, or failure mode. |
| Error responses may leak stack traces | `app/main.py` — relies on FastAPI's default exception handling | Noise | Checked against a live 422 and 404 response; both return clean JSON (`{"detail": "..."}"`) with no traceback or internal path. FastAPI's default handlers already prevent this for the error paths this app actually triggers. |

## My manual findings

- **No length limit on `description`** (same as above — I found this
  independently while reading `app/models.py` before running the AI
  audit, then saw the AI surfaced it too; counted in "Agreement" below).
- **`assignee` field accepts any string, including empty string vs
  `None`.** Not a security issue exactly, but there's no validation
  distinguishing "no assignee" from "assignee is an empty string" —
  a data-quality gap rather than a security one, so not added to the
  backlog below, just noted.
- Checked `.dockerignore` and `Dockerfile` by hand: confirmed `.env`,
  `.git`, and `venv/` are excluded from the build context, and the
  runtime image only ever `COPY`s `app/` and `frontend/` explicitly —
  so even a loosened `.dockerignore` couldn't leak `tests/` or `docs/`
  into the shipped image.

## Reconciliation

| Agreement (AI + manual both found) | AI-only | You-only |
|---|---|---|
| No `description` length limit | CORS `"null"` origin note; no-auth-by-design finding | `.dockerignore`/Dockerfile copy-scope check (I verified this myself rather than trusting the AI's read of the Dockerfile) |

The "You-only" column is thin this round, which is itself worth noting
honestly rather than padding it: most of what I checked by hand landed
on the same two or three things the AI also caught. The place my own
judgment mattered most was rejecting the AI's incorrect `*`-wildcard
CORS claim and the SQL-injection false positive — both required
actually opening `app/main.py` and `app/storage.py` rather than trusting
a fluent-sounding finding.

## Top-3 backlog

1. **Add a max length validator to `description`** in `app/models.py`
   (e.g. cap at 2000 chars, mirroring the `title` pattern) — prevents
   unbounded in-memory growth from a single field. Owner: whoever picks
   up the next models.py change. Not applied in this review per the
   read-only/docs-first guardrail.
2. **Document the no-auth decision explicitly as a known limitation**
   in the README's Architecture section, so a future maintainer doesn't
   assume auth was simply forgotten. (Done — see README "Architecture"
   section and CLAUDE.md do-not rules.)
3. **Remove `"null"` from `allow_origins` before any real deployment**,
   or gate it behind an environment flag so local dev keeps working
   without shipping it to production CORS config.
