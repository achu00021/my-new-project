# my-new-project
A demonstration project for GitHub repository creation workflow

## Contrarian Reversal Pro (TradingView indicator)

`contrarian-reversal-indicator.pine` is a Pine Script v6 contrarian (mean-reversion) indicator with BUY/SELL signals, alerts, and an on-chart win-rate table.

**How to load it:**
1. Open [TradingView](https://www.tradingview.com/) and open any chart.
2. Open the **Pine Editor** (bottom panel).
3. Delete the default code, paste the full contents of `contrarian-reversal-indicator.pine`, and click **Add to chart**.

**How it works:** it fades crowd extremes, but only after confirmation — a composite exhaustion score (RSI + Stochastic + CCI + Bollinger %B) must hit an extreme while price pierces the Bollinger Band, and the signal fires only when price closes back inside the band with a reversal candle. A 200 EMA trend filter (on by default), optional volume-spike filter, and a signal cooldown further raise signal quality. The table in the top-right shows the historical win rate of the signals on the current chart so you can tune the settings per symbol and timeframe.
