# Project Starter Kit

This repository is a reusable planning template for starting software projects fast without letting scope creep turn an MVP into a full product roadmap.

Ship first. Improve second.

## Purpose

Use this template to define a small MVP, freeze scope, plan the first sprint, and start building with clear guardrails.

This is not an application scaffold. It intentionally contains no app code.

## Philosophy

- Small MVPs ship.
- Good ideas are not automatically MVP requirements.
- Simpler systems win early.
- Backlog capture should be continuous.
- MVP scope should stay frozen during implementation.

Ship first. Improve second.

## Repository Map

- [`docs/MVP.md`](docs/MVP.md): the contract for what the MVP includes
- [`docs/Future.md`](docs/Future.md): ideas that should not expand the MVP
- [`docs/Decisions.md`](docs/Decisions.md): engineering decisions and tradeoffs
- [`docs/Sprint-01.md`](docs/Sprint-01.md): the active implementation document
- [`docs/Sprint-Template.md`](docs/Sprint-Template.md): reusable sprint format
- [`docs/Release-Checklist.md`](docs/Release-Checklist.md): pre-ship checklist
- [`templates/Feature-Proposal.md`](templates/Feature-Proposal.md): evaluate new feature requests
- [`templates/Decision-Record.md`](templates/Decision-Record.md): reusable decision record
- [`AGENTS.md`](AGENTS.md): permanent instructions for AI coding agents

## Workflow

1. Fill out [`docs/MVP.md`](docs/MVP.md).
2. Put every extra idea in [`docs/Future.md`](docs/Future.md).
3. Record key tradeoffs in [`docs/Decisions.md`](docs/Decisions.md).
4. Plan implementation in [`docs/Sprint-01.md`](docs/Sprint-01.md).
5. Build only what the sprint and MVP allow.
6. Use [`docs/Release-Checklist.md`](docs/Release-Checklist.md) before shipping.
7. Collect feedback, then decide what belongs in the next sprint.

## Lifecycle

```text
Idea
  ↓
Brainstorm
  ↓
Freeze MVP
  ↓
Sprint Planning
  ↓
Build
  ↓
Ship
  ↓
Collect Feedback
  ↓
Next Sprint
```

Ship first. Improve second.

## How To Start A New Project

1. Clone this repository into a new project folder.
2. Rename the project in [`docs/MVP.md`](docs/MVP.md).
3. Define the problem, target user, success metric, and ship date.
4. Limit the MVP to five allowed features or fewer.
5. Move every non-essential idea into [`docs/Future.md`](docs/Future.md).
6. Write the first implementation sprint in [`docs/Sprint-01.md`](docs/Sprint-01.md).
7. Start building with [`AGENTS.md`](AGENTS.md) and the sprint as guardrails.

## Quick Rules

- If it is not in [`docs/MVP.md`](docs/MVP.md), it is not in scope.
- If it is a good idea but not required now, put it in [`docs/Future.md`](docs/Future.md).
- If implementation work is not in the active sprint, do not do it yet.
- If a shortcut helps the MVP ship, prefer the shortcut.
