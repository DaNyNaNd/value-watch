from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path

from .http import request_json

# Do not request compression: urllib's minimal client does not transparently decode it.
SEC_HEADERS = {"User-Agent": "Value Watch/0.1 contact: local-user@example.invalid"}
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"


class SecCache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS company_facts (
            cik INTEGER PRIMARY KEY, symbol TEXT NOT NULL, fetched_on TEXT NOT NULL, payload TEXT NOT NULL)""")
        self.db.commit()

    def get(self, cik: int) -> dict | None:
        row = self.db.execute("SELECT payload FROM company_facts WHERE cik = ?", (cik,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, cik: int, symbol: str, payload: dict) -> None:
        self.db.execute("""INSERT INTO company_facts (cik, symbol, fetched_on, payload)
            VALUES (?, ?, ?, ?) ON CONFLICT(cik) DO UPDATE SET symbol=excluded.symbol,
            fetched_on=excluded.fetched_on, payload=excluded.payload""",
            (cik, symbol, date.today().isoformat(), json.dumps(payload)))
        self.db.commit()


def ticker_map() -> dict[str, int]:
    raw = request_json(TICKERS_URL, headers=SEC_HEADERS)
    return {entry["ticker"].upper(): int(entry["cik_str"]) for entry in raw.values()}


def company_facts(symbol: str, cik: int, cache: SecCache, refresh: bool = False) -> dict:
    cached = cache.get(cik)
    if cached and not refresh:
        return cached
    payload = request_json(FACTS_URL.format(cik=cik), headers=SEC_HEADERS)
    cache.put(cik, symbol, payload)
    return payload


def annual_values(facts: dict, tags: tuple[str, ...], unit: str = "USD") -> dict[int, float]:
    """Latest 10-K observation for each fiscal year under the first available tag."""
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        observations = us_gaap.get(tag, {}).get("units", {}).get(unit, [])
        values: dict[int, tuple[str, float]] = {}
        for item in observations:
            fy, form, value = item.get("fy"), item.get("form"), item.get("val")
            if not isinstance(fy, int) or form != "10-K" or value is None:
                continue
            filed = item.get("filed", "")
            if fy not in values or filed > values[fy][0]:
                values[fy] = (filed, float(value))
        if values:
            return {fy: pair[1] for fy, pair in values.items()}
    return {}


def financials(facts: dict) -> dict:
    revenue = annual_values(facts, ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"))
    eps = annual_values(facts, ("EarningsPerShareDiluted",), "USD/shares")
    cfo = annual_values(facts, ("NetCashProvidedByUsedInOperatingActivities",))
    capex = annual_values(facts, ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"))
    net_income = annual_values(facts, ("NetIncomeLoss",))
    equity = annual_values(facts, ("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"))
    debt = annual_values(facts, ("LongTermDebtAndFinanceLeaseObligations", "LongTermDebt", "LongTermDebtNoncurrent"))
    fcf = {year: cfo[year] - abs(capex[year]) for year in cfo.keys() & capex.keys()}
    def used_tag(tags: tuple[str, ...], unit: str = "USD") -> str:
        gaap = facts.get("facts", {}).get("us-gaap", {})
        return next((tag for tag in tags if gaap.get(tag, {}).get("units", {}).get(unit)), "N/A")
    cfo_tag = used_tag(("NetCashProvidedByUsedInOperatingActivities",))
    capex_tag = used_tag(("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"))
    return {"revenue": revenue, "eps": eps, "fcf": fcf, "net_income": net_income,
            "equity": equity, "debt": debt,
            "tags": {"revenue": used_tag(("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet")),
                     "eps": used_tag(("EarningsPerShareDiluted",), "USD/shares"),
                     "fcf": f"{cfo_tag} − {capex_tag}",
                     "equity": used_tag(("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")),
                     "debt": used_tag(("LongTermDebtAndFinanceLeaseObligations", "LongTermDebt", "LongTermDebtNoncurrent"))}}
