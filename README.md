# quant-skillkit

`quant-skillkit` is a lightweight Python toolkit for turning practical quant trading ideas into reusable research and agent-facing tools.

It was inspired by the hands-on quant sections of *Python 与量化投资：从基础到实战*, but this repository does not reproduce the book's original code or text. Instead, it reshapes the underlying ideas into a clean, dependency-light package that is easier to run, extend, and deploy.

## Why this project exists

A lot of quant learning material stops at notebooks or platform-specific demos. This project is for the next step:

- reusable quant research components instead of one-off examples
- built-in strategy templates for fast experimentation
- simple CLI workflows for local analysis
- HTTP endpoints and tool manifests for agent integration

If you want a compact bridge between quant research, backtesting, and agent tooling, this repo is built for that.

## Core capabilities

- Data preparation: tidy price loading, cleaning, pivoting, return generation
- Indicators: `AROON`, `BOLL`, `CCI`, `CMO`, `DMI`
- Factor helpers: winsorization, z-score, momentum, mean reversion
- Strategy templates: sector rotation, trend following, mean reversion, smart beta, market neutral alpha
- Portfolio construction: rank weighting, mean-variance approximation, risk parity
- Backtesting: turnover-aware backtest engine with transaction cost support
- Risk analytics: annual return, Sharpe, drawdown, Calmar, win rate
- Options utilities: Black-Scholes price, Greeks, implied volatility, volatility smile
- Agent integration: stdlib HTTP API, Hermes manifest generator, `/tools` discovery endpoint

## Installation

```bash
git clone https://github.com/pushaolei-create/quant-skillkit.git
cd quant-skillkit
python -m pip install -e .
```

Dependencies are intentionally minimal:

- `numpy`
- `pandas`

## Quick start

Run a sample backtest:

```bash
python -m quant_skillkit.cli backtest --input examples/sample_prices.csv --strategy smart-beta --lookback 3 --top-n 2
```

Generate a Hermes-friendly manifest:

```bash
python -m quant_skillkit.cli manifest --base-url http://127.0.0.1:8010
```

Start the local API service:

```bash
python -m quant_skillkit.cli serve --host 127.0.0.1 --port 8010
```

Calculate an indicator from sample data:

```bash
python -m quant_skillkit.cli indicators --input examples/sample_prices.csv --indicator boll
```

## Input format

The default input is a tidy CSV:

```text
date,asset,close,high,low,sector
2026-01-01,AAA,10.1,10.3,9.9,Tech
2026-01-01,BBB,8.2,8.4,8.0,Finance
```

Required columns for most workflows:

- `date`
- `asset`
- `close`

Useful optional columns:

- `high`
- `low`
- `sector`

## Hermes integration

Start the service:

```bash
python -m quant_skillkit.cli serve --host 0.0.0.0 --port 8010
```

Available endpoints:

- `GET /health`
- `GET /tools`
- `POST /indicators/{name}`
- `POST /portfolio/risk-parity`
- `POST /options/greeks`
- `POST /strategy/backtest`

Useful integration files:

- [examples/hermes_tool_manifest.json](examples/hermes_tool_manifest.json)
- [quant_skillkit/hermes_adapter.py](quant_skillkit/hermes_adapter.py)
- [docs/hermes-integration.md](docs/hermes-integration.md)

## Project structure

- [quant_skillkit](quant_skillkit)
- [docs/book-to-skillkit.md](docs/book-to-skillkit.md)
- [docs/hermes-integration.md](docs/hermes-integration.md)
- [examples](examples)
- [tests](tests)

## Validation

Run tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Notes

- This repo is a research toolkit, not a production execution engine.
- Backtest results are template-grade and should not be treated as live trading evidence.
- If you later need broker connectivity or production orchestration, it is better to keep this project as the research and signal layer.
