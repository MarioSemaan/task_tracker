# Tool-Fit Reflection

*Module 4 X1 deliverable: comparing Copilot, Cursor, Claude Code, and
Codex App by workflow scope rather than ranking them. The lesson from
Module 4 Part 2 is that there is no single best tool; the right tool
is determined by the scope of the task.*

---

## What the course taught me to compare

The module introduces three (later four) surfaces in ascending order of
scope:

| Surface | Scope | Cost of a careless approval |
|---|---|---|
| Copilot / autocomplete | Single line or function, inline while typing | Low — one misplaced line is visible and easy to revert |
| Cursor / IDE chat | One file at a time, diff visible in the editor | Medium — a file-level change that looks plausible can still be wrong |
| Claude Code / terminal agent | Whole repo — read, plan, edit multiple files, run commands | High — one approval can touch several files or run shell commands that change state |
| Codex App / desktop agent | Read-only review, planning, governance, context experiments | Low if used in plan-and-review posture; higher if diffs are approved reflexively |

---

## What I actually used each one for in this project

### Copilot / inline autocomplete
Best moment in this project: filling in repetitive Pydantic field
declarations in `app/models.py` and the repeated `assert` boilerplate
in `tests/test_tasks.py`. The suggestion stayed within one function
body, I could see it immediately, and accepting or rejecting it was a
single keystroke.

Not the right tool for: generating the `ci.yml` file or the Dockerfile.
Those cross multiple concepts and need to be read end-to-end before
being committed; autocomplete works one line at a time and has no way
to enforce the module's "no `continue-on-error`" constraint.

### Cursor / IDE chat
Best moment: reviewing a diff for the frontend Kanban board logic in
`frontend/index.html`. The sidebar chat could see the full file, answer
questions about a specific event handler, and propose a targeted change
I could inspect in the editor diff panel before applying.

Not the right tool for: running `python -m pytest -v` in a loop,
building the Docker image, or verifying that the CI workflow actually
exercises the test suite rather than silently skipping it. Those require
a terminal loop, not an editor view.

### Claude Code / terminal agent
Best moment: generating the initial `.github/workflows/ci.yml` and
`Dockerfile` in plan mode. The agent could read `requirements.txt`,
`app/main.py`, and `CLAUDE.md` in one turn, propose the multi-stage
Dockerfile design, and then wait for approval before writing any file.
That cross-file read-and-plan capability is exactly what makes it
worth the added verification overhead.

Risk I learned: the broader the scope the agent has, the more a
"looks right" response can cost you. The CI workflow the agent
generated initially used bare `pytest -v` in the workflow file while
`requirements.txt` didn't even list `pytest` — the workflow looked
professional but would have failed the first real run. The fix was
reading the YAML end-to-end, not just skimming the last step.

### Codex App / desktop agent (Module 5)
Best moment: the read-only security audit and the repo-grounded
comments-feature plan. Both tasks are fundamentally about reading real
files and producing a document — not about writing application code.
The desktop app's bounded-thread model and explicit diff review pane
made it easier to maintain the grading posture the module requires.

Risk to watch: a long, smooth thread accumulates context that is harder
to verify. The smoke tests (5.1C/D) exist specifically because a
convincing-sounding answer about "this FastAPI project" could describe
any FastAPI project. Checking two repo-specific facts before trusting
any substantive output is the habit, not the exception.

---

## The one rule that emerged

The scope of the task determines the tool, not the difficulty:

- **Inline, familiar, one function** → autocomplete (Copilot)
- **One file, needs explanation or diff** → IDE chat (Cursor)
- **Multi-file, needs commands or cross-repo planning** → terminal agent (Claude Code)
- **Read-only review, governance, or planning without implementation** → desktop agent (Codex App)

No tool is universally best. The risk isn't using the "wrong" tool;
the risk is using a broad-scope tool with a narrow-scope verification
habit — approving a repo-level agent edit the same way you would
accept a single autocomplete suggestion.
