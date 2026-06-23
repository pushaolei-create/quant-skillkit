from __future__ import annotations

import math
from typing import Iterable

import pandas as pd


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _d1(spot: float, strike: float, rate: float, vol: float, maturity: float) -> float:
    return (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))


def _d2(d1: float, vol: float, maturity: float) -> float:
    return d1 - vol * math.sqrt(maturity)


def black_scholes_price(
    option_type: str,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> float:
    if maturity <= 0 or vol <= 0 or spot <= 0 or strike <= 0:
        intrinsic = max(0.0, spot - strike) if option_type == "call" else max(0.0, strike - spot)
        return intrinsic
    d1 = _d1(spot, strike, rate, vol, maturity)
    d2 = _d2(d1, vol, maturity)
    disc = math.exp(-rate * maturity)
    if option_type == "call":
        return spot * _norm_cdf(d1) - strike * disc * _norm_cdf(d2)
    return strike * disc * _norm_cdf(-d2) - spot * _norm_cdf(-d1)


def black_scholes_greeks(
    option_type: str,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> dict:
    if maturity <= 0 or vol <= 0 or spot <= 0 or strike <= 0:
        return {"price": black_scholes_price(option_type, spot, strike, rate, vol, maturity), "delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
    d1 = _d1(spot, strike, rate, vol, maturity)
    d2 = _d2(d1, vol, maturity)
    disc = math.exp(-rate * maturity)
    pdf = _norm_pdf(d1)
    sqrt_t = math.sqrt(maturity)
    call = option_type == "call"

    delta = _norm_cdf(d1) if call else _norm_cdf(d1) - 1.0
    gamma = pdf / (spot * vol * sqrt_t)
    vega = spot * pdf * sqrt_t
    if call:
        theta = -(spot * pdf * vol) / (2.0 * sqrt_t) - rate * strike * disc * _norm_cdf(d2)
        rho = strike * maturity * disc * _norm_cdf(d2)
    else:
        theta = -(spot * pdf * vol) / (2.0 * sqrt_t) + rate * strike * disc * _norm_cdf(-d2)
        rho = -strike * maturity * disc * _norm_cdf(-d2)

    return {
        "price": black_scholes_price(option_type, spot, strike, rate, vol, maturity),
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }


def implied_volatility(
    option_type: str,
    market_price: float,
    spot: float,
    strike: float,
    rate: float,
    maturity: float,
    initial_vol: float = 0.2,
    max_iter: int = 100,
    tolerance: float = 1e-6,
) -> float:
    vol = max(initial_vol, 1e-4)
    for _ in range(max_iter):
        greeks = black_scholes_greeks(option_type, spot, strike, rate, vol, maturity)
        diff = greeks["price"] - market_price
        if abs(diff) < tolerance:
            return float(vol)
        vega = greeks["vega"]
        if abs(vega) < 1e-8:
            break
        vol = max(1e-4, vol - diff / vega)
    return float(vol)


def volatility_smile(
    option_type: str,
    spot: float,
    strikes: Iterable[float],
    prices: Iterable[float],
    rate: float,
    maturity: float,
) -> pd.DataFrame:
    rows = []
    for strike, market_price in zip(strikes, prices):
        iv = implied_volatility(option_type, float(market_price), spot, float(strike), rate, maturity)
        rows.append({"strike": float(strike), "market_price": float(market_price), "implied_volatility": iv})
    return pd.DataFrame(rows).sort_values("strike").reset_index(drop=True)
