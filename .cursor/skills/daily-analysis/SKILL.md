---
name: daily-analysis
description: Institutional-grade US equity research workflow for analyzing US-listed stocks from a top Wall Street analyst perspective. Use when the user asks for comprehensive 美股分析, stock pitch, earnings review, valuation, target price, catalysts, risks, technical setup, portfolio view, or investment memo using Yahoo Finance and Bloomberg data.
---

# daily Analysis

Use this skill to produce rigorous US equity research, not casual ticker commentary. Treat Yahoo Finance as the default public data source. Always state data timestamps, source availability.

## Core Workflow

1. Clarify the ticker, listing, horizon, base currency, and output language if ambiguous. Default to Chinese, US-listed common stock/ADR, USD, and a 1-12 month investment horizon.
2. Gather current data before analyzing: price, market cap, volume, 52-week range, beta, analyst estimates, financial statements, earnings dates, guidance, valuation multiples, institutional ownership, news, and sector benchmarks.
3. Use `scripts/market_data.py` for a fast Yahoo Finance availability check when local Python is available. Dependencies live in the repository `.venv`. The script switches to that interpreter when the current `python3` cannot import `yfinance`. Read [references/data-sources.md](references/data-sources.md) for field mapping and fallback rules.
4. Build the analysis using [references/analysis-framework.md](references/analysis-framework.md). Do not skip fundamentals, valuation, catalysts, risks, and scenario analysis.
5. Format the answer with [references/report-template.md](references/report-template.md) unless the user requests a different format.
6. Cite web-accessible sources with links.
7. Include a short "not investment advice" note only at the end, without weakening the analysis.

## Analyst Standard

Act like an institutional analyst preparing a buy-side memo:

- Separate facts, assumptions, and judgment.
- Anchor valuation on forward fundamentals, not price action alone.
- Compare the company against peers and its own history.
- Explicitly identify the variant perception: what the market may be underpricing or overpricing.
- Include disconfirming evidence and what would change the view.
- Avoid false precision. Use ranges and probability-weighted scenarios where inputs are uncertain.

## Data Discipline

- For "latest", "today", earnings, guidance, price, estimates, ownership, and news, fetch current data. Do not rely on memory.
-  proceed with Yahoo Finance plus SEC filings, company IR, exchange data, or other cited public sources.
- Use official company filings/IR for reported financials when precision matters. Use Yahoo for market data, estimates, ownership, and screening context.

## Useful Commands

Run from the skill directory, or pass the full script path from the repository root. Either form uses `.venv` automatically when system `python3` does not have `yfinance`:

```bash
python3 scripts/market_data.py AAPL --period 1y --json
```

The script is a helper, not the full research process. It should speed up data gathering, then the agent must still reason through the investment case.