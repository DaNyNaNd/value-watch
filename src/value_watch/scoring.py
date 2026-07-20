from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Check:
    name: str
    value: str
    passed: bool | None
    reason: str


@dataclass(frozen=True)
class Result:
    value_points: int
    quality_points: int
    label: str
    checks: list[Check]


def _latest(values: dict[int, float]) -> tuple[int, float] | None:
    return max(values.items()) if values else None


def _five(values: dict[int, float]) -> list[tuple[int, float]] | None:
    years = sorted(values)[-5:]
    return [(year, values[year]) for year in years] if len(years) == 5 and years == list(range(years[0], years[0] + 5)) else None


def _cagr(values: list[tuple[int, float]]) -> float | None:
    start, end = values[0][1], values[-1][1]
    return (end / start) ** (1 / 4) - 1 if start > 0 and end > 0 else None


def score(quote: dict | None, financials: dict | None, comparable: bool = True) -> Result:
    financials = financials or {}
    quote = quote or {}
    checks: list[Check] = []
    pe = quote.get("peRatio") or quote.get("peRatioTTM")
    checks.append(Check("Earnings yield", f"P/E {pe:.2f}" if isinstance(pe, (int, float)) else "N/A",
                        pe > 0 and pe <= 25 if isinstance(pe, (int, float)) else None,
                        "P/E is positive and ≤ 25" if isinstance(pe, (int, float)) else "Schwab P/E unavailable"))
    market_cap = quote.get("marketCap")
    fcf = financials.get("fcf", {})
    latest_fcf = _latest(fcf)
    fcf_yield = latest_fcf[1] / market_cap if latest_fcf and market_cap else None
    checks.append(Check("FCF yield", f"{fcf_yield:.1%}" if fcf_yield is not None else "N/A",
                        fcf_yield >= .04 if fcf_yield is not None else None,
                        "Annual FCF ÷ market cap ≥ 4%" if fcf_yield is not None else "FCF or market cap unavailable"))
    revenue5, eps5, fcf5 = (_five(financials.get(key, {})) for key in ("revenue", "eps", "fcf"))
    for name, values, threshold in (("Revenue trend", revenue5, 0), ("EPS trend", eps5, 0)):
        rate = _cagr(values) if values else None
        checks.append(Check(name, f"{rate:.1%} CAGR" if rate is not None else "N/A",
                            rate > threshold if rate is not None else None,
                            "Five-year CAGR is positive" if rate is not None else "Five contiguous annual values and positive endpoints required"))
    positives = sum(value > 0 for _, value in fcf5) if fcf5 else None
    checks.append(Check("FCF consistency", f"{positives}/5 positive" if positives is not None else "N/A",
                        positives >= 4 if positives is not None else None,
                        "At least 4 of the last 5 annual FCF values are positive" if positives is not None else "Five contiguous annual FCF values required"))
    income, equity = financials.get("net_income", {}), financials.get("equity", {})
    latest_income = _latest(income)
    latest_equity = _latest(equity)
    prior_equity = equity.get(latest_equity[0] - 1) if latest_equity else None
    roe = latest_income[1] / ((latest_equity[1] + prior_equity) / 2) if latest_income and latest_equity and prior_equity else None
    checks.append(Check("Return on equity", f"{roe:.1%}" if roe is not None else "N/A",
                        roe >= .15 if roe is not None else None,
                        "Latest income ÷ average beginning/end equity ≥ 15%" if roe is not None else "Annual net income and two equity values required"))
    debt = _latest(financials.get("debt", {}))
    debt_ratio = debt[1] / latest_fcf[1] if debt and latest_fcf and latest_fcf[1] > 0 else None
    checks.append(Check("Debt sanity", f"{debt_ratio:.2f}× FCF" if debt_ratio is not None else "N/A",
                        debt_ratio <= 3 if debt_ratio is not None else None,
                        "Total debt ≤ 3× latest annual FCF" if debt_ratio is not None else "Debt and positive latest FCF required"))
    value_points = sum(check.passed is True for check in checks[:2])
    quality_points = sum(check.passed is True for check in checks[2:])
    complete = all(check.passed is not None for check in checks[:5])
    label = "Review" if comparable and complete and value_points >= 1 and quality_points >= 3 else "Watch" if comparable and complete else "Insufficient data"
    return Result(value_points, quality_points, label, checks)
