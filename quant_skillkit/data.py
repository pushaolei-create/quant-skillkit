from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def load_price_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns or "asset" not in df.columns or "close" not in df.columns:
        raise ValueError("CSV must contain date, asset, and close columns.")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["date", "asset"]).reset_index(drop=True)
    return df


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates(subset=["date", "asset"], keep="last")
    cleaned = cleaned.sort_values(["date", "asset"]).reset_index(drop=True)
    numeric_cols = [col for col in ["close", "open", "high", "low", "volume"] if col in cleaned.columns]
    for col in numeric_cols:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
    cleaned = cleaned.dropna(subset=["close"])
    return cleaned


def pivot_prices(
    df: pd.DataFrame,
    value_col: str = "close",
    date_col: str = "date",
    asset_col: str = "asset",
) -> pd.DataFrame:
    wide = df.pivot(index=date_col, columns=asset_col, values=value_col).sort_index()
    wide.index = pd.to_datetime(wide.index)
    return wide


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.sort_index().pct_change().replace([np.inf, -np.inf], np.nan).fillna(0.0)


def normalize_rows(frame: pd.DataFrame) -> pd.DataFrame:
    denom = frame.abs().sum(axis=1).replace(0.0, np.nan)
    normalized = frame.div(denom, axis=0).fillna(0.0)
    return normalized


def forward_fill_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_index().ffill()


def rolling_window_view(values: Iterable[float], window: int) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    if window <= 0:
        raise ValueError("window must be positive")
    if arr.size < window:
        return np.empty((0, window))
    stride = arr.strides[0]
    shape = (arr.size - window + 1, window)
    return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=(stride, stride))
