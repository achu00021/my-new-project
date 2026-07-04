# my-new-project
A demonstration project for GitHub repository creation workflow

## Contrarian Cipher B v2 — TradingView Indicator

`contrarian-cipher-b.pine` is a Pine Script v6 indicator that combines the core engine of the latest public **VuManChu Cipher B (Divergences)** with a **contrarian signal layer** that fades crowd extremes. `contrarian-cipher-b-strategy.pine` is the backtestable strategy version of the same engine, so the winrate can be measured in TradingView's Strategy Tester on any symbol and timeframe.

### v2 quality upgrades (signal quality across all timeframes)

- **Adaptive OB/OS levels** — WaveTrend thresholds are derived from the recent distribution (percentile rank) instead of fixed ±53/±60, so the indicator self-calibrates to any timeframe and asset. A floor prevents over-triggering in dead ranges.
- **Higher-timeframe confirmation** — contrarian longs are blocked while the higher-timeframe WaveTrend is still overbought (and vice versa). Auto mode uses 4× the chart timeframe.
- **ADX trend filter** — signals are suppressed when a strong trend (high ADX with DI direction against the trade) is running them over.
- **Price stretch component** — distance from a 200 EMA measured in ATRs feeds the extremity score, so signals need genuine overextension.
- **Confirmation candle + signal cooldown** — avoids catching falling knives and clustered repeat losses.
- **Winrate tables** — the indicator shows an on-chart table scoring every historical signal N bars after it fired (count, winrate, average return, split by buys/sells); the strategy shows a live performance table (total trades, winrate, long/short breakdown, profit factor, net profit, max drawdown, open position).

### What's inside

**Cipher B core (re-implemented):**

- WaveTrend oscillator (WT1 / WT2 waves + VWAP difference area)
- Money Flow area (RSI-MFI hybrid, green/red area at the top of the pane)
- RSI and Stochastic RSI
- Fractal-based regular divergence detection on WaveTrend (and optionally RSI)
- Classic Cipher B momentum buy/sell circles (WT cross at oversold/overbought)

**Contrarian layer (new):**

- **Crowd Extremity Score (0–100)** — measures how one-sided the market is. Components: WaveTrend at oversold/overbought (and extreme levels), RSI extremes, Stoch RSI extremes, Money Flow extremes, and consecutive candle streaks (capitulation/euphoria).
- **Contrarian Buy** (green triangle) — the crowd is extremely bearish (score ≥ threshold) and WaveTrend crosses up: fade the panic.
- **Contrarian Sell** (red triangle) — the crowd is extremely bullish and WaveTrend crosses down: fade the euphoria.
- **Strong signals** (large triangles + labels) — extremity + recent divergence + extreme WaveTrend level all align.
- **Fade Mode warnings** (yellow diamonds) — a classic momentum signal firing *at an extreme* is treated as a late-crowd warning (e.g. a sell cross at extreme oversold means shorts are late — lean long).
- Background tint whenever the extremity score crosses the threshold.
- Alert conditions for every signal type.

### How to use

1. Open TradingView → Pine Editor → paste the contents of `contrarian-cipher-b.pine` → **Add to chart**.
2. The indicator renders in a separate pane, like Cipher B.
3. Tune the **Contrarian Engine** inputs:
   - `Crowd Extremity Score Threshold` (default 60): higher = fewer, stronger signals.
   - `Require Divergence For Contrarian Signals`: only take fades confirmed by a divergence.
   - `Capitulation / Euphoria Streak`: consecutive candles counted as a crowd extreme.
4. Set alerts from the indicator's built-in alert conditions if you want notifications.

### Reading the signals

| Marker | Meaning |
| --- | --- |
| Small green/red triangle | Contrarian buy / sell (fade the extreme) |
| Large bright triangle + label | Strong contrarian signal (divergence-confirmed) |
| Yellow diamond | Fade-mode warning: late crowd entering at an extreme |
| Green/red circle on the wave | Classic Cipher B momentum signal |
| `Bull Div` / `Bear Div` label | Regular divergence on WaveTrend |

### Backtesting the winrate

1. Paste `contrarian-cipher-b-strategy.pine` into the Pine Editor and add it to the chart.
2. Open the **Strategy Tester** tab and check *Percent Profitable* and *Profit Factor* for your symbol/timeframe.
3. To push winrate up: raise the `Crowd Extremity Score Threshold`, enable `Require Divergence For Signals`, and keep `Exit When WaveTrend Reverts To Zero` on (mean-reversion exits close winners early and often).
4. Winrate alone is not profitability — a high winrate with oversized losses still loses money. Always evaluate Profit Factor and max drawdown alongside it.

### Disclaimer

This indicator is for educational purposes only and is not financial advice. Contrarian entries fight the prevailing trend by design — always combine with risk management (stops, position sizing) and higher-timeframe context.

Credits: WaveTrend/Cipher B concepts by VuManChu, building on LazyBear's WaveTrend oscillator.
