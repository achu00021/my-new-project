"""
Backtest the TripleConfluence indicator on real daily data (via yfinance)
and report winrate, profit factor, and other stats per symbol.

Usage:
    python3 backtest.py                          # default basket, daily
    python3 backtest.py SPY QQQ AAPL             # custom symbols, daily
    python3 backtest.py --interval=1h            # hourly (max ~730 days)
    python3 backtest.py --interval=1wk SPY QQQ   # weekly
    python3 backtest.py --cost=5                 # 5 bps slippage per side

Execution model (conservative, no lookahead):
  - Signals are computed on bar close.
  - Entries and exits fill on the NEXT bar's open.
  - One position at a time, long only.
"""

import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
import yfinance as yf

from indicator import Params, compute_signals

DEFAULT_SYMBOLS = ["SPY", "QQQ", "DIA", "IWM", "AAPL", "MSFT", "GOOGL", "JNJ", "XLP", "GLD"]
START = "2005-01-01"


@dataclass
class Trade:
    entry_date: pd.Timestamp
    exit_date: pd.Timestamp
    entry: float
    exit: float
    bars_held: int

    @property
    def ret(self) -> float:
        return self.exit / self.entry - 1.0


def run_backtest(df: pd.DataFrame, p: Params = Params(),
                 cost_bps: float = 0.0) -> list[Trade]:
    df = compute_signals(df, p)
    opens = df["Open"].to_numpy()
    closes = df["Close"].to_numpy()
    buy = df["buy_signal"].to_numpy()
    above_mean = df["above_mean"].to_numpy()
    dates = df.index
    cost = cost_bps / 10000.0

    trades: list[Trade] = []
    in_pos = False
    entry_i = -1
    entry_px = np.nan

    n = len(df)
    for i in range(n - 1):
        if not in_pos:
            if buy[i]:
                in_pos = True
                entry_i = i + 1                # fill next open
                entry_px = opens[i + 1] * (1 + cost)
        else:
            bars_held = i - entry_i
            # Exit when the pullback has reverted (close above the short
            # mean) AND the trade is in profit; bail on the time stop or
            # the catastrophic stop (the trade thesis has failed).
            take = above_mean[i] and closes[i] > entry_px
            stop = bars_held >= p.time_stop or closes[i] < entry_px * (1 - p.stop_pct)
            if i >= entry_i and (take or stop):
                trades.append(
                    Trade(dates[entry_i], dates[i + 1], entry_px,
                          opens[i + 1] * (1 - cost), bars_held + 1)
                )
                in_pos = False
    return trades


def stats(trades: list[Trade]) -> dict:
    if not trades:
        return {"trades": 0}
    rets = np.array([t.ret for t in trades])
    wins = rets > 0
    gross_win = rets[wins].sum()
    gross_loss = -rets[~wins].sum()
    return {
        "trades": len(trades),
        "winrate": wins.mean() * 100,
        "avg_ret": rets.mean() * 100,
        "profit_factor": gross_win / gross_loss if gross_loss > 0 else float("inf"),
        "avg_bars": np.mean([t.bars_held for t in trades]),
        "worst": rets.min() * 100,
    }


def main() -> None:
    args = sys.argv[1:]
    interval = "1d"
    cost_bps = 0.0
    for a in list(args):
        if a.startswith("--interval="):
            interval = a.split("=", 1)[1]
            args.remove(a)
        elif a.startswith("--cost="):
            cost_bps = float(a.split("=", 1)[1])
            args.remove(a)
    symbols = args or DEFAULT_SYMBOLS

    # yfinance limits intraday history; use the max allowed window.
    dl_kwargs: dict = {"interval": interval}
    if interval.endswith(("m", "h")):
        dl_kwargs["period"] = "730d" if interval == "1h" else "60d"
    else:
        dl_kwargs["start"] = START

    print(f"interval: {interval}, cost: {cost_bps} bps/side")
    print(f"{'symbol':<8}{'trades':>8}{'winrate%':>10}{'avg_ret%':>10}"
          f"{'PF':>8}{'avg_bars':>10}{'worst%':>9}")
    print("-" * 63)

    all_trades: list[Trade] = []
    for sym in symbols:
        df = yf.download(sym, auto_adjust=True, progress=False, **dl_kwargs)
        if df is None or df.empty:
            print(f"{sym:<8}  no data")
            continue
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        trades = run_backtest(df, cost_bps=cost_bps)
        all_trades.extend(trades)
        s = stats(trades)
        if s["trades"] == 0:
            print(f"{sym:<8}{0:>8}")
            continue
        print(f"{sym:<8}{s['trades']:>8}{s['winrate']:>10.1f}{s['avg_ret']:>10.2f}"
              f"{s['profit_factor']:>8.2f}{s['avg_bars']:>10.1f}{s['worst']:>9.2f}")

    if all_trades:
        s = stats(all_trades)
        print("-" * 63)
        print(f"{'ALL':<8}{s['trades']:>8}{s['winrate']:>10.1f}{s['avg_ret']:>10.2f}"
              f"{s['profit_factor']:>8.2f}{s['avg_bars']:>10.1f}{s['worst']:>9.2f}")


if __name__ == "__main__":
    main()
