# Personal AI Playbook

## When I reach for AI first

Tasks where AI consistently made me faster during this course:

- **CI and Docker boilerplate**: Claude Code drafted a clean multi-stage
  Dockerfile and ci.yml in one pass. These are pattern-heavy files where
  the real work is inspection and safety-checking the output, not
  generating it from scratch.
- **Docstring drafts**: endpoint docstrings for `app/main.py` were
  generated and then verified against the live `/docs` page — a much
  faster loop than writing them cold.
- **Test edge cases**: AI suggested the empty-body PATCH test and the
  same-status transition test, both of which ended up in `tests/test_tasks.py`
  and caught real behavior I hadn't explicitly specified.
- **Planning documents**: the grounded Codex plan for the comments
  feature (Part 5.4) was genuinely more useful than I expected, because
  I required it to read `app/models.py` and `app/storage.py` first — it
  extended the existing dict pattern rather than inventing a database.

## When I do not reach for AI first

- **Core business rules**: I wrote the status-transition logic in
  `app/business_rules.py` by hand first, then used AI to generate tests
  for it — not the other way around. If AI defines the rule and AI
  writes the tests, neither is verifying anything.
- **Security findings I'm about to act on**: the AI audit claimed
  `allow_origins="*"` (a wildcard). I opened `app/main.py` and found
  a specific localhost whitelist. Acting on that finding without
  checking the file would have been a wasted change or a confusing PR
  comment. Manual check first.
- **Anything involving `.env` or real credentials**: non-negotiable,
  no exceptions.

## My non-negotiables

1. Never paste `.env` values, credentials, API keys, tokens, or real
   customer/personal data into any AI tool — only `.env.example`
   placeholder values are shareable.
2. Every AI-generated code change must pass `python -m pytest -v`
   before being committed. "The diff looks correct" is not the same as
   "the tests pass."
3. No AI tool modifies `app/business_rules.py` without me reading
   the diff line by line first — that file is the single source of
   truth for what the API enforces.

## My review rules

- Run `git diff` before accepting any generated change; read every
  changed file, not just the file the prompt mentioned.
- For security findings: label each one Valid / False Positive / Noise
  with a one-sentence reason before deciding whether to act — the CORS
  finding in this project is the concrete reason that rule exists.
- For code review comments: label each one Useful / Noise / Wrong.
  "Wrong" gets its own bucket because it wastes more than a glance —
  it can cause me to "fix" a bug that doesn't exist.
- Check generated files for exact duplication, not just correctness.
  `app/business_rules.py` ran fine with its entire contents doubled;
  nothing in "the tests pass" would have caught that.

## What I am still figuring out

- How to set per-project rules for when a terminal agent (Claude Code)
  is the right tool versus the in-editor chat (Cursor) — my current
  heuristic is "repo-level tasks go to the terminal agent, file-level
  edits go to the IDE," but it breaks down for tasks that are
  technically one file but have broad logic implications.
- At what point a governance worksheet becomes worth the overhead on a
  solo project versus a team project — I kept it here because the
  course required it, but I haven't settled on what the lightweight
  version looks like for future personal work.

## Decision Card

| Decision | My answer |
|---|---|
| **New feature** | Design the model and storage changes by hand first; then use Claude Code (terminal agent) in plan mode to draft routes and tests — inspect the plan before any file is touched |
| **Code review** | Codex App (desktop) for a read-only first-pass diff review; I grade every comment Useful/Noise/Wrong before acting on any of them |
| **Debugging** | Paste the *exact* failing test name and error output, not a paraphrase — the pytest `ModuleNotFoundError` in this project was generic enough that vague prompts produced generic advice |
| **Infrastructure (CI / Docker)** | Claude Code or Codex for the first draft; I read the generated YAML/Dockerfile end-to-end before committing, specifically checking for `continue-on-error`, `|| true`, `latest` tags, and root-user issues |
| **Never paste** | `.env` values, API keys, auth tokens, real customer names, personal email addresses, production logs, or any database connection string with credentials in it |
| **My one rule** | Before committing any AI-generated file, I will name the specific verification I ran — not just "I checked it," but "I ran `python -m pytest -v` and all 20 tests passed" or "I ran `curl /health` and got 200" |

## 30-day re-read commitment

Calendar reminder set for **30 days after submitting this project**:
re-read `docs/ai-playbook.md` and ask one honest question: *am I still
following it?*

Specifically, check whether:
- The never-paste rule was kept (no `.env` values, no credentials).
- The "name the specific verification" rule was applied to at least one
  AI-assisted commit message or PR description.
- The Decision Card tool choices still match how I am actually working,
  or whether new habits replaced them.

If the answer is no, update the playbook with what changed and why.
