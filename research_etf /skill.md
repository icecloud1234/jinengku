# ETF Research Skill

This skill performs research on ETFs or stocks.

Capabilities:
- download historical price data
- calculate annual return
- calculate volatility
- calculate max drawdown
- generate price charts
- produce an investment report

Rules:

1. Never use simulated or fake data
2. If data download fails, retry up to 3 times
3. Validate dataset size before analysis
4. If all sources fail, report failure

Example usage:

research VXUS

research VTI

research AAPL

## Execution

Use python-runner to execute research.py
