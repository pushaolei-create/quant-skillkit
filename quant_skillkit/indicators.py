from __future__ import annotations

import numpy as np
import pandas as pd


def moving_average(prices: pd.Series, window: int) -> pd.Series:
    return prices.rolling(window).mean()


def bollinger_bands(prices: pd.Series, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    mid = prices.rolling(window).mean()
    std = prices.rolling(window).std(ddof=0)
    upper = mid + num_std * std
    lower = mid - num_std * std
    zscore = (prices - mid) / std.replace(0.0, np.nan)
    return pd.DataFrame({"mid": mid, "upper": upper, "lower": lower, "zscore": zscore})


def commodity_channel_index(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 20,
) -> pd.Series:
    typical_price = (high + low + close) / 3.0
    ma = typical_price.rolling(window).mean()
    mad = typical_price.rolling(window).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    return (typical_price - ma) / (0.015 * mad.replace(0.0, np.nan))


def chande_momentum_oscillator(prices: pd.Series, window: int = 14) -> pd.Series:
    diff = prices.diff()
    up = diff.clip(lower=0.0).rolling(window).sum()
    down = (-diff.clip(upper=0.0)).rolling(window).sum()
    denom = (up + down).replace(0.0, np.nan)
    return 100.0 * (up - down) / denom


def aroon(high: pd.Series, low: pd.Series, window: int = 25) -> pd.DataFrame:
    def aroon_up(values: np.ndarray) -> float:
        days_since_high = window - 1 - int(np.argmax(values))
        return 100.0 * (window - days_since_high) / window

    def aroon_down(values: np.ndarray) -> float:
        days_since_low = window - 1 - int(np.argmin(values))
        return 100.0 * (window - days_since_low) / window

    up = high.rolling(window).apply(aroon_up, raw=True)
    down = low.rolling(window).apply(aroon_down, raw=True)
    oscillator = up - down
    return pd.DataFrame({"aroon_up": up, "aroon_down": down, "oscillator": oscillator})


def dmi(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.DataFrame:
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0.0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0.0), down_move, 0.0)

    tr_components = pd.concat(
        [
            high - low,
            (high - close.shift(1)).abs(),
            (low - close.shift(1)).abs(),
        ],
        axis=1,
    )
    true_range = tr_components.max(axis=1)
    atr = true_range.rolling(window).mean()

    plus_di = 100.0 * pd.Series(plus_dm, index=high.index).rolling(window).mean() / atr.replace(0.0, np.nan)
    minus_di = 100.0 * pd.Series(minus_dm, index=high.index).rolling(window).mean() / atr.replace(0.0, np.nan)
    dx = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan)
    adx = dx.rolling(window).mean()
    return pd.DataFrame({"plus_di": plus_di, "minus_di": minus_di, "adx": adx})
