# Status Transition Rules

## Context

Tasks move through a small set of statuses (ToDo, InProgress, Done).
Early in the project (see the original ADR-001) I assumed a task could
jump straight from ToDo to Done — a simple "mark complete" shortcut.
Once I started writing tests for PATCH /tasks/{id}, that assumption
didn't hold up: a task marked Done without ever passing through
InProgress makes it impossible to tell, later, whether work was
actually started and tracked, or just rubber-stamped. I decided the
API itself should enforce the intended workflow instead of trusting
every client to do it correctly.

## Decision

`app/business_rules.py` enforces a fixed set of legal transitions:

- `ToDo -> InProgress`
- `InProgress -> Done`
- `Done -> InProgress` (reopening a task is allowed)

Anything outside this set — including skipping a stage (`ToDo -> Done`),
moving backward to ToDo, or "transitioning" to the same status a task
is already in — is rejected with `422` and a message listing the
allowed transitions.

## Alternatives considered

1. **No validation, client decides.** The frontend enforces order, the
   API accepts any status value. Rejected: any other client (a script,
   a future teammate's tool, a curl command) could bypass the frontend
   and write garbage state directly.
2. **Allow any transition, log a warning.** Rejected: a warning nobody
   reads is not a rule. If the transition is invalid, the caller should
   find out immediately, not discover it later when the data looks odd.
3. **Full workflow engine / state machine library.** Rejected as
   overkill for three states and four legal edges — a `frozenset` of
   `(from, to)` tuples in one function is easier to read, test, and
   change than pulling in a dependency for this.

## Trade-offs

Enforcing this server-side makes the API stricter and slightly less
forgiving — a client that naively PATCHes straight to `Done` gets a
422 instead of a silently "helpful" auto-correction. That's a
deliberate trade: predictability over convenience. It also means the
frontend has to handle and display 422s instead of assuming every
status write succeeds, which added a small amount of UI work.

The one asymmetry worth calling out: `Done -> InProgress` is allowed
(reopening), but `Done -> ToDo` and `InProgress -> ToDo` are not. That
was a judgment call — "reopen" is a normal real-world action; "un-start"
back to the very beginning felt like it should require deleting and
recreating the task rather than being a status flip.

## Consequences

- Any new status value added later needs an explicit entry in
  `VALID_TRANSITIONS`, or it will be unreachable by design — that's
  intentional friction, not an oversight.
- The 422 error message lists all allowed transitions, which doubles as
  informal API documentation for anyone testing the endpoint manually.
- Tests (`tests/test_tasks.py`) cover the ToDo->InProgress happy path,
  the ToDo->Done skip rejection, and the same-status rejection — they
  do **not** currently cover `Done -> InProgress` or `Done -> ToDo`
  explicitly, which is a gap worth closing (see Open Questions).

## Open questions

- Should `Done -> ToDo` be allowed for the "actually, this needs to be
  redone from scratch" case, instead of forcing a delete + recreate?
  I don't have a strong answer yet — leaning no, but haven't tested
  this against how the frontend actually gets used.
- The current tests don't exercise `Done -> InProgress`. I'd add that
  before trusting this rule set in anything beyond a course project.
- If this ever needs more than three statuses (e.g. "Blocked"), the
  `frozenset` approach still works, but the do-not-skip guarantee gets
  harder to reason about by inspection alone — that might be the point
  where a small state-machine helper becomes worth the dependency.

I would do this differently by writing the `Done -> InProgress` and
`Done -> ToDo` test cases *before* deciding the reopen rule, instead of
after — I made the call based on intuition, not evidence from tests.
