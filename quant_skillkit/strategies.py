from __future__ import annotations

from typing import Mapping

import pandas as pd

from .factors import market_neutralize, mean_reversion_score, momentum_score, sector_relative_strength
from .indicators import moving_average
from .portfolio import rank_weight


def trend_following_weights(
    prices: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 60,
) -> pd.DataFrame:
    short_ma = prices.rolling(short_window).mean()
    long_ma = prices.rolling(long_window).mean()
    signal = (short_ma > long_ma).astype(float)
    counts = signal.sum(axis=1).replace(0.0, pd.NA)
    return signal.div(counts, axis=0).fillna(0.0)


def mean_reversion_weights(prices: pd.DataFrame, lookback: int = 10, top_n: int = 3) -> pd.DataFrame:
    scores = mean_reversion_score(prices, lookback=lookback)
    rows = []
    for idx, row in scores.iterrows():
        rows.append(rank_weight(row, top_n=top_n, long_only=True).rename(idx))
    return pd.DataFrame(rows).reindex(prices.index).fillna(0.0)


def smart_beta_weights(
    prices: pd.DataFrame,
    factor_mode: str = "momentum",
    lookback: int = 20,
    top_n: int = 5,
) -> pd.DataFrame:
    if factor_mode == "momentum":
        scores = momentum_score(prices, lookback=lookback)
    elif factor_mode == "reversion":
        scores = mean_reversion_score(prices, lookback=lookback)
    else:
        raise ValueError("factor_mode must be momentum or reversion")

    rows = []
    for idx, row in scores.iterrows():
        rows.append(rank_weight(row, top_n=top_n, long_only=True).rename(idx))
    return pd.DataFrame(rows).reindex(prices.index).fillna(0.0)


def market_neutral_alpha_weights(
    prices: pd.DataFrame,
    lookback: int = 20,
    factor_mode: str = "momentum",
) -> pd.DataFrame:
    scores = momentum_score(prices, lookback=lookback) if factor_mode == "momentum" else mean_reversion_score(prices, lookback=lookback)
    rows = []
    for idx, row in scores.iterrows():
        rows.append(market_neutralize(row.dropna()).rename(idx))
    return pd.DataFrame(rows).reindex(prices.index).fillna(0.0)


def sector_rotation_weights(
    prices: pd.DataFrame,
    sectors: Mapping[str, str],
    lookback: int = 20,
    top_k_sectors: int = 2,
) -> pd.DataFrame:
    sector_scores = sector_relative_strength(prices, sectors, lookback=lookback)
    sector_names = pd.Series(sectors)
    rows = []

    for idx, row in sector_scores.iterrows():
        sector_rank = {}
        for asset, score in row.dropna().items():
            sector = sector_names.get(asset)
            if sector is None:
                continue
            sector_rank.setdefault(sector, []).append(float(score))
        top_sectors = sorted(sector_rank.items(), key=lambda kv: sum(kv[1]) / len(kv[1]), reverse=True)[:top_k_sectors]
        chosen = {name for name, _ in top_sectors}
        eligible = [asset for asset in prices.columns if sectors.get(asset) in chosen]
        rows.append(rank_weight(pd.Series(1.0, index=eligible), top_n=len(eligible), long_only=True).rename(idx))

    return pd.DataFrame(rows).reindex(prices.index).fillna(0.0)
