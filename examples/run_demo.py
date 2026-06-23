from quant_skillkit.backtest import run_backtest
from quant_skillkit.data import clean_price_data, load_price_csv, pivot_prices
from quant_skillkit.strategies import smart_beta_weights


df = clean_price_data(load_price_csv("examples/sample_prices.csv"))
prices = pivot_prices(df)
weights = smart_beta_weights(prices, factor_mode="momentum", lookback=3, top_n=2)
result = run_backtest(prices, weights, fee_bps=5)
print(result["summary"])
