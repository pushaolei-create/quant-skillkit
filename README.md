# quant-skillkit

`quant-skillkit` is a lightweight Python toolkit distilled from the practical quant trading sections of *Python 与量化投资：从基础到实战*.

It is designed for two jobs:

- turn the book's quant ideas into reusable modules instead of notebook-only examples
- expose those modules through CLI and HTTP so an agent such as `hermes` can call them

## What is included

- data cleaning and wide-table preparation
- technical indicators: `AROON`, `BOLL`, `CCI`, `CMO`, `DMI`
- factor helpers: winsorize, z-score, momentum, mean reversion
- strategy templates: sector rotation, trend following, mean reversion, smart beta, market neutral alpha
- portfolio construction: rank weighting, mean-variance approximation, risk parity
- backtest engine with turnover and transaction cost support
- risk metrics: annual return, Sharpe, drawdown, Calmar, win rate
- option utilities: Black-Scholes price, Greeks, implied volatility, smile table
- stdlib HTTP API for agent integration
- Hermes manifest generator and `/tools` discovery endpoint

## Why this repo exists

The book's strongest practical value is in Chapters 4 to 6:

- Chapter 4: data acquisition and cleaning
- Chapter 5: backtesting and risk evaluation
- Chapter 6: strategy templates and quantitative research workflow

This repo turns those ideas into a reusable skill pack without copying the book's original code or text.

## Quick start

```bash
python -m quant_skillkit.cli backtest --input examples/sample_prices.csv --strategy trend-following
python -m quant_skillkit.cli indicators --input examples/sample_prices.csv --indicator boll
python -m quant_skillkit.cli manifest --base-url http://127.0.0.1:8010
python -m quant_skillkit.cli serve --host 127.0.0.1 --port 8010
```

## Input format

The default price file is a tidy CSV:

```text
date,asset,close,high,low,sector
2026-01-01,AAA,10.1,10.3,9.9,Tech
2026-01-01,BBB,8.2,8.4,8.0,Finance
```

Only `date`, `asset`, and `close` are mandatory for most features.

## Hermes integration

Start the local API:

```bash
python -m quant_skillkit.cli serve --host 0.0.0.0 --port 8010
```

Main endpoints:

- `GET /health`
- `GET /tools`
- `POST /indicators/{name}`
- `POST /portfolio/risk-parity`
- `POST /options/greeks`
- `POST /strategy/backtest`

An example tool manifest is in [examples/hermes_tool_manifest.json](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/examples/hermes_tool_manifest.json), and the generator lives in [quant_skillkit/hermes_adapter.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/hermes_adapter.py).

## Repository layout

- [quant_skillkit](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit)
- [docs/book-to-skillkit.md](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/docs/book-to-skillkit.md)
- [docs/hermes-integration.md](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/docs/hermes-integration.md)
- [tests](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/tests)

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```
