from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ROOT, Settings
from .report import render, write_report
from .schwab import SchwabClient
from .scoring import score
from .sec import SecCache, company_facts, financials, ticker_map
from .watchlist import read_watchlist


def _quote_fields(raw: dict) -> dict:
    # Schwab places P/E in fundamental and price fields in quote; normalize the fields this MVP uses.
    quote, fundamental = raw.get("quote", {}), raw.get("fundamental", {})
    price = quote.get("mark") or quote.get("lastPrice") or quote.get("closePrice")
    shares = fundamental.get("sharesOutstanding")
    return {"peRatio": fundamental.get("peRatio") or fundamental.get("peRatioTTM") or quote.get("peRatio"),
            "marketCap": fundamental.get("marketCap") or raw.get("marketCap") or
                         (price * shares if isinstance(price, (int, float)) and isinstance(shares, (int, float)) else None)}


def _to_schwab_symbol(symbol: str) -> str:
    return symbol.replace(".", "/")


def _from_schwab_symbol(symbol: str) -> str:
    return symbol.replace("/", ".")


def run(args: argparse.Namespace) -> Path:
    watchlist = read_watchlist(Path(args.watchlist))
    settings = Settings.from_env()
    client = SchwabClient(settings)
    # Schwab uses slashes for class shares (BRK/B), while the local watchlist uses conventional dots (BRK.B).
    raw_quotes = client.quotes([_to_schwab_symbol(item.symbol) for item in watchlist])
    quotes = {_from_schwab_symbol(symbol): value for symbol, value in raw_quotes.items() if symbol != "errors"}
    cache = SecCache(settings.data_dir / "sec.sqlite3")
    ciks = ticker_map()
    results = []
    for item in watchlist:
        cik = ciks.get(item.symbol.replace(".", "-"))
        facts = company_facts(item.symbol, cik, cache, refresh=args.refresh_sec) if cik else None
        values = financials(facts) if facts else {}
        result = score(_quote_fields(quotes.get(item.symbol, {})), values, comparable=bool(cik))
        results.append((item, result, values))
    path = write_report(render(results), Path(args.reports_dir))
    print(path)
    return path


def dry_run(args: argparse.Namespace) -> Path:
    fixture = Path(args.fixture)
    payload = json.loads(fixture.read_text())
    items = read_watchlist(Path(args.watchlist))
    results = []
    for item in items:
        entry = payload["companies"].get(item.symbol, {})
        values = dict(entry.get("financials", {}))
        for key in ("revenue", "eps", "fcf", "net_income", "equity", "debt"):
            if key in values:
                values[key] = {int(year): value for year, value in values[key].items()}
        results.append((item, score(entry.get("quote"), values, entry.get("comparable", True)), values))
    path = write_report(render(results), Path(args.reports_dir))
    print(path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a local, read-only Value Watch report.")
    sub = parser.add_subparsers(required=True)
    login = sub.add_parser("login", help="Authorize Schwab OAuth and save a local token.")
    login.set_defaults(func=lambda _: SchwabClient(Settings.from_env()).login())
    report = sub.add_parser("report", help="Fetch Schwab and SEC data then write a report.")
    report.add_argument("--watchlist", default=ROOT / "watchlist.csv")
    report.add_argument("--reports-dir", default=ROOT / "reports")
    report.add_argument("--refresh-sec", action="store_true", help="Refetch cached SEC Company Facts.")
    report.set_defaults(func=run)
    dry = sub.add_parser("dry-run", help="Render a report from fixtures; no credentials or network.")
    dry.add_argument("--watchlist", default=ROOT / "watchlist.csv")
    dry.add_argument("--fixture", default=ROOT / "tests/fixtures/offline.json")
    dry.add_argument("--reports-dir", default=ROOT / "reports")
    dry.set_defaults(func=dry_run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
