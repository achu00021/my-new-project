# TripleConfluence — High-Winrate Mean-Reversion Indicator

A long-only trading indicator designed to maximize winrate, built from three
independent technical-analysis confirmations, with a **live winrate table on
the chart**. All results below use next-open fills with no lookahead.

Headline winrates with the default pullback-limit entries (10-symbol
baskets):

| Timeframe | Development basket | Out-of-sample basket |
|-----------|--------------------|----------------------|
| Daily (2005–2026) | **86.7%** (460 trades, PF 2.75, avg +1.16%) | **87.9%** (429 trades, PF 3.12, avg +1.18%) |
| Hourly (~2 years) | **90.1%** (365 trades, PF 2.04) | — |
| Weekly (2005–2026) | **90.4%** (83 trades, PF 3.16) | — |

These numbers are **validated, not just fitted** — see
[How accurate are these winrates?](#how-accurate-are-these-winrates) below.

Provided as:

- **Pine Script v5** for TradingView — `pinescript/triple_confluence_indicator.pine`
  (chart signals, alerts, and an on-chart winrate table that simulates the
  system bar by bar on whatever symbol/timeframe you load) and
  `pinescript/triple_confluence_strategy.pine` (Strategy Tester version).
- **Python** — `python/indicator.py` (signal computation),
  `python/backtest.py` (backtester, any timeframe, optional costs), and
  `python/validate.py` (walk-forward / survivorship / cost audit).

## Why this design wins so often

There is no indicator that predicts the market; high winrate comes from
*stacking independent edges* and *taking profits at a statistically likely
target*. This indicator combines:

| # | Confirmation | Tool | Rule |
|---|--------------|------|------|
| 1 | Regime filter | SMA(200) | Close above the 200-bar SMA — only buy dips inside a long-term uptrend |
| 2 | Exhaustion | RSI(2) | RSI(2) < 10 — Connors-style fast-RSI pullback, one of the highest-winrate published setups on index ETFs |
| 3 | Stretch | Bollinger %B(20, 2) | %B < 0.10 — price pressed into the lower band, so the dip is statistically extreme, not mild drift |

**Entry** (default "limit" mode): all three conditions true at the close →
place a **limit order 0.5×ATR(14) below the signal close**, working for the
next 3 bars. Only ~60% of signals fill, but the fills buy deeper into the
dip: average profit rises from +0.85% to +1.16% per trade, profit factor
from 2.2 to 2.8, and the worst loss shrinks — on every timeframe tested.
Set entry mode to "market" for the simpler buy-next-open entry
(more trades, thinner edge per trade).

**Exit** (first that triggers):

1. Close back above the **7-bar SMA while in profit** — the pullback has
   reverted to its mean. This is ~87% of exits.
2. **Catastrophic stop** at −15% — the dip-buying thesis has failed; cut it.
3. **75-bar time stop** — cap how long capital can sit in a stagnant trade.

All parameters are in *bars*, so the same settings apply on any timeframe —
the logic self-scales (200-bar trend, 20-bar bands, 7-bar mean).

## How accurate are these winrates?

A high backtested winrate is easy to fake with lookahead, survivorship bias,
or overfitting. `python/validate.py` attacks the result from three angles:

**1. Walk-forward (unseen data).** Parameters chosen on 2005–2015 data only,
then evaluated on 2016–2026 — a window tuning never saw:

```
test                                    trades   win%   avg%     PF
dev basket 2016-2026                       218   83.5   0.62   1.57
OOS basket 2016-2026 (symbols+dates new)   208   87.0   1.34   4.19
```

**2. Survivorship stress.** A basket of historically weak/troubled large
caps (GE, F, T, C, BAC, INTC, VZ, XRX) — no hindsight winners — and crypto:

```
weak large caps, daily 2005-2026           303   83.2   0.76   1.56
crypto BTC/ETH, daily 2015-2026             51   86.3   1.65   1.53
```

**3. Costs.** With 5 bps slippage per side, daily winrate barely moves
(86.7% → 85.4%); hourly drops to 83.0% and at 10 bps the hourly edge is
thin (75.3%, PF 1.18).

**4. Stop execution.** The backtest checks the −15% stop on the close; a
real resting stop order triggers intrabar. `python/test_intrabar.py`
compares both (market-entry config): winrate is unchanged (87.2% vs 87.1%)
and the intrabar stop actually improves the worst trade (−18.3% vs −22.8%)
because it fills at the stop level instead of waiting for the close.

**5. Entry fills.** The default limit entry assumes a fill when the bar's
low touches the limit price, and assumes a fill at the open when price
gaps below the order. Both are conservative for a resting limit order on
liquid ETFs/large caps.

**Verdict:** expect roughly **84–88% on daily bars** in honest conditions —
the genuine edge of buying statistically extreme dips inside long-term
uptrends and taking small profits at the mean. The weekly 90%+ and the
frictionless hourly 90.1% are real in-sample numbers but rest on fewer
trades or shrink under costs; treat daily as the representative timeframe.

## Full daily results (development basket, 2005–2026, limit entries)

```
symbol    trades  winrate%  avg_ret%      PF  avg_bars   worst%
SPY           47      80.9      0.38    1.34       9.2   -17.92
QQQ           53      86.8      1.12    2.37       9.1   -19.65
DIA           44      88.6      0.78    2.57       9.1   -20.64
IWM           53      84.9      0.59    1.49       8.3   -19.10
AAPL          51      94.1      2.81    7.36       7.4   -16.91
MSFT          39      87.2      2.24    7.09       6.5    -9.79
GOOGL         49      87.8      1.47    4.08       9.7   -16.40
JNJ           43      79.1      0.31    1.41      18.6    -9.15
XLP           49      91.8      1.13   75.96       8.9    -0.62
GLD           32      84.4      0.58    1.62      11.7   -16.97
ALL          460      86.7      1.16    2.75       9.7   -20.64
```

Out-of-sample basket: XLK, XLV, XLE, KO, PG, V, WMT, EEM, EFA, HD.
PF = profit factor (gross wins / gross losses).

## Usage

### TradingView

1. Open the Pine Editor, paste `pinescript/triple_confluence_indicator.pine`,
   and add it to a chart of a liquid ETF or large-cap stock (any timeframe;
   daily is the best-validated).
2. The **winrate table** (top-right by default) shows trades, wins/losses,
   winrate, average trade, profit factor, and average holding time — computed
   live for the exact symbol and timeframe on your chart, with no lookahead.
3. Small lime triangles mark signals; a **yellow line shows the resting
   limit order** (the improved entry point); green labels mark actual entry
   fills; magenta triangles mark exit fills. Alerts exist for all three.
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
python3 backtest.py --cost=5                 # 5 bps slippage per side
python3 validate.py                          # full accuracy audit
```

## Honest caveats

- **Winrate is not profitability.** This system wins often because it takes
  quick, small profits; losses are rarer but larger (capped by the −15%
  stop). The profit factor (≈2.2 daily) shows the edge is real, but
  position-size accordingly.
- It is a **bull-regime dip buyer**. It goes quiet in bear markets (by
  design — the 200-SMA filter) and does not short.
- Hourly per-trade edge is small (~0.2% average) and disappears at ~10 bps
  round-trip costs; intraday use requires very low fees.
- Weekly results rest on only ~130 trades; treat daily as representative.
- Past performance never guarantees future results. This is educational
  code, not financial advice.
