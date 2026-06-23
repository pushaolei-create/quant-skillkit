from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd


def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lower=lo, upper=hi)


def zscore_series(series: pd.Series) -> pd.Series:
    std = series.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / std


def cross_sectional_rank(series: pd.Series, ascending: bool = False) -> pd.Series:
    return series.rank(ascending=ascending, pct=True)


def momentum_score(prices: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    return prices / prices.shift(lookback) - 1.0


def mean_reversion_score(prices: pd.DataFrame, lookback: int = 10) -> pd.DataFrame:
    rolling_mean = prices.rolling(lookback).mean()
    rolling_std = prices.rolling(lookback).std(ddof=0).replace(0.0, np.nan)
    return -1.0 * ((prices - rolling_mean) / rolling_std)


def sector_relative_strength(
    prices: pd.DataFrame,
    sectors: Mapping[str, str],
    lookback: int = 20,
) -> pd.DataFrame:
    asset_returns = prices / prices.shift(lookback) - 1.0
    sector_frame = pd.DataFrame(index=asset_returns.index, columns=asset_returns.columns, dtype=float)
    sector_groups: dict[str, list[str]] = {}
    for asset, sector in sectors.items():
        if asset in asset_returns.columns:
            sector_groups.setdefault(sector, []).append(asset)

    for sector, assets in sector_groups.items():
        sector_score = asset_returns[assets].mean(axis=1)
        sector_frame.loc[:, assets] = np.repeat(sector_score.to_numpy().reshape(-1, 1), len(assets), axis=1)

    return sector_frame


def market_neutralize(scores: pd.Series) -> pd.Series:
    centered = scores - scores.mean()
    longs = centered.clip(lower=0.0)
    shorts = centered.clip(upper=0.0)
    long_sum = longs.sum()
    short_sum = shorts.abs().sum()
    out = pd.Series(0.0, index=scores.index)
    if long_sum > 0:
        out += 0.5 * longs / long_sum
    if short_sum > 0:
        out += 0.5 * shorts / short_sum
    return out
