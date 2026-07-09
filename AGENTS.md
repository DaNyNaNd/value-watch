# AGENTS.md

Permanent instructions for AI coding agents working in repositories created from this template.

## MVP Contract

[`docs/MVP.md`](docs/MVP.md) is the source of truth.

Do not add features that are not explicitly listed there.

## Scope Guard

Whenever asked to implement a new feature:

1. Check whether it exists in [`docs/MVP.md`](docs/MVP.md).
2. If yes, continue.
3. If no, do not implement it.
4. Explain that the request expands scope and recommend adding it to [`docs/Future.md`](docs/Future.md).

## Architecture Rules

Prefer:

- duplication over abstraction
- SQLite over distributed databases
- synchronous execution over queues
- hardcoded values over configuration
- one service over microservices
- local files over cloud infrastructure
- one developer optimization over team optimization

Unless the MVP explicitly requires otherwise.

## Simplicity Rule

Every architectural decision should optimize for this question:

> What is the smallest implementation that can survive until Version 1?

Never optimize for hypothetical future scale.

## Sprint Discipline

Only implement tasks found in the active sprint document, such as [`docs/Sprint-01.md`](docs/Sprint-01.md).

Ignore [`docs/Future.md`](docs/Future.md) during implementation.

## Technical Debt

Intentional technical debt is acceptable.

Document it.

Do not prematurely fix it.
