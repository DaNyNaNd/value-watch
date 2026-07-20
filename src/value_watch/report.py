from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .scoring import Result
from .watchlist import WatchItem


ORDER = {"Review": 0, "Watch": 1, "Insufficient data": 2}


def render(items: list[tuple[WatchItem, Result, dict]], generated_at: datetime | None = None) -> str:
    generated_at = generated_at or datetime.now(timezone.utc)
    sections: list[str] = ["# Value Watch weekly report", "",
        f"Generated: {generated_at.strftime('%Y-%m-%d %H:%M UTC')}", "",
        "This is a research triage screen, not investment advice or a trade recommendation.", ""]
    for label in ("Review", "Watch", "Insufficient data"):
        group = sorted((item for item in items if item[1].label == label),
                       key=lambda item: (-item[1].value_points, -item[1].quality_points, item[0].symbol))
        sections.extend([f"## {label}", ""])
        if not group:
            sections.extend(["None.", ""])
        for watch, result, financials in group:
            sections.extend([f"### {watch.symbol} — {result.value_points}/2 value, {result.quality_points}/5 quality", "",
                watch.description, "", "| Check | Input | Result | Reason |", "| --- | --- | --- | --- |"])
            for check in result.checks:
                verdict = "Pass" if check.passed is True else "Fail" if check.passed is False else "N/A"
                sections.append(f"| {check.name} | {check.value} | {verdict} | {check.reason} |")
            tags = financials.get("tags", {})
            sections.extend(["", f"FCF definition/tags: {tags.get('fcf', 'N/A')}", ""])
    sections.extend(["## Human review for a Review label", "",
        "Explain the business and its main risk; assess why the market prices it this way; identify what could make the screen misleading; and consider a ten-year holding period.", ""])
    return "\n".join(sections)


def write_report(content: str, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"weekly-{datetime.now().date().isoformat()}.md"
    path.write_text(content)
    return path
