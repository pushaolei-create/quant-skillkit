# Hermes Integration

## Deployment shape

The easiest deployment path for `hermes` is:

1. run the toolkit as a local HTTP service
2. fetch or generate the tool manifest
3. register each endpoint as a callable tool inside `hermes`
4. let `hermes` pass market data payloads or prepared price records

## Start the service

```bash
python -m quant_skillkit.cli serve --host 0.0.0.0 --port 8010
python -m quant_skillkit.cli manifest --base-url http://127.0.0.1:8010
```

Or fetch the live discovery document:

```bash
curl http://127.0.0.1:8010/tools
```

## Suggested tool mapping

`quant.indicator.boll`

- method: `POST`
- path: `/indicators/boll`
- use when `hermes` needs volatility bands or z-score style mean-reversion context

`quant.indicator.dmi`

- method: `POST`
- path: `/indicators/dmi`
- use when `hermes` needs directional movement trend strength

`quant.portfolio.risk_parity`

- method: `POST`
- path: `/portfolio/risk-parity`
- use when `hermes` must allocate capital across assets from return history

`quant.options.greeks`

- method: `POST`
- path: `/options/greeks`
- use when `hermes` reasons about option sensitivity and volatility

`quant.strategy.backtest`

- method: `POST`
- path: `/strategy/backtest`
- use when `hermes` wants a quick sanity-check backtest before proposing a trade idea

## What was added for deployment

- [quant_skillkit/hermes_adapter.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/hermes_adapter.py)
  generates a structured manifest with tool schemas
- `GET /tools`
  exposes the live manifest from the running service
- [examples/hermes_tool_manifest.json](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/examples/hermes_tool_manifest.json)
  gives you a ready-to-import static version

## Example request

```json
{
  "strategy": "trend-following",
  "params": {
    "short_window": 10,
    "long_window": 30,
    "fee_bps": 5
  },
  "records": [
    {"date": "2026-01-01", "asset": "AAA", "close": 10.0},
    {"date": "2026-01-01", "asset": "BBB", "close": 12.0}
  ]
}
```

## Agent-side caution

- the service expects clean market data, not broker order events
- backtests are research-grade templates, not production execution simulators
- if you later need live brokerage integration, keep this toolkit as the research layer and place execution elsewhere
