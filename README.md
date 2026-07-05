# TripleConfluence — High-Winrate Mean-Reversion Indicator

A long-only trading indicator designed to maximize winrate, built from three
independent technical-analysis confirmations, with a **live winrate table on
the chart**. All results below use next-open fills with no lookahead.

Headline winrates (10-symbol baskets):

| Timeframe | Development basket | Out-of-sample basket |
|-----------|--------------------|----------------------|
| Daily (2005–2026) | **87.1%** (696 trades, PF 2.23) | **86.2%** (676 trades, PF 2.74) |
| Hourly (~2 years) | **88.5%** (549 trades, PF 1.63) | **87.1%** (487 trades, PF 1.58) |
| Weekly (2005–2026) | **87.0%** (131 trades, PF 2.84) | **92.3%** (130 trades, PF 4.97) |

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

**Entry**: all three conditions true at the close → buy next bar's open.

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
dev basket 2016-2026                       329   84.2   0.48   1.49
OOS basket 2016-2026 (symbols+dates new)   323   84.8   0.91   2.92
```

**2. Survivorship stress.** A basket of historically weak/troubled large
caps (GE, F, T, C, BAC, INTC, VZ, XRX) — no hindsight winners — and crypto:

```
weak large caps, daily 2005-2026           436   84.4   0.84   1.77
crypto BTC/ETH, daily 2015-2026             81   86.4   1.14   1.40
```

**3. Costs.** With 5 bps slippage per side, daily winrate barely moves
(87.1% → 86.2%); hourly drops to 81.3% and at 10 bps the hourly edge is
roughly break-even.

**Verdict:** expect roughly **84–87% on daily bars** in honest conditions —
the genuine edge of buying statistically extreme dips inside long-term
uptrends and taking small profits at the mean. The weekly 92%+ and the
frictionless hourly 88.5% are real in-sample numbers but rest on fewer
trades or vanish under costs; treat daily as the representative timeframe.

## Full daily results (development basket, 2005–2026)

```
symbol    trades  winrate%  avg_ret%      PF  avg_bars   worst%
SPY           73      86.3      0.57    1.86       8.4   -17.83
QQQ           80      82.5      0.95    2.65       8.4   -20.61
DIA           73      90.4      0.89    3.79       7.7   -21.47
IWM           70      85.7      0.26    1.22       8.6   -20.15
AAPL          74      89.2      1.34    2.16       7.3   -22.76
MSFT          61      91.8      1.26    2.53       9.5   -16.58
GOOGL         72      87.5      1.12    2.16       9.5   -18.18
JNJ           56      83.9      0.37    1.62      16.4    -9.41
XLP           78      87.2      0.93   24.98       8.1    -1.05
GLD           59      86.4      0.65    2.00      11.5   -15.56
ALL          696      87.1      0.85    2.23       9.3   -22.76
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
