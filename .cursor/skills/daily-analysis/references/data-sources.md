# Data Sources

## Source Hierarchy

Use this order when sources are available:

1. Company IR, SEC EDGAR, 10-K, 10-Q, 8-K, earnings release, and call transcript for reported financials, guidance, capital allocation, and management commentary.
2. Yahoo Finance for public market data, chart history, profile, holders, options, news, estimates, and basic financial statements.
3. Exchange, index provider, FRED, Treasury, or sector-specific sources for macro and benchmark context.

## Yahoo Finance Fields

Use Yahoo Finance for:

- Quote: price, previous close, open, day range, 52-week range, volume, average volume, market cap, beta.
- Valuation: trailing P/E, forward P/E, PEG, price/sales, price/book, enterprise value, EV/EBITDA when available.
- Financials: revenue, gross profit, EBITDA, EBIT, net income, EPS, operating cash flow, capex, free cash flow, cash, debt.
- Estimates: revenue/EPS next quarter and fiscal year, recommendation trend, target price range.
- Market context: chart history, options chain, news headlines, sector/industry classification.

Prefer `yfinance` if installed. Otherwise query Yahoo public endpoints. Because Yahoo endpoints can change or throttle, treat script output as a starting point and verify important values with browser/source links.

## Time Stamps

Always record retrieval time and timezone. For this workspace the user's timezone is usually Asia/Shanghai unless the user says otherwise.