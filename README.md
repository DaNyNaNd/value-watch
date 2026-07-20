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

## Run locally

Requires Python 3.11+. No packages need to be installed. Configure local credentials:

```sh
cp .env.example .env
```

Set `SCHWAB_API_CLIENT_ID`, `SCHWAB_API_CLIENT_SECRET`, and
`SCHWAB_API_CALLBACK_URL=https://127.0.0.1` in `.env`. Schwab's client ID is
its “App Key.” `SCHWAB_API_APP_MACHINE_NAME` is not needed by this project.

Authorize once (and again if Schwab expires the refresh token):

```sh
./bin/value-watch login
```

After approving the request, the browser may not load `https://127.0.0.1`.
Copy its complete address-bar URL and paste it into the prompt. The callback URL
in `.env` must match the Schwab app setting exactly.

Generate a live, read-only report:

```sh
./bin/value-watch report
```

It writes `reports/weekly-YYYY-MM-DD.md`. SEC Company Facts are cached in
ignored `data/sec.sqlite3`; use `--refresh-sec` after a new filing. Schwab
tokens are stored locally in ignored `data/schwab-token.json`.

Run the credential-free fixture check:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
./bin/value-watch dry-run
```

### Weekly macOS schedule

Use cron for the smallest local scheduler. Edit with `crontab -e` and add this
line to run Monday at 8:00 a.m. (adjust the absolute path):

```cron
0 8 * * 1 cd /Users/danielhampton/Projects/personal/value-watch && /Users/danielhampton/Projects/personal/value-watch/bin/value-watch report >> /Users/danielhampton/Projects/personal/value-watch/data/cron.log 2>&1
```

First run `./bin/value-watch dry-run` to verify the command and report location.

## Safety boundary

This project deliberately excludes account data, trade execution, swing-trading signals, alerts, and personalized investment advice.
