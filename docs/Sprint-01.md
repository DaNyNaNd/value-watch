# Sprint 01

This is the only document implementation should follow.

Keep the sprint small enough to finish in 1-2 weeks.

Use [`Sprint-Template.md`](Sprint-Template.md) for future sprints.
Check [`MVP.md`](MVP.md) before adding tasks, and move non-essential ideas to [`Future.md`](Future.md).

## Sprint Goal

Run a local weekly report for a small personal watchlist that ranks transparent value and quality checks without accessing trading functions.

## Definition of Done

- MVP feature works as described
- Acceptance criteria are met
- Known shortcuts are documented
- Deferred ideas are moved out of implementation

## Task List

<!-- Keep this to roughly ten implementation tasks or fewer. -->

- [ ] Create the smallest executable project skeleton, test command, and local-only configuration example.
- [ ] Define the 5–20 ticker watchlist file, including the required one-sentence business description.
- [ ] Implement authenticated, read-only Schwab quote retrieval and validate the exact fields returned for the initial watchlist.
- [ ] Implement SEC Company Facts retrieval, ticker-to-CIK mapping, and a SQLite cache for filing-derived annual metrics.
- [ ] Calculate and display P/E, free-cash-flow yield, five-year revenue/EPS trends, free-cash-flow consistency, ROE when available, and a debt sanity check.
- [ ] Implement the published rules in `docs/Scorecard.md`, including data definitions and “insufficient data” behavior next to the generated output.
- [ ] Generate one Markdown report sorted into review, watch, and insufficient-data sections.
- [ ] Add an on-demand command plus a documented weekly local scheduler setup; test it with a dry run.
- [ ] Add fixture-based tests for calculations and a report snapshot test using no credentials.
- [ ] Record API and data-source shortcuts in `docs/Decisions.md` and deferred ideas in `docs/Future.md`.

## Acceptance Criteria

- With valid local Schwab credentials, one command produces a report for a 5–20-symbol watchlist without requesting account or order scopes.
- Each reported decision label identifies the metric(s) that caused it; missing or stale values are explicit rather than inferred as zero.
- The report contains no buy/sell wording, order controls, account balances, or personally identifying account data.
- Re-running with saved fixtures succeeds offline and gives stable calculation results.
- The implementation matches [`MVP.md`](MVP.md).

## Blocked Items

- None yet

## Deferred Ideas

<!-- Put tempting ideas here instead of expanding this sprint. -->

- Automated DCF and historical valuation bands
- AI filing summaries and qualitative moat/management assessment
- News, analyst, options, and insider-trading data
- Notifications, email, web dashboard, and cloud scheduling
- Portfolio tracking or broker-account functionality

## Retrospective

<!-- Fill this out after the sprint ends. -->

- What worked:
- What slowed things down:
- What to change next sprint:
