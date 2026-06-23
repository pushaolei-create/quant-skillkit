from __future__ import annotations

import argparse
import json

import pandas as pd

from .backtest import run_backtest
from .data import clean_price_data, load_price_csv, pivot_prices
from .hermes_adapter import build_hermes_manifest
from .indicators import aroon, bollinger_bands, commodity_channel_index, chande_momentum_oscillator, dmi
from .server import run_server
from .strategies import (
    market_neutral_alpha_weights,
    mean_reversion_weights,
    sector_rotation_weights,
    smart_beta_weights,
    trend_following_weights,
)


def _load_sectors(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    df = pd.read_csv(path)
    if "asset" not in df.columns or "sector" not in df.columns:
        raise ValueError("sector mapping CSV must contain asset and sector")
    return dict(zip(df["asset"], df["sector"]))


def command_indicators(args: argparse.Namespace) -> None:
    df = clean_price_data(load_price_csv(args.input))
    asset = args.asset or df["asset"].iloc[0]
    asset_df = df[df["asset"] == asset].sort_values("date")

    if args.indicator == "boll":
        result = bollinger_bands(asset_df["close"], window=args.window)
    elif args.indicator == "cmo":
        result = chande_momentum_oscillator(asset_df["close"], window=args.window).to_frame("cmo")
    elif args.indicator == "aroon":
        result = aroon(asset_df["high"], asset_df["low"], window=args.window)
    elif args.indicator == "cci":
        result = commodity_channel_index(asset_df["high"], asset_df["low"], asset_df["close"], window=args.window).to_frame("cci")
    elif args.indicator == "dmi":
        result = dmi(asset_df["high"], asset_df["low"], asset_df["close"], window=args.window)
    else:
        raise ValueError("unsupported indicator")

    print(result.tail(args.tail).to_json(orient="index", force_ascii=False))


def command_backtest(args: argparse.Namespace) -> None:
    df = clean_price_data(load_price_csv(args.input))
    prices = pivot_prices(df)

    if args.strategy == "trend-following":
        weights = trend_following_weights(prices, short_window=args.short_window, long_window=args.long_window)
    elif args.strategy == "mean-reversion":
        weights = mean_reversion_weights(prices, lookback=args.lookback, top_n=args.top_n)
    elif args.strategy == "smart-beta":
        weights = smart_beta_weights(prices, factor_mode=args.factor_mode, lookback=args.lookback, top_n=args.top_n)
    elif args.strategy == "market-neutral":
        weights = market_neutral_alpha_weights(prices, lookback=args.lookback, factor_mode=args.factor_mode)
    elif args.strategy == "sector-rotation":
        sectors = _load_sectors(args.sectors)
        if not sectors and "sector" in df.columns:
            sectors = dict(df.drop_duplicates("asset")[["asset", "sector"]].itertuples(index=False, name=None))
        weights = sector_rotation_weights(prices, sectors=sectors, lookback=args.lookback, top_k_sectors=args.top_k_sectors)
    else:
        raise ValueError("unsupported strategy")

    result = run_backtest(prices, weights, fee_bps=args.fee_bps)
    payload = {
        "summary": result["summary"],
        "final_equity": float(result["equity_curve"].iloc[-1]),
        "latest_weights": result["weights"].iloc[-1].round(6).to_dict(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_manifest(args: argparse.Namespace) -> None:
    print(json.dumps(build_hermes_manifest(base_url=args.base_url), ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="quant-skillkit")
    sub = parser.add_subparsers(dest="command", required=True)

    indicator = sub.add_parser("indicators")
    indicator.add_argument("--input", required=True)
    indicator.add_argument("--indicator", choices=["boll", "cmo", "aroon", "cci", "dmi"], required=True)
    indicator.add_argument("--asset")
    indicator.add_argument("--window", type=int, default=20)
    indicator.add_argument("--tail", type=int, default=5)
    indicator.set_defaults(func=command_indicators)

    backtest = sub.add_parser("backtest")
    backtest.add_argument("--input", required=True)
    backtest.add_argument("--strategy", choices=["trend-following", "mean-reversion", "smart-beta", "market-neutral", "sector-rotation"], required=True)
    backtest.add_argument("--lookback", type=int, default=20)
    backtest.add_argument("--short-window", type=int, default=20)
    backtest.add_argument("--long-window", type=int, default=60)
    backtest.add_argument("--top-n", type=int, default=3)
    backtest.add_argument("--top-k-sectors", type=int, default=2)
    backtest.add_argument("--factor-mode", choices=["momentum", "reversion"], default="momentum")
    backtest.add_argument("--fee-bps", type=float, default=5.0)
    backtest.add_argument("--sectors")
    backtest.set_defaults(func=command_backtest)

    manifest = sub.add_parser("manifest")
    manifest.add_argument("--base-url", default="http://127.0.0.1:8010")
    manifest.set_defaults(func=command_manifest)

    serve = sub.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8010)
    serve.set_defaults(func=lambda args: run_server(host=args.host, port=args.port))

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
