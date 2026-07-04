# my-new-project
A demonstration project for GitHub repository creation workflow

## Contrarian Cipher B — TradingView Indicator

`contrarian-cipher-b.pine` is a Pine Script v6 indicator that combines the core engine of the latest public **VuManChu Cipher B (Divergences)** with a **contrarian signal layer** that fades crowd extremes.

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

### Disclaimer

This indicator is for educational purposes only and is not financial advice. Contrarian entries fight the prevailing trend by design — always combine with risk management (stops, position sizing) and higher-timeframe context.

Credits: WaveTrend/Cipher B concepts by VuManChu, building on LazyBear's WaveTrend oscillator.
