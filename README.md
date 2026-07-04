# TripleConfluence — High-Winrate Mean-Reversion Indicator

A long-only trading indicator designed to maximize winrate, built from three
independent technical-analysis confirmations, with a **live winrate table on
the chart**. Backtested winrate (10-symbol baskets, next-open fills, no
lookahead):

| Timeframe | Development basket | Out-of-sample basket |
|-----------|--------------------|----------------------|
| Daily (2005–2026) | **87.5%** (696 trades, PF 3.56) | **86.4%** (676 trades, PF 4.17) |
| Hourly (~2 years) | **88.5%** (549 trades, PF 1.63) | **87.1%** (487 trades, PF 1.58) |
| Weekly (2005–2026) | **93.8%** (130 trades, PF 24.5) | **96.2%** (130 trades, PF 18.2) |

Provided as:

- **Pine Script v5** for TradingView — `pinescript/triple_confluence_indicator.pine`
  (chart signals, alerts, and an on-chart winrate table that simulates the
  system bar by bar on whatever symbol/timeframe you load) and
  `pinescript/triple_confluence_strategy.pine` (Strategy Tester version).
- **Python** — `python/indicator.py` (signal computation) and
  `python/backtest.py` (backtester on real data via yfinance, any timeframe).

## Why this design wins so often

There is no indicator that predicts the market; high winrate comes from
*stacking independent edges* and *taking profits at a statistically likely
target*. This indicator combines:

| # | Confirmation | Tool | Rule |
|---|--------------|------|------|
| 1 | Regime filter | SMA(200) | Close above the 200-bar SMA — only buy dips inside a long-term uptrend |
| 2 | Exhaustion | RSI(2) | RSI(2) < 10 — Connors-style fast-RSI pullback, one of the highest-winrate published setups on index ETFs |
| 3 | Stretch | Bollinger %B(20, 2) | %B < 0.10 — price pressed into the lower band, so the dip is statistically extreme, not mild drift |

**Entry**: all three conditions true at the close → buy next bar's open.

**Exit**: close back above the **7-bar SMA while in profit** (the pullback
has reverted to its mean), or a **75-bar time stop**. Requiring profit at
the mean-reversion exit, plus a patient time stop that gives the trade room
to recover inside an intact uptrend, is what lifts the winrate to 85–95%
on every timeframe tested.

All parameters are in *bars*, so the same settings apply on any timeframe —
the logic self-scales (200-bar trend, 20-bar bands, 7-bar mean).

## Backtest results (next-open fills, no lookahead)

Development basket — SPY, QQQ, DIA, IWM, AAPL, MSFT, GOOGL, JNJ, XLP, GLD.
Daily, 2005–2026:

```
symbol    trades  winrate%  avg_ret%      PF  avg_bars   worst%
SPY           73      87.7      1.12   10.13      10.2    -6.19
QQQ           80      83.8      1.29    6.29       9.0    -8.83
DIA           73      91.8      1.09   10.04       8.6    -7.25
IWM           70      85.7      0.80    2.26      11.9   -14.52
AAPL          74      90.5      1.81    3.46       9.4   -24.12
MSFT          61      90.2      1.23    2.44      10.0   -18.43
GOOGL         72      88.9      1.61    4.34      12.2   -16.04
JNJ           56      83.9      0.37    1.62      16.4    -9.41
XLP           78      85.9      0.93   24.98       8.1    -1.05
GLD           59      86.4      0.57    1.78      12.3   -20.45
ALL          696      87.5      1.11    3.56      10.6   -24.12
```

Hourly (max yfinance history, ~730 days): **88.5%** over 549 trades.
Weekly (2005–2026): **93.8%** over 130 trades.

Out-of-sample basket (XLK, XLV, XLE, KO, PG, V, WMT, EEM, EFA, HD — never
used during tuning): daily **86.4%** / 676 trades, hourly **87.1%** / 487
trades, weekly **96.2%** / 130 trades.

PF = profit factor (gross wins / gross losses).

## Usage

### TradingView

1. Open the Pine Editor, paste `pinescript/triple_confluence_indicator.pine`,
   and add it to a chart of a liquid ETF or large-cap stock (any timeframe;
   daily/hourly/weekly are the tested ones).
2. The **winrate table** (top-right by default) shows trades, wins/losses,
   winrate, average trade, profit factor, and average holding time — computed
   live for the exact symbol and timeframe on your chart, using next-open
   fills with no lookahead.
3. Green triangles mark BUY signals; magenta triangles mark exit fills.
   Alerts are included for both.
4. `pinescript/triple_confluence_strategy.pine` runs the same system in the
   Strategy Tester for full equity-curve statistics.

### Python

```bash
cd python
pip install -r requirements.txt
python3 backtest.py                          # default 10-symbol basket, daily
python3 backtest.py SPY QQQ TSLA             # any symbols
python3 backtest.py --interval=1h            # hourly
python3 backtest.py --interval=1wk SPY QQQ   # weekly
```

## Honest caveats

- **Winrate is not profitability.** This system wins often because it takes
  quick, small profits and lets the occasional loser run to a time stop —
  the worst single trade in the daily test was −24%. The profit factor
  (3.5 daily) shows the edge is real, but position-size accordingly.
- It is a **bull-regime dip buyer**. It goes quiet in bear markets (by
  design — the 200-SMA filter) and does not short.
- Hourly per-trade edge is small (~0.2% average); commissions and slippage
  matter much more intraday than on daily/weekly bars.
- Weekly results look spectacular but rest on only ~130 trades with long
  holding periods — treat the daily numbers as the most representative.
- Past performance never guarantees future results. This is educational
  code, not financial advice.
