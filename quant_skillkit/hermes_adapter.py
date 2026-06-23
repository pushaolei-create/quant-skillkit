from __future__ import annotations


def _tool(
    name: str,
    description: str,
    method: str,
    path: str,
    input_schema: dict,
    tags: list[str],
) -> dict:
    return {
        "name": name,
        "description": description,
        "transport": {
            "type": "http",
            "method": method,
            "path": path,
        },
        "input_schema": input_schema,
        "tags": tags,
    }


def build_hermes_manifest(base_url: str = "http://127.0.0.1:8010") -> dict:
    base = base_url.rstrip("/")
    tools = [
        _tool(
            name="quant.indicator.boll",
            description="Calculate Bollinger Bands for a price series.",
            method="POST",
            path="/indicators/boll",
            input_schema={
                "type": "object",
                "required": ["prices"],
                "properties": {
                    "prices": {"type": "array", "items": {"type": "number"}},
                    "window": {"type": "integer", "default": 20},
                },
            },
            tags=["indicator", "volatility", "mean-reversion"],
        ),
        _tool(
            name="quant.indicator.dmi",
            description="Calculate DMI and ADX trend strength from OHLC data.",
            method="POST",
            path="/indicators/dmi",
            input_schema={
                "type": "object",
                "required": ["high", "low", "close"],
                "properties": {
                    "high": {"type": "array", "items": {"type": "number"}},
                    "low": {"type": "array", "items": {"type": "number"}},
                    "close": {"type": "array", "items": {"type": "number"}},
                    "window": {"type": "integer", "default": 14},
                },
            },
            tags=["indicator", "trend"],
        ),
        _tool(
            name="quant.portfolio.risk_parity",
            description="Allocate risk-parity weights from a return matrix.",
            method="POST",
            path="/portfolio/risk-parity",
            input_schema={
                "type": "object",
                "required": ["returns"],
                "properties": {
                    "returns": {
                        "type": "object",
                        "description": "Column-oriented return matrix keyed by asset name.",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"type": "number"},
                        },
                    }
                },
            },
            tags=["portfolio", "allocation"],
        ),
        _tool(
            name="quant.options.greeks",
            description="Calculate Black-Scholes price and Greeks for a vanilla option.",
            method="POST",
            path="/options/greeks",
            input_schema={
                "type": "object",
                "required": ["option_type", "spot", "strike", "rate", "vol", "maturity"],
                "properties": {
                    "option_type": {"type": "string", "enum": ["call", "put"]},
                    "spot": {"type": "number"},
                    "strike": {"type": "number"},
                    "rate": {"type": "number"},
                    "vol": {"type": "number"},
                    "maturity": {"type": "number"},
                },
            },
            tags=["options", "derivatives", "risk"],
        ),
        _tool(
            name="quant.strategy.backtest",
            description="Run a lightweight backtest over prepared price records using built-in quant strategy templates.",
            method="POST",
            path="/strategy/backtest",
            input_schema={
                "type": "object",
                "required": ["strategy", "records"],
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": [
                            "trend-following",
                            "mean-reversion",
                            "smart-beta",
                            "market-neutral",
                            "sector-rotation",
                        ],
                    },
                    "params": {"type": "object"},
                    "sectors": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                    },
                    "records": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["date", "asset", "close"],
                            "properties": {
                                "date": {"type": "string"},
                                "asset": {"type": "string"},
                                "close": {"type": "number"},
                                "high": {"type": "number"},
                                "low": {"type": "number"},
                                "sector": {"type": "string"},
                            },
                        },
                    },
                },
            },
            tags=["strategy", "backtest", "research"],
        ),
    ]

    return {
        "name": "quant-skillkit",
        "version": "0.1.0",
        "base_url": base,
        "healthcheck": f"{base}/health",
        "tools_endpoint": f"{base}/tools",
        "tools": [
            {
                **tool,
                "transport": {
                    **tool["transport"],
                    "url": f"{base}{tool['transport']['path']}",
                },
            }
            for tool in tools
        ],
    }
