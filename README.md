# TripleConfluence — High-Winrate Mean-Reversion Indicator

A long-only trading indicator designed to maximize winrate, built from three
independent technical-analysis confirmations. Backtested winrate:
**84.4% over 698 trades** (2005–2026, 10-symbol daily basket) and **83.4%
over 676 trades** on a fully out-of-sample basket of 10 different symbols.

Provided as:

- **Pine Script v5** for TradingView — `pinescript/triple_confluence_indicator.pine`
  (chart signals + alerts) and `pinescript/triple_confluence_strategy.pine`
  (Strategy Tester version so you can verify the winrate yourself).
- **Python** — `python/indicator.py` (signal computation) and
  `python/backtest.py` (backtester on real data via yfinance).

## Why this design wins so often

There is no indicator that predicts the market; high winrate comes from
*stacking independent edges* and *taking profits at a statistically likely
target*. This indicator combines:

| # | Confirmation | Tool | Rule |
|---|--------------|------|------|
| 1 | Regime filter | SMA(200) | Close above the 200-day SMA — only buy dips inside a long-term uptrend |
| 2 | Exhaustion | RSI(2) | RSI(2) < 10 — Connors-style fast-RSI pullback, one of the highest-winrate published setups on index ETFs |
| 3 | Stretch | Bollinger %B(20, 2) | %B < 0.10 — price pressed into the lower band, so the dip is statistically extreme, not mild drift |

**Entry**: all three conditions true at the close → buy next bar's open.

**Exit**: close back above the **7-day SMA while in profit** (the pullback
has reverted to its mean), or a **30-bar time stop**. Requiring profit at
the mean-reversion exit is what lifts the winrate above 80% — most dips
inside an uptrend resolve upward within a few bars.

## Backtest results (daily bars, next-open fills, no lookahead)

Development basket, 2005–2026:

```
symbol    trades  winrate%  avg_ret%      PF  avg_bars   worst%
SPY           73      83.6      0.37    1.44       7.7   -17.12
QQQ           80      81.2      0.87    2.34       7.0   -11.89
DIA           73      90.4      0.78    2.84       7.5   -18.15
IWM           70      82.9      0.27    1.23       8.1   -22.07
AAPL          74      89.2      1.27    2.03       7.3   -30.46
MSFT          61      88.5      1.45    3.51       7.3   -11.48
GOOGL         73      83.6      0.73    1.54       8.8   -21.58
JNJ           57      75.4     -0.03    0.97      10.6   -11.02
XLP           78      82.1      0.78    5.70       7.4    -4.83
GLD           59      86.4      0.89    3.14       9.2   -15.83
ALL          698      84.4      0.74    1.96       8.0   -30.46
```

Out-of-sample basket (symbols never used during tuning):

```
symbol    trades  winrate%  avg_ret%      PF  avg_bars   worst%
XLK / XLV / XLE / KO / PG / V / WMT / EEM / EFA / HD
ALL          676      83.4      0.76    2.26       8.0   -19.30
```

PF = profit factor (gross wins / gross losses).

## Usage

### TradingView

1. Open the Pine Editor, paste `pinescript/triple_confluence_indicator.pine`,
   and add it to a **daily** chart of a liquid ETF or large-cap stock.
2. Green triangles mark BUY signals; small magenta triangles mark where
   price reverts to the short mean (exit zone). Alerts are included for both.
3. To see the winrate stats, load `pinescript/triple_confluence_strategy.pine`
   in the Strategy Tester instead.

### Python

```bash
cd python
pip install -r requirements.txt
python3 backtest.py                # default 10-symbol basket
python3 backtest.py SPY QQQ TSLA   # any symbols you like
```

## Honest caveats

- **Winrate is not profitability.** This system wins often because it takes
  quick, small profits and lets the occasional loser run to a time stop —
  the worst single trade in the test was −30%. The profit factor (≈2)
  shows the edge is real, but position-size accordingly.
- It is a **bull-regime dip buyer**. It goes quiet in bear markets (by
  design — the 200-SMA filter) and does not short.
- Results are from daily bars on liquid equities/ETFs with next-open fills
  and no commissions/slippage. Intraday timeframes, illiquid tickers, or
  heavy fees will change the numbers.
- Past performance never guarantees future results. This is educational
  code, not financial advice.
