#!/usr/bin/env python3
"""Fetch quick US equity market data through yfinance."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from typing import Any


QUOTE_KEYS = [
    "symbol",
    "shortName",
    "longName",
    "currency",
    "exchange",
    "regularMarketPrice",
    "regularMarketChangePercent",
    "regularMarketPreviousClose",
    "regularMarketOpen",
    "regularMarketDayLow",
    "regularMarketDayHigh",
    "regularMarketVolume",
    "averageDailyVolume3Month",
    "marketCap",
    "fiftyTwoWeekLow",
    "fiftyTwoWeekHigh",
    "trailingPE",
    "forwardPE",
    "priceToBook",
    "epsTrailingTwelveMonths",
    "epsForward",
    "sharesOutstanding",
]

EXTRA_KEYS = [
    "sector",
    "industry",
    "website",
    "enterpriseValue",
    "enterpriseToRevenue",
    "enterpriseToEbitda",
    "profitMargins",
    "grossMargins",
    "operatingMargins",
    "returnOnEquity",
    "returnOnAssets",
    "totalCash",
    "totalDebt",
    "freeCashflow",
    "recommendationKey",
    "targetMeanPrice",
    "targetHighPrice",
    "targetLowPrice",
    "numberOfAnalystOpinions",
]


def utc_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def require_yfinance():
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError(
            "yfinance is not installed. Install dependencies from requirements.txt."
        ) from exc
    return yf


def json_value(value: Any) -> Any:
    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            return value
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def pick_fields(info: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    picked: dict[str, Any] = {}
    for key in keys:
        if key not in info:
            continue
        value = json_value(info.get(key))
        if value is not None:
            picked[key] = value
    return picked


def quote_from_info(symbol: str, info: dict[str, Any]) -> dict[str, Any]:
    quote = pick_fields(info, QUOTE_KEYS)
    quote.setdefault("symbol", symbol.upper())
    return quote


def chart_from_history(history: Any, period: str, interval: str, info: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {
        "currency": json_value(info.get("currency")),
        "exchangeName": json_value(info.get("fullExchangeName") or info.get("exchange")),
        "instrumentType": json_value(info.get("quoteType")),
        "firstTradeDate": json_value(info.get("firstTradeDateEpochUtc")),
        "regularMarketTime": json_value(info.get("regularMarketTime")),
        "period": period,
        "interval": interval,
        "points": 0,
    }
    if history is None or getattr(history, "empty", True) or "Close" not in getattr(history, "columns", []):
        compact["error"] = "yfinance returned no chart data"
        return {key: value for key, value in compact.items() if value is not None}

    close = history["Close"].dropna()
    numeric_close = [json_value(value) for value in close.tolist()]
    numeric_close = [value for value in numeric_close if isinstance(value, (int, float)) and not isinstance(value, bool)]
    compact["points"] = int(len(history))
    if numeric_close:
        compact.update(
            {
                "close_first": numeric_close[0],
                "close_last": numeric_close[-1],
                "close_min": min(numeric_close),
                "close_max": max(numeric_close),
                "return_pct": (numeric_close[-1] / numeric_close[0] - 1) * 100 if numeric_close[0] else None,
            }
        )
    return {key: value for key, value in compact.items() if value is not None}


def collect(symbol: str, period: str, interval: str) -> dict[str, Any]:
    yf = require_yfinance()
    ticker = yf.Ticker(symbol)
    info: dict[str, Any] = {}
    info_error: str | None = None
    try:
        raw_info = ticker.get_info()
        if isinstance(raw_info, dict):
            info = raw_info
    except Exception as exc:
        info_error = str(exc)

    try:
        history = ticker.history(period=period, interval=interval, auto_adjust=False)
    except Exception as exc:
        raise RuntimeError(f"yfinance chart request failed for {symbol}: {exc}") from exc

    quote = quote_from_info(symbol, info)
    chart = chart_from_history(history, period, interval, info)
    if not quote.get("regularMarketPrice") and chart.get("error"):
        detail = info_error or chart["error"]
        raise RuntimeError(f"yfinance returned no quote or chart data for {symbol}: {detail}")

    result: dict[str, Any] = {
        "symbol": symbol.upper(),
        "retrieved_at_utc": utc_timestamp(),
        "sources": {"yfinance": True},
        "yahoo_quote": quote,
        "yahoo_chart": chart,
    }
    extra = pick_fields(info, EXTRA_KEYS)
    if info_error:
        extra["yfinance_info_error"] = info_error
    if extra:
        result["yfinance_extra"] = extra
    return result


def print_summary(data: dict[str, Any]) -> None:
    quote = data.get("yahoo_quote", {})
    chart = data.get("yahoo_chart", {})
    extra = data.get("yfinance_extra", {})
    print(f"Symbol: {data.get('symbol')}")
    print(f"Retrieved UTC: {data.get('retrieved_at_utc')}")
    print(f"Name: {quote.get('longName') or quote.get('shortName')}")
    print(f"Price: {quote.get('regularMarketPrice')} {quote.get('currency')}")
    print(f"1D %: {quote.get('regularMarketChangePercent')}")
    print(f"Market cap: {quote.get('marketCap')}")
    print(f"52-week range: {quote.get('fiftyTwoWeekLow')} - {quote.get('fiftyTwoWeekHigh')}")
    print(f"Forward P/E: {quote.get('forwardPE')}")
    print(f"EV/EBITDA: {extra.get('enterpriseToEbitda')}")
    print(f"Target mean: {extra.get('targetMeanPrice')}")
    print(f"{chart.get('period')} return %: {chart.get('return_pct')}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch quick US equity data through yfinance.")
    parser.add_argument("symbol", help="US ticker, for example AAPL or NVDA")
    parser.add_argument("--period", default="1y", help="Chart range, for example 6mo, 1y, 2y, 5y")
    parser.add_argument("--interval", default="1d", help="Chart interval, for example 1d, 1wk, 1mo")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a text summary")
    args = parser.parse_args(argv)

    try:
        data = collect(args.symbol, args.period, args.interval)
    except (RuntimeError, TimeoutError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print_summary(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
