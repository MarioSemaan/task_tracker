# ADR-001: Task Tracker Backend Architecture

**Status:** Accepted
**Date:** 2026-07-25

## Context

The Task Tracker is a learning project with a Python/FastAPI backend and a separate lightweight web frontend, supporting CRUD operations on tasks (title, description, status, priority, assignee), status filtering, and enforced forward-only status transitions (ToDo → InProgress → Done). Transitions must proceed through each stage in order; skipping directly from ToDo to Done is not permitted.

Project constraints:

- Learning project, not production software
- Backend must use Python with FastAPI and Pydantic for validation
- REST API backend with a separate web frontend
- Simple, well-documented tech stack
- No authentication or multi-tenancy
- Must run locally with one or two commands
- No microservices, Docker, or cloud deployment

Two architectures were evaluated:

- **Option A:** FastAPI + SQLModel + SQLite (persistent storage)
- **Option B:** FastAPI + Pydantic + an in-memory dict-based store (no database)

## Decision

Option B — FastAPI with Pydantic models and an in-memory store — is the chosen architecture.

## Reasoning

Option B is more aligned with the project's stated constraints than Option A:

- **Simplicity first:** the constraints explicitly call for a simple, well-documented stack. Option B removes the ORM/session layer entirely — there's no engine, no session lifecycle, and no SQL to reason about.
- **Learning project scope:** with no requirement for data to survive restarts, an in-memory store meets the actual need without adding persistence machinery the project doesn't call for.
- **Easy to run locally:** both options run in two commands, but Option B has no database file to create, reset, or accidentally commit — one less moving part to explain in the README.
- **Testability:** pytest + TestClient tests reset state with a single `store.clear()`-style fixture, with no database setup/teardown to get right — a good fit for a project meant to be easy to test.

## Consequences

- **Positive:** Minimal setup, fastest path to a working app, simplest possible test fixtures, nothing to install beyond FastAPI/Pydantic/Uvicorn.
- **Negative:** All task data is lost on every server restart — acceptable for this learning project's current scope, but a real limitation if the project evolves into something used across sessions or by multiple people.
- **Negative:** Filtering, ID generation, and status-transition validation are hand-rolled rather than provided by an ORM — more code to maintain if the data model grows significantly.
- **Follow-up:** If persistence is ever needed later, the storage layer (`store.py`) would need to be rewritten against a database — this decision does not preclude that, but it is not free to switch.

## Amendment (mid-course project)

Initial ADR-001 stated that ToDo → Done (skipping InProgress) would be allowed. The implemented and tested business rule instead requires strictly sequential transitions: ToDo → InProgress → Done. This document is updated to match the actual, tested behavior rather than the original assumption.
