# ICT Contrarian RSI Fib — TradingView Indicator

A Pine Script v5 overlay indicator combining **ICT concepts**, **contrarian entries**, **RSI**, and **Fibonacci retracement**, with built-in position sizing for a **$1,000 account**, **3% risk per trade**, and **15x leverage**.

## Quick Start

1. Open [TradingView](https://www.tradingview.com/chart/)
2. Open **Pine Editor** (bottom panel)
3. Copy the contents of [`indicators/ICT_Contrarian_RSI_Fib.pine`](indicators/ICT_Contrarian_RSI_Fib.pine)
4. Click **Add to chart**

## What It Does

### ICT (Inner Circle Trader)
- **Swing structure** — tracks higher lows / lower highs
- **Premium / Discount zones** — equilibrium at the 50% Fib level
- **Liquidity sweeps** — wick beyond swing high/low then close back inside
- **Order blocks** — last opposing candle before impulsive move
- **Fair Value Gaps (FVG)** — imbalance zones

### Contrarian Logic
- Fades liquidity grabs: after a **bull sweep** (stop hunt below lows), looks for longs; after a **bear sweep**, looks for shorts
- Works with RSI extremes to enter against exhausted moves at key levels

### RSI
- Configurable length and overbought/oversold thresholds
- Optional **RSI divergence** requirement for higher-quality setups

### Fibonacci Retracement
- Auto-drawn from the most recent swing leg
- Highlights the **golden pocket** (61.8%–78.6%)
- Key levels: 23.6%, 38.2%, 50%, 61.8%, 78.6%

### Risk Management (defaults)
| Setting | Default |
|---------|---------|
| Account | $1,000 |
| Risk per trade | 3% ($30) |
| Leverage | 15x ($15,000 max notional) |
| Reward:Risk | 2:1 |
| Stop | 1.2× ATR |

Each signal label shows **entry**, **stop loss**, **take profit**, **position size**, and **margin required**.

## High Win Rate Design

Signals only fire when multiple factors align (confluence scoring). Default **minimum score: 4/6**:

1. **Premium/Discount** — longs in discount, shorts in premium
2. **RSI / Contrarian** — oversold/overbought or sweep fade
3. **Fib Golden Pocket** — price at 61.8%–78.6% retracement
4. **Liquidity Sweep** — stop hunt confirmed
5. **Order Block / FVG** — price at institutional zone
6. **Structure + Divergence** — trend alignment and optional RSI div

**Tips for higher win rate:**
- Keep `Min Confluence Score` at **5–6** for fewer, higher-quality signals
- Enable `Require RSI Divergence` and `Require Liquidity Sweep`
- Use on **15m–1H** timeframes for crypto/forex
- Trade only in the direction of higher-timeframe structure

## Alerts

Create alerts in TradingView for:
- **ICT Long Entry**
- **ICT Short Entry**

## Disclaimer

This indicator is for educational purposes only. Past performance does not guarantee future results. Always paper-trade and verify signals before risking real capital. High leverage (15x) amplifies both gains and losses.
