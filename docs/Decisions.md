# Decisions

Engineering log. Append new decisions chronologically.

Use [`../templates/Decision-Record.md`](../templates/Decision-Record.md) when a decision needs more structure, then summarize the outcome here.

---

## Date

2026-07-20

## Decision

Build the first version as a local, read-only command that writes a Markdown report. Use Schwab for quote-time fields and SEC Company Facts for periodic business metrics; cache filing data locally.

## Alternatives Considered

Use only Schwab data, buy a commercial fundamentals API, build a dashboard first, or automate a DCF before validating the data pipeline.

## Reason

Quotes are the only facts that need a weekly refresh. Financial-statement facts are authoritative but normally change only at filing time. This division minimizes API dependence and avoids presenting a volatile price move as a changing business thesis.

## Tradeoffs

SEC XBRL facts can need issuer-specific normalization and will sometimes be unavailable. The first score will therefore be intentionally incomplete, showing missing data rather than manufacturing precision.

## Impact

The MVP needs a credentialed Schwab adapter, an SEC adapter and SQLite cache, but no broker account endpoints, cloud services, or web UI.
