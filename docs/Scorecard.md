# Value Watch Scorecard

This is a triage screen for a human investor. It does not produce investment advice, a price target, or a trade decision.

## Universe

The first version supports U.S. operating companies that file standard financial statements with the SEC. Exclude banks, insurers, REITs, funds, ETFs, ADRs, and companies with fewer than five annual data points. Their capital structures or reporting conventions need different measures.

The user supplies a one-sentence description of how each company makes money before a symbol can be screened. A score never substitutes for understanding the business.

## Inputs and definitions

| Input | Definition | Refresh |
| --- | --- | --- |
| Price and P/E | Schwab quote fields. P/E must be positive. | Weekly |
| Market capitalization | Current market capitalization from Schwab, or current price × latest shares outstanding if unavailable. | Weekly |
| Revenue and EPS | Annual SEC XBRL facts, using the most recent value for each fiscal year. | After a filing |
| Free cash flow (FCF) | Cash from operations minus capital expenditures. The report must show the tags used. | After a filing |
| ROE | Latest annual net income ÷ average beginning/end equity, when both values exist. | After a filing |
| Debt burden | Latest total debt ÷ latest annual FCF. | After a filing |

Never substitute a missing value with zero. A field is `N/A` when its source or definition is unavailable.

## Screen

Award one point for each passing check. Display every input, pass/fail result, and reason.

### Value: 0–2 points

1. **Earnings yield:** P/E is positive and no greater than 25 (earnings yield of at least 4%).
2. **FCF yield:** Latest annual FCF ÷ current market capitalization is at least 4%.

### Realization / financial quality: 0–5 points

1. **Revenue trend:** five-year revenue CAGR is positive.
2. **EPS trend:** five-year EPS CAGR is positive. Do not calculate a CAGR across a zero or negative starting EPS; mark it `N/A`.
3. **FCF consistency:** FCF is positive in at least four of the last five fiscal years.
4. **Returns on equity:** latest annual ROE is at least 15%.
5. **Debt sanity:** total debt is no more than three times latest annual FCF.

## Labels

- **Review:** at least 1 value point, at least 3 quality points, and all five years of revenue, EPS, and FCF are present.
- **Watch:** enough data to calculate the screen, but the review condition is not met.
- **Insufficient data:** a required source value is missing, stale, non-comparable, or the company is outside the initial universe.

The report should sort `Review` first, then `Watch`, then `Insufficient data`; within a label, show value points before quality points. Scores are never compared across sectors as proof that one business is better.

## Human review after a `Review` label

Before any action, answer these outside the automated score:

1. Can I explain the business and its main risk in one sentence each?
2. Why might the market be pricing it this way?
3. What would have to be true for the current value screen to be misleading?
4. Would I be comfortable owning it for ten years?

If the answer is unclear, retain the label as a prompt for research, not a conclusion.
