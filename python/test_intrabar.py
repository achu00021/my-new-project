"""Close-based stop vs a real intrabar stop order at -15%."""

import numpy as np
import pandas as pd
import yfinance as yf

from backtest import DEFAULT_SYMBOLS, START, Trade, stats
from indicator import Params, compute_signals


def fetch(syms):
    out = {}
    for sym in syms:
        df = yf.download(sym, interval="1d", start=START, auto_adjust=True, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        out[sym] = df
    return out


def run(df, p, intrabar):
    df = compute_signals(df, p)
    opens = df["Open"].to_numpy()
    lows = df["Low"].to_numpy()
    closes = df["Close"].to_numpy()
    sma_exit = df["sma_exit"].to_numpy()
    buy = df["buy_signal"].to_numpy()
    dates = df.index

    trades = []
    in_pos = False
    entry_i, entry_px = -1, np.nan
    n = len(df)
    for i in range(n - 1):
        if not in_pos:
            if buy[i]:
                in_pos, entry_i, entry_px = True, i + 1, opens[i + 1]
        else:
            stop_px = entry_px * (1 - p.stop_pct)
            if intrabar and i >= entry_i and lows[i] <= stop_px:
                # stop order fills at the stop price (or worse on a gap open)
                fill = min(stop_px, opens[i]) if i > entry_i else min(stop_px, entry_px)
                trades.append(Trade(dates[entry_i], dates[i], entry_px, fill, i - entry_i))
                in_pos = False
                continue
            bars_held = i - entry_i
            take = closes[i] > sma_exit[i] and closes[i] > entry_px
            stop = bars_held >= p.time_stop or (not intrabar and closes[i] < stop_px)
            if i >= entry_i and (take or stop):
                trades.append(Trade(dates[entry_i], dates[i + 1], entry_px, opens[i + 1], bars_held + 1))
                in_pos = False
    return trades


data = fetch(DEFAULT_SYMBOLS)
p = Params()
print(f"{'stop model':<28}{'trades':>7}{'win%':>8}{'avg%':>8}{'PF':>7}{'worst%':>9}")
for name, intrabar in [("close-based (backtest)", False), ("intrabar stop order", True)]:
    trades = []
    for df in data.values():
        trades.extend(run(df, p, intrabar))
    s = stats(trades)
    print(f"{name:<28}{s['trades']:>7}{s['winrate']:>8.1f}{s['avg_ret']:>8.2f}"
          f"{s['profit_factor']:>7.2f}{s['worst']:>9.2f}")
