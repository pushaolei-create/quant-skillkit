from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import pandas as pd

from .backtest import run_backtest
from .hermes_adapter import build_hermes_manifest
from .indicators import aroon, bollinger_bands, commodity_channel_index, chande_momentum_oscillator, dmi
from .options import black_scholes_greeks
from .portfolio import risk_parity_weights
from .strategies import (
    market_neutral_alpha_weights,
    mean_reversion_weights,
    sector_rotation_weights,
    smart_beta_weights,
    trend_following_weights,
)


def _frame_from_payload(payload: dict) -> pd.DataFrame:
    if "records" not in payload:
        raise ValueError("payload must contain records")
    df = pd.DataFrame(payload["records"])
    df["date"] = pd.to_datetime(df["date"])
    return df


class QuantSkillHandler(BaseHTTPRequestHandler):
    server_version = "QuantSkillKit/0.1"

    def _write_json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._write_json(200, {"ok": True, "service": "quant-skillkit"})
            return
        if parsed.path == "/tools":
            host = self.headers.get("Host", "127.0.0.1:8010")
            self._write_json(200, build_hermes_manifest(base_url=f"http://{host}"))
            return
        self._write_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            body = self._read_json()
            if parsed.path.startswith("/indicators/"):
                self._handle_indicator(parsed.path.split("/")[-1], body)
                return
            if parsed.path == "/portfolio/risk-parity":
                self._handle_risk_parity(body)
                return
            if parsed.path == "/options/greeks":
                self._handle_option_greeks(body)
                return
            if parsed.path == "/strategy/backtest":
                self._handle_backtest(body)
                return
            self._write_json(404, {"error": "not found"})
        except Exception as exc:
            self._write_json(400, {"error": str(exc)})

    def _handle_indicator(self, name: str, body: dict) -> None:
        series = pd.Series(body["prices"], dtype=float)
        if name == "boll":
            result = bollinger_bands(series, window=int(body.get("window", 20))).fillna("").to_dict(orient="list")
        elif name == "cmo":
            result = {"cmo": chande_momentum_oscillator(series, window=int(body.get("window", 14))).fillna("").tolist()}
        elif name == "aroon":
            high = pd.Series(body["high"], dtype=float)
            low = pd.Series(body["low"], dtype=float)
            result = aroon(high, low, window=int(body.get("window", 25))).fillna("").to_dict(orient="list")
        elif name == "cci":
            high = pd.Series(body["high"], dtype=float)
            low = pd.Series(body["low"], dtype=float)
            close = pd.Series(body["close"], dtype=float)
            result = {"cci": commodity_channel_index(high, low, close, window=int(body.get("window", 20))).fillna("").tolist()}
        elif name == "dmi":
            high = pd.Series(body["high"], dtype=float)
            low = pd.Series(body["low"], dtype=float)
            close = pd.Series(body["close"], dtype=float)
            result = dmi(high, low, close, window=int(body.get("window", 14))).fillna("").to_dict(orient="list")
        else:
            raise ValueError("unsupported indicator")
        self._write_json(200, {"indicator": name, "result": result})

    def _handle_risk_parity(self, body: dict) -> None:
        frame = pd.DataFrame(body["returns"])
        weights = risk_parity_weights(frame).to_dict()
        self._write_json(200, {"weights": weights})

    def _handle_option_greeks(self, body: dict) -> None:
        greeks = black_scholes_greeks(
            option_type=body["option_type"],
            spot=float(body["spot"]),
            strike=float(body["strike"]),
            rate=float(body["rate"]),
            vol=float(body["vol"]),
            maturity=float(body["maturity"]),
        )
        self._write_json(200, {"greeks": greeks})

    def _handle_backtest(self, body: dict) -> None:
        df = _frame_from_payload(body)
        prices = df.pivot(index="date", columns="asset", values="close").sort_index()
        strategy = body["strategy"]
        params = body.get("params", {})

        if strategy == "trend-following":
            weights = trend_following_weights(prices, short_window=int(params.get("short_window", 20)), long_window=int(params.get("long_window", 60)))
        elif strategy == "mean-reversion":
            weights = mean_reversion_weights(prices, lookback=int(params.get("lookback", 10)), top_n=int(params.get("top_n", 3)))
        elif strategy == "smart-beta":
            weights = smart_beta_weights(prices, factor_mode=params.get("factor_mode", "momentum"), lookback=int(params.get("lookback", 20)), top_n=int(params.get("top_n", 5)))
        elif strategy == "market-neutral":
            weights = market_neutral_alpha_weights(prices, lookback=int(params.get("lookback", 20)), factor_mode=params.get("factor_mode", "momentum"))
        elif strategy == "sector-rotation":
            sectors = body.get("sectors", {})
            weights = sector_rotation_weights(prices, sectors=sectors, lookback=int(params.get("lookback", 20)), top_k_sectors=int(params.get("top_k_sectors", 2)))
        else:
            raise ValueError("unsupported strategy")

        result = run_backtest(prices, weights, fee_bps=float(params.get("fee_bps", 5.0)))
        payload = {
            "summary": result["summary"],
            "equity_curve": {str(k.date()): float(v) for k, v in result["equity_curve"].items()},
        }
        self._write_json(200, payload)


def run_server(host: str = "127.0.0.1", port: int = 8010) -> None:
    server = ThreadingHTTPServer((host, port), QuantSkillHandler)
    print(f"quant-skillkit serving on http://{host}:{port}")
    server.serve_forever()
