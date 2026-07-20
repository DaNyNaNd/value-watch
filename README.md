# Value Watch

A local, read-only weekly research report for a small value-investing watchlist.

Value Watch uses Schwab quote data for current valuation and SEC filings for periodic business fundamentals. It is a decision-support tool only: it never accesses accounts, submits orders, or makes buy/sell recommendations.

## MVP

The frozen MVP and its guardrails live in [docs/MVP.md](docs/MVP.md). The current screen, definitions, labels, and human-review prompts are in [docs/Scorecard.md](docs/Scorecard.md).

The active work is constrained to [Sprint 01](docs/Sprint-01.md). Deferred ideas—such as a DCF, dashboard, and notifications—are in [docs/Future.md](docs/Future.md).

## Planned workflow

1. Maintain a 5–20-company watchlist with a one-sentence business description.
2. Run the report once a week, or on demand.
3. Use a `Review` label as a prompt for human research—not as an investment conclusion.
4. Do a deeper thesis review when a company files quarterly or annual results.

## Safety boundary

This project deliberately excludes account data, trade execution, swing-trading signals, alerts, and personalized investment advice.
