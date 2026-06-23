# From Book to Skill Kit

This repository does not reproduce the book.

It extracts the practical quant trading ideas and reshapes them into reusable software modules.

## Mapping

`Chapter 4: 常用数据的获取与整理`

- mapped to [quant_skillkit/data.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/data.py)
- covers data cleaning, pivoting, return generation, row normalization

`Chapter 5: 回测平台与风险评价`

- mapped to [quant_skillkit/backtest.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/backtest.py)
- mapped to [quant_skillkit/risk.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/risk.py)
- includes turnover, cost deduction, annualized metrics, drawdown

`Chapter 6.2: 行业轮动`

- mapped to `sector_rotation_weights`
- input: price panel plus asset-to-sector mapping
- output: sector-selection driven portfolio weights

`Chapter 6.3: 市场中性 Alpha`

- mapped to `market_neutral_alpha_weights`
- uses cross-sectional factor scores and neutralizes net exposure

`Chapter 6.5: CTA`

- mapped to `trend_following_weights`
- mapped to `mean_reversion_weights`
- represents two core CTA logic families mentioned in the book

`Chapter 6.6: Smart Beta`

- mapped to `smart_beta_weights`
- mapped to `mean_variance_weights`
- mapped to `risk_parity_weights`

`Chapter 6.7: 技术指标`

- mapped to [quant_skillkit/indicators.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/indicators.py)
- includes `AROON`, `BOLL`, `CCI`, `CMO`, `DMI`

`Chapter 6.8: 资产配置`

- mapped to [quant_skillkit/portfolio.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/portfolio.py)
- includes equal weight, rank weight, mean-variance approximation, risk parity

`Chapter 6.9: 时间序列分析`

- distilled into factor and signal abstractions
- full AR, MA, ARMA, ARIMA implementations are intentionally omitted to keep the toolkit dependency-light

`Chapter 6.10: 组合优化器`

- mapped to `mean_variance_weights`
- kept simple and transparent for GitHub deployment

`Chapter 6.11: 期权 Greeks 与隐含波动率微笑`

- mapped to [quant_skillkit/options.py](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/quant_skillkit/options.py)
- includes Black-Scholes price, Greeks, implied volatility, smile table

## Design choices

- no direct copy of the book's original code
- no mandatory external web framework
- only `numpy` and `pandas` are required
- built for agent invocation as much as for human research
