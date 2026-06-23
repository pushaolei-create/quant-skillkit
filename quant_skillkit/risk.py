from __future__ import annotations

import numpy as np
import pandas as pd


def max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1.0
    return float(drawdown.min())


def summarize_returns(returns: pd.Series, turnover: pd.Series | None = None, periods_per_year: int = 252) -> dict:
    returns = returns.fillna(0.0)
    equity = (1.0 + returns).cumprod()
    total_return = float(equity.iloc[-1] - 1.0)
    ann_return = float((1.0 + total_return) ** (periods_per_year / max(len(returns), 1)) - 1.0)
    ann_vol = float(returns.std(ddof=0) * np.sqrt(periods_per_year))
    sharpe = float(ann_return / ann_vol) if ann_vol > 0 else 0.0
    mdd = max_drawdown(equity)
    calmar = float(ann_return / abs(mdd)) if mdd < 0 else 0.0
    win_rate = float((returns > 0).mean())

    summary = {
        "total_return": total_return,
        "annual_return": ann_return,
        "annual_volatility": ann_vol,
        "sharpe": sharpe,
        "max_drawdown": mdd,
        "calmar": calmar,
        "win_rate": win_rate,
    }
    if turnover is not None:
        summary["avg_turnover"] = float(turnover.fillna(0.0).mean())
    return summary
