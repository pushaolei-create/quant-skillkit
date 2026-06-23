import unittest

import pandas as pd

from quant_skillkit.indicators import bollinger_bands, chande_momentum_oscillator


class IndicatorTests(unittest.TestCase):
    def test_bollinger_has_columns(self) -> None:
        series = pd.Series([1, 2, 3, 4, 5, 6, 7])
        bands = bollinger_bands(series, window=3)
        self.assertEqual(list(bands.columns), ["mid", "upper", "lower", "zscore"])

    def test_cmo_range(self) -> None:
        series = pd.Series([1, 2, 3, 2, 1, 2, 3, 4, 3, 2])
        cmo = chande_momentum_oscillator(series, window=3).dropna()
        self.assertTrue(((cmo >= -100) & (cmo <= 100)).all())


if __name__ == "__main__":
    unittest.main()
