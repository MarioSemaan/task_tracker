# Personal AI Playbook

## When I reach for AI first
- **CI/Docker boilerplate**: Claude Code drafted a working multi-stage Dockerfile and `ci.yml` in one pass — pattern-heavy files where the real work is inspecting the output, not writing it from scratch.
- **Docstring drafts**: generated, then checked against the live `/docs` page — faster than writing cold.
- **Test edge cases**: AI suggested the empty-body PATCH test and the same-status transition test, both now in `tests/test_tasks.py`.
- **Repo-grounded planning**: the Codex plan for the comments feature (Part 5.4) was genuinely useful once I required it to read `app/models.py` and `app/storage.py` first — it extended the existing dict pattern instead of inventing a database.

## When I do not reach for AI first
- **Core business rules**: I wrote `app/business_rules.py` by hand, then used AI to generate tests for it — not the reverse. If AI writes both the rule and the test, neither is verifying anything.
- **Security findings I'm about to act on**: the AI audit first claimed `allow_origins="*"`. Opening `app/main.py` showed a specific localhost whitelist instead. Manual check first, always.
- **Anything involving `.env` or real credentials**: no exceptions.

## My non-negotiables
1. Never paste `.env` values, credentials, tokens, or real customer/personal data into any AI tool.
2. Every AI-generated change must pass `python -m pytest -v` before being committed — a clean-looking diff is not the same as passing tests.
3. No AI tool touches `app/business_rules.py` without me reading the diff line by line first — it's the single source of truth for what the API enforces.

## My review rules
- Run `git diff` before accepting any change; read every changed file, not just the one the prompt mentioned.
- Grade security findings Valid / False Positive / Noise, and review comments Useful / Noise / Wrong, before acting on any of them.
- Check generated files for exact duplication, not just correctness — `app/business_rules.py` ran fine with its entire contents copy-pasted twice; nothing about "the tests pass" caught that.

## What I am still figuring out
- When a task is "one file but broad logic" — my current heuristic (repo-level → terminal agent, file-level → IDE chat) breaks down here.
- How much governance overhead is worth keeping on a solo project versus a team one once the course requirement isn't forcing it.

## Decision Card
| Decision | My answer |
|---|---|
| **New feature** | Design the model/storage changes by hand first; then Claude Code in plan mode drafts routes and tests — I inspect the plan before any file is touched |
| **Code review** | Codex App for a read-only first-pass diff; I grade every comment Useful/Noise/Wrong before acting |
| **Debugging** | Paste the *exact* failing test name and error output, not a paraphrase — vague prompts produced generic advice on this project |
| **Infrastructure (CI/Docker)** | AI drafts it; I read the YAML/Dockerfile end-to-end checking for `continue-on-error`, `\|\| true`, `latest` tags, and root-user issues before committing |
| **Never paste** | `.env` values, API keys, auth tokens, real customer names/emails, production logs, or any connection string with credentials |
| **My one rule** | Before committing any AI-generated file, name the specific verification I ran — "ran `python -m pytest -v`, 20/20 passed," not "I checked it" |

## 30-day re-read commitment
Reminder set for 30 days after submission: re-read this file and ask honestly — am I still following it? Specifically: was the never-paste rule kept, was "name the specific verification" applied to at least one real commit, and does the Decision Card still match how I'm actually working. If not, update it.