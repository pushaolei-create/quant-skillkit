# quant-skillkit

`quant-skillkit` is a lightweight Python toolkit for turning practical quant trading ideas into reusable research and agent-facing tools.

`quant-skillkit` 是一个轻量级 Python 工具包，用来把量化交易中的实战思路整理成可复用的研究模块和可供智能体调用的能力接口。

It was inspired by the hands-on quant sections of *Python 与量化投资：从基础到实战*, but this repository does not reproduce the book's original code or text. Instead, it reshapes the underlying ideas into a clean, dependency-light package that is easier to run, extend, and deploy.

它受到《Python 与量化投资：从基础到实战》中量化实战部分的启发，但并不复刻书中的原始代码或原文，而是把核心思想重新整理成一个更干净、依赖更少、也更方便运行、扩展和部署的工具包。

## Why this project exists | 为什么做这个项目

A lot of quant learning material stops at notebooks or platform-specific demos. This project is for the next step:

很多量化学习资料停留在 notebook 示例或者平台专用脚本这一步，而这个项目解决的是“下一步怎么复用”的问题：

- reusable quant research components instead of one-off examples
- built-in strategy templates for fast experimentation
- simple CLI workflows for local analysis
- HTTP endpoints and tool manifests for agent integration
- 把一次性的示例代码整理成可复用的量化研究组件
- 提供内置策略模板，方便快速实验
- 提供简洁的 CLI 工作流，适合本地分析
- 提供 HTTP 接口和工具清单，方便接入智能体

If you want a compact bridge between quant research, backtesting, and agent tooling, this repo is built for that.

如果你希望在“量化研究、回测验证、智能体调用”之间搭一座轻量级桥梁，这个仓库就是为这个目标设计的。

## Core capabilities | 核心能力

- Data preparation: tidy price loading, cleaning, pivoting, return generation
- Indicators: `AROON`, `BOLL`, `CCI`, `CMO`, `DMI`
- Factor helpers: winsorization, z-score, momentum, mean reversion
- Strategy templates: sector rotation, trend following, mean reversion, smart beta, market neutral alpha
- Portfolio construction: rank weighting, mean-variance approximation, risk parity
- Backtesting: turnover-aware backtest engine with transaction cost support
- Risk analytics: annual return, Sharpe, drawdown, Calmar, win rate
- Options utilities: Black-Scholes price, Greeks, implied volatility, volatility smile
- Agent integration: stdlib HTTP API, Hermes manifest generator, `/tools` discovery endpoint
- 数据准备：价格数据读取、清洗、透视转换、收益率生成
- 技术指标：`AROON`、`BOLL`、`CCI`、`CMO`、`DMI`
- 因子辅助：去极值、标准化、动量、均值回归
- 策略模板：行业轮动、趋势跟随、均值回归、Smart Beta、市场中性 Alpha
- 组合构建：排序加权、均值方差近似、风险平价
- 回测引擎：支持换手率和交易成本的轻量回测
- 风险分析：年化收益、夏普、回撤、Calmar、胜率
- 期权工具：Black-Scholes 定价、Greeks、隐含波动率、波动率微笑
- 智能体集成：标准库 HTTP API、Hermes manifest 生成器、`/tools` 发现接口

## Installation | 安装

```bash
git clone https://github.com/pushaolei-create/quant-skillkit.git
cd quant-skillkit
python -m pip install -e .
```

Dependencies are intentionally minimal:

项目依赖刻意保持在最小范围：

- `numpy`
- `pandas`

## Quick start | 快速开始

Run a sample backtest:

运行一个示例回测：

```bash
python -m quant_skillkit.cli backtest --input examples/sample_prices.csv --strategy smart-beta --lookback 3 --top-n 2
```

Generate a Hermes-friendly manifest:

生成适合 Hermes 接入的 manifest：

```bash
python -m quant_skillkit.cli manifest --base-url http://127.0.0.1:8010
```

Start the local API service:

启动本地 API 服务：

```bash
python -m quant_skillkit.cli serve --host 127.0.0.1 --port 8010
```

Calculate an indicator from sample data:

用示例数据计算技术指标：

```bash
python -m quant_skillkit.cli indicators --input examples/sample_prices.csv --indicator boll
```

## Input format | 输入格式

The default input is a tidy CSV:

默认输入采用 tidy CSV 结构：

```text
date,asset,close,high,low,sector
2026-01-01,AAA,10.1,10.3,9.9,Tech
2026-01-01,BBB,8.2,8.4,8.0,Finance
```

Required columns for most workflows:

大多数功能至少需要这些列：

- `date`
- `asset`
- `close`

Useful optional columns:

这些可选列在部分策略或指标中会有帮助：

- `high`
- `low`
- `sector`

## Hermes integration | Hermes 接入

Start the service:

先启动本地服务：

```bash
python -m quant_skillkit.cli serve --host 0.0.0.0 --port 8010
```

Available endpoints:

可用接口如下：

- `GET /health`
- `GET /tools`
- `POST /indicators/{name}`
- `POST /portfolio/risk-parity`
- `POST /options/greeks`
- `POST /strategy/backtest`

Useful integration files:

与接入相关的文件：

- [examples/hermes_tool_manifest.json](examples/hermes_tool_manifest.json)
- [quant_skillkit/hermes_adapter.py](quant_skillkit/hermes_adapter.py)
- [docs/hermes-integration.md](docs/hermes-integration.md)
- [deploy/DEPLOY-HERMES.md](deploy/DEPLOY-HERMES.md)
- [deploy/hermes-config.template.json](deploy/hermes-config.template.json)

## Project structure | 项目结构

- [quant_skillkit](quant_skillkit)
- [docs/book-to-skillkit.md](docs/book-to-skillkit.md)
- [docs/hermes-integration.md](docs/hermes-integration.md)
- [deploy/DEPLOY-HERMES.md](deploy/DEPLOY-HERMES.md)
- [deploy/hermes-config.template.json](deploy/hermes-config.template.json)
- [examples](examples)
- [tests](tests)

## Validation | 验证

Run tests:

运行测试：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Notes | 说明

- This repo is a research toolkit, not a production execution engine.
- Backtest results are template-grade and should not be treated as live trading evidence.
- If you later need broker connectivity or production orchestration, it is better to keep this project as the research and signal layer.
- 这个仓库是研究工具包，不是生产级交易执行系统。
- 回测结果适合研究和验证，不应直接视为真实交易表现。
- 如果后续需要接券商、实盘执行或调度系统，建议把这个项目保留在“研究与信号层”。
