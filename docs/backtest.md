# 30-Day Replay & DGCA Backtest

## 1. Backtest Design
To prove reproducible index performance without volatile network calls during evaluation:
- 30 daily dated snapshots are maintained in `data/replay-30d/`.
- Replaying these snapshots executes the exact cleaning, deduplication, imputation, and index engine logic.
- Output series are validated against historical DGCA quarterly average fare trends.

## 2. Sensitivity Analysis
- Evaluates headline stability under $\pm 20\%$ horizon weight shifts.
- Measures volatility under route exclusion scenarios.

