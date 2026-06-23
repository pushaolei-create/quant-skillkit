from __future__ import annotations

import pandas as pd

from .data import normalize_rows, simple_returns
from .risk import summarize_returns


def run_backtest(
    prices: pd.DataFrame,
    target_weights: pd.DataFrame,
    fee_bps: float = 5.0,
) -> dict:
    prices = prices.sort_index()
    target_weights = target_weights.reindex(prices.index).fillna(0.0)
    target_weights = normalize_rows(target_weights)

    asset_returns = simple_returns(prices)
    executed_weights = target_weights.shift(1).fillna(0.0)
    gross_returns = (executed_weights * asset_returns).sum(axis=1)
    turnover = target_weights.diff().abs().sum(axis=1).fillna(target_weights.abs().sum(axis=1))
    trading_cost = turnover * (fee_bps / 10000.0)
    net_returns = gross_returns - trading_cost
    equity_curve = (1.0 + net_returns).cumprod()
    summary = summarize_returns(net_returns, turnover=turnover)

    return {
        "returns": net_returns,
        "equity_curve": equity_curve,
        "weights": target_weights,
        "turnover": turnover,
        "summary": summary,
    }
