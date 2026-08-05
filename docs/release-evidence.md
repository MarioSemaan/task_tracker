# Release Evidence

## Baseline
- **Branch**: final-project
- **Date**: August 4, 2026
- **Local app run command**: `uvicorn app.main:app --reload --port 8000`
- **`/health` result**: `HTTP/1.1 200 OK` → `{"status":"ok","timestamp":"2026-08-04T18:23:11.042531+00:00"}`
- **Frontend check**: Opened `frontend/index.html` in browser; Kanban board renders with three columns (ToDo, InProgress, Done) and the create/edit modal opens correctly.
- **Test command**: `python -m pytest -v`
- **Test result**: `20 passed in 0.06s` (full output in docs/midcourse/baseline-test-results.txt)

## CI evidence
- **Workflow file**: `.github/workflows/ci.yml`
- **Latest run**: GitHub Actions ran the full suite on push to `final-project`. The workflow installed dependencies from `requirements.txt` (which includes `pytest` and `httpx`) and ran `python -m pytest -v`. All 20 tests passed. Run is visible at: `https://github.com/MarioSemaan/task_tracker/actions/runs/31004708404` under the most recent push to `final-project`.
- **Test command used by CI**: `python -m pytest -v` — changed from an earlier draft that used bare `pytest -v`, which fails with `ModuleNotFoundError: No module named 'app'` because the console-script form of pytest does not add the project root to `sys.path`. `python -m pytest` does. The workflow file was updated to match after this was caught during the claim-vs-reality check below.
- **Shortcut check**: Verified no `continue-on-error`, no `|| true`, no `--exit-zero`, pytest is not skipped, and the Python version is pinned to `3.11` (not `latest`).

## Docker evidence
- **Build command**: `docker build -t task-tracker:dev .`
- **Run command**: `docker run -d -p 8000:8000 --name tt-dev task-tracker:dev`
- **`/health` check**: `curl -i http://localhost:8000/health` returned `HTTP/1.1 200 OK` with body `{"status":"ok","timestamp":"..."}`.
- **Non-root check**: `docker exec tt-dev whoami` returned `app` — not `root`.
- **No-baked-secrets check**: `.dockerignore` excludes `.env`, `.env.example`, `.git`, `venv/`, `.venv/`, `docs/`, `tests/`, and `__pycache__/`. The Dockerfile `COPY`s only `app/` and `frontend/` explicitly in the runtime stage, so nothing else from the build context can appear in the shipped image even if `.dockerignore` is later loosened.
- **Multi-stage build**: Confirmed — a `builder` stage installs all Python dependencies into `/opt/venv`; the `runtime` stage copies only the built venv and application code, with no compilers or build tools present.
- **Image size**: Approximately 180MB (multi-stage + slim base).

### Docker security log
| Check | Result |
|---|---|
| Non-root user | `docker exec tt-dev whoami` → `app` |
| Slim runtime base | Runtime stage: `FROM python:3.11-slim AS runtime` |
| No baked secrets | `.dockerignore` excludes `.env`, `.git`, `venv/`; Dockerfile copies only `app/` and `frontend/` |

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `pytest -v` works as standalone command in CI | Ran `pytest -v` vs `python -m pytest` locally | Raw `pytest` failed with `ModuleNotFoundError: No module named 'app'` | Updated `.github/workflows/ci.yml` to use `python -m pytest -v`; added `pytest` and `httpx` to `requirements.txt` since they were missing and CI would otherwise fail before even running tests |
| `/health` returns `{"status":"ok"}` | `curl http://localhost:8000/health` against live server | Returned correct JSON with `status` and `timestamp` fields | Claim verified; no change needed |
| Docker container runs as non-root | `docker exec tt-dev whoami` | Returned `app` | Verified; `USER app` directive in Dockerfile confirmed |
| README described the current API accurately | Compared README intro paragraph to `app/main.py` routes | An early README draft said "no task CRUD endpoints included yet" — true in Module 1, false now that full CRUD, filtering, and status transitions exist | Rewrote the README intro to describe the current API |
