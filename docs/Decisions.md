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

---

## Date

2026-07-20

## Decision

Use the registered `https://127.0.0.1` callback with a manual paste-back OAuth authorization-code flow.

## Alternatives Considered

Run a local HTTPS callback server, require a public redirect URL, or automate browser sign-in.

## Reason

The app is personal and local-only. Schwab redirects to the registered callback after consent; copying that final URL supplies the authorization code without a public host or storing brokerage login credentials.

## Tradeoffs

The initial authorization is interactive and refresh-token expiry requires repeating it. The token remains in the ignored local `data/` directory with owner-only file permissions.

## Impact

`SCHWAB_API_CLIENT_ID`, `SCHWAB_API_CLIENT_SECRET`, and `SCHWAB_API_CALLBACK_URL` are required. `SCHWAB_API_APP_MACHINE_NAME` is intentionally unused.

---

## Date

2026-07-20

## Decision

Use the standard-library HTTP client and record Schwab fields as `P/E` and `marketCap` from the quote response's `fundamental` object, with explicit `N/A` reporting when absent.

## Alternatives Considered

Use a third-party broker SDK or infer missing market capitalization from price and shares outstanding.

## Reason

The standard library keeps the local command installable without package dependencies. A missing field must remain visible rather than be inferred or substituted with zero.

## Tradeoffs

The first live run may expose symbol-specific data shape differences. These create `Insufficient data` results until validated, rather than an incorrect score.

## Impact

The `report` command requests only Schwab's market-data quote/fundamental fields and never calls account or order endpoints.
