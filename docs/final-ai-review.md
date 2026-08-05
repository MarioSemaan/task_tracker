# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| "Replace in-memory dictionary storage with SQLite database" | Wrong | Project rules explicitly prohibit adding external databases or major architecture shifts. | Rejected proposal. |
| "Add docstrings to API endpoints in `app/main.py`" | Useful | Improves maintainability for future developers without changing runtime logic. | Applied docstring documentation. |
| "Reformat code using custom line length of 70 characters" | Noise | Unnecessary stylistic change that adds zero structural value. | Ignored. |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Missing endpoint authentication | `app/main.py` | Valid | Endpoint authentication is intentionally omitted due to course scope, but represents a production risk. | Documented in `AGENTS.md` and security review. |
| CORS `allow_origins` includes `"null"` | `app/main.py` (CORSMiddleware config) | Valid | Corrected from an earlier draft finding that mistakenly said `allow_origins="*"` — checking the code shows a specific localhost whitelist, not a wildcard. The real issue is that `"null"` is included, which some browsers send for `file://` pages and sandboxed iframes; it's a reasonable local-dev convenience but should be dropped before any production deployment. | Documented here and in AGENTS.md do-not-ship-as-is note; no code change made since this is a course/local-dev project. |
| Potential unhandled exceptions returning stack traces | `app/main.py` | Noise | FastAPI handles basic Pydantic validation errors cleanly without exposing system internals. | No action required. |

## Manual security check
I manually inspected `app/models.py` and `app/storage.py` to confirm that user inputs for task titles and descriptions are properly validated by Pydantic models, preventing basic type-injection attacks.

## One AI output I rejected or corrected
An AI tool suggested adding JWT authentication middleware to secure the routes in `app/main.py`. I rejected this because the project guidelines explicitly forbid implementing authentication or altering existing application feature scope.

## Three AI usage rules
1. **Never paste**: Credentials, API tokens, `.env` variables, or real customer data into AI tools.
2. **Always verify**: AI-generated suggestions by running `python -m pytest` and manually inspecting the diff before committing.
3. **Record AI contributions by**: Logging review findings and document edits in project tracking docs.

## Ownership statement
I am confident submitting this repository as my own work because I have personally executed all test suites, verified API endpoint responses, and written the release documentation. Every line of code and configuration file added has been audited line-by-line to ensure full alignment with course guidelines. I understand how the backend routes, storage mechanisms, and CI processes operate within this codebase.