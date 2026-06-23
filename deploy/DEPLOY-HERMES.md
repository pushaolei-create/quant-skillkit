# Deploy to Hermes

## Goal

This folder turns `quant-skillkit` into a deployable service for `hermes`.

You only need to do three things:

1. start the local quant service
2. export or fetch the tool manifest
3. point `hermes` at the service

## 1. Start the service

From PowerShell:

```powershell
.\deploy\start-quant-skillkit.ps1
```

If you want a custom host or port:

```powershell
.\deploy\start-quant-skillkit.ps1 -HostName 0.0.0.0 -Port 8010
```

## 2. Export the Hermes manifest

```powershell
.\deploy\export-hermes-manifest.ps1
```

This writes:

- `deploy/hermes-tool-manifest.generated.json`

You can also set a custom base URL:

```powershell
.\deploy\export-hermes-manifest.ps1 -BaseUrl http://127.0.0.1:8010
```

## 3. Configure Hermes

Use:

- [deploy/hermes-config.template.json](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/deploy/hermes-config.template.json)
- [deploy/hermes-tool-manifest.generated.json](/C:/Users/Administrator/Documents/Codex/2026-06-23/new-chat/outputs/quant-skillkit/deploy/hermes-tool-manifest.generated.json)

At minimum, `hermes` needs:

- base URL: `http://127.0.0.1:8010`
- health endpoint: `/health`
- tools endpoint: `/tools`

## Tools exposed to Hermes

- `quant.indicator.boll`
- `quant.indicator.dmi`
- `quant.portfolio.risk_parity`
- `quant.options.greeks`
- `quant.strategy.backtest`

## Recommended deployment pattern

- Keep `quant-skillkit` as the research and signal layer
- Let `hermes` call it for indicators, backtests, allocation, and option analytics
- Keep brokerage execution in a separate service if you later go live

## Quick verification

After starting the service:

```powershell
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/tools
```

If both endpoints respond, Hermes can integrate against the service.
