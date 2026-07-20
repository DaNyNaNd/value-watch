# MVP

> Changing this document means changing the MVP.
> Most new ideas belong in [`Future.md`](Future.md) instead.

This document is a contract. Once approved, it should rarely change.

Review [`Future.md`](Future.md) before editing this file to make sure new ideas belong here and not there.

## Project Name

Value Watch

## Problem Statement

Following a possible investment manually makes it too easy to react to a price move without checking whether the underlying business is still high quality and reasonably valued. The first version turns a small, personally curated watchlist into one short weekly review report.

## Target User

One self-directed individual investor using a Schwab Individual Trader API account. It is a research aid, not an adviser or trading system.

## Success Metric

Each week, it generates a readable report for a 5–20-company watchlist in under two minutes, with no spreadsheet work, and identifies the symbols that warrant a human review.

## Ship Date

2026-08-07

## Non-negotiable Constraints

- Personal, local-first tool; no public hosting or multi-user features.
- Read-only market-data access. It must never submit, preview, or modify an order.
- Schwab credentials and refresh tokens stay in local environment variables or the OS keychain; never in source control or reports.
- Use the Schwab Trader API for current quote fields and SEC Company Facts for filing-derived financials.
- A score is a triage signal, not a buy/sell recommendation or a valuation guarantee.

## Allowed Features

<!-- Maximum five. If a feature is not listed here, it is not part of the MVP. -->

1. Read a local watchlist of 5–20 common-stock tickers and a one-sentence business description supplied by the user.
2. Retrieve and cache current quote/fundamental fields from Schwab and annual filing facts from the SEC for each ticker.
3. Calculate a transparent two-part screen: value (P/E and free-cash-flow yield) and realization/quality (five-year revenue and EPS trends, positive free cash flow, return on equity when available, and debt sanity check).
4. Create a Markdown weekly report ranked by score, including raw inputs, missing-data warnings, score rationale, and a “review, watch, or insufficient data” label.
5. Run the report once on demand and once each week through a documented local scheduler command.

## Forbidden Features

<!-- Explicitly list tempting ideas that are intentionally excluded. -->

- Order entry, portfolio/account access, tax lots, alerts that encourage immediate action, or automatic trades.
- Investment advice, price targets, personalized recommendations, and claims that a company is a “buy.”
- A web dashboard, mobile app, accounts, cloud deployment, or email/SMS delivery.
- AI summaries of filings, sentiment/news signals, options data, insider-trading signals, or analyst estimates.
- A full DCF model. Its assumptions deserve a deliberate later design rather than hidden automation.

## Out of Scope

<!-- Add anything likely to cause confusion during implementation. -->

- The user, not the tool, chooses and understands the businesses on the watchlist.
- The initial universe is U.S. operating companies with comparable SEC financial statements; financial institutions, REITs, funds, ETFs, and ADRs are excluded.
- SEC financial statements are periodic. A weekly report can change price-based metrics while business metrics normally change only after a filing.
- The report should never compare companies across materially different business models as if one score establishes a winner.

## Future Vision

After the report is trusted, it could add a manually reviewable DCF, historical valuation bands, an investment-memo workflow, filing/risk summaries, notifications, and a lightweight dashboard—while retaining the rule that data and assumptions are visible before a decision is made.
