from __future__ import annotations

import numpy as np
import pandas as pd


def equal_weight(assets: list[str]) -> pd.Series:
    if not assets:
        return pd.Series(dtype=float)
    weight = 1.0 / len(assets)
    return pd.Series(weight, index=assets, dtype=float)


def rank_weight(scores: pd.Series, top_n: int = 5, long_only: bool = True) -> pd.Series:
    ranked = scores.dropna().sort_values(ascending=False)
    selected = ranked.head(top_n)
    if selected.empty:
        return pd.Series(0.0, index=scores.index)
    weights = pd.Series(0.0, index=scores.index, dtype=float)
    if long_only:
        weights.loc[selected.index] = 1.0 / len(selected)
        return weights
    centered = selected - selected.mean()
    denom = centered.abs().sum()
    if denom == 0:
        return weights
    weights.loc[selected.index] = centered / denom
    return weights


def mean_variance_weights(
    expected_returns: pd.Series,
    covariance: pd.DataFrame,
    risk_aversion: float = 3.0,
    long_only: bool = True,
) -> pd.Series:
    aligned_cov = covariance.loc[expected_returns.index, expected_returns.index]
    regularized = aligned_cov + np.eye(len(aligned_cov)) * 1e-6
    raw = np.linalg.solve(regularized.to_numpy(), expected_returns.to_numpy())
    raw = pd.Series(raw / max(risk_aversion, 1e-6), index=expected_returns.index)
    if long_only:
        raw = raw.clip(lower=0.0)
    denom = raw.abs().sum()
    if denom == 0:
        return pd.Series(0.0, index=expected_returns.index)
    return raw / denom


def risk_parity_weights(
    returns_window: pd.DataFrame,
    max_iter: int = 200,
    tolerance: float = 1e-6,
) -> pd.Series:
    cols = returns_window.columns
    if returns_window.empty:
        return pd.Series(dtype=float)
    cov = returns_window.cov().to_numpy()
    n = cov.shape[0]
    w = np.full(n, 1.0 / n)
    target = 1.0 / n

    for _ in range(max_iter):
        portfolio_var = float(w.T @ cov @ w)
        if portfolio_var <= 0:
            break
        marginal = cov @ w
        contributions = w * marginal / np.sqrt(portfolio_var)
        total = contributions.sum()
        if total == 0:
            break
        normalized = contributions / total
        gap = normalized - target
        if np.max(np.abs(gap)) < tolerance:
            break
        w *= np.clip(target / np.where(normalized == 0, 1e-8, normalized), 0.5, 1.5)
        w = np.clip(w, 1e-8, None)
        w /= w.sum()

    return pd.Series(w, index=cols)
