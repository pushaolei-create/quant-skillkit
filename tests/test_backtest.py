import unittest

import pandas as pd

from quant_skillkit.backtest import run_backtest
from quant_skillkit.options import black_scholes_greeks, implied_volatility
from quant_skillkit.strategies import trend_following_weights


class BacktestTests(unittest.TestCase):
    def test_trend_following_backtest_runs(self) -> None:
        idx = pd.date_range("2026-01-01", periods=8, freq="D")
        prices = pd.DataFrame(
            {
                "AAA": [10, 10.2, 10.4, 10.5, 10.8, 10.9, 11.0, 11.2],
                "BBB": [8.0, 7.9, 7.8, 7.7, 7.6, 7.5, 7.45, 7.4],
            },
            index=idx,
        )
        weights = trend_following_weights(prices, short_window=2, long_window=3)
        result = run_backtest(prices, weights)
        self.assertIn("summary", result)
        self.assertEqual(len(result["equity_curve"]), len(prices))

    def test_implied_volatility_is_positive(self) -> None:
        greeks = black_scholes_greeks("call", 100, 100, 0.02, 0.25, 0.5)
        iv = implied_volatility("call", greeks["price"], 100, 100, 0.02, 0.5)
        self.assertGreater(iv, 0.0)


if __name__ == "__main__":
    unittest.main()
