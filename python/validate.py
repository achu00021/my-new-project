"""
Honest validation of the TripleConfluence winrates.

1. Walk-forward: evaluate the shipped defaults on 2016-2026 only —
   a window that parameter selection (done on 2005-2015-dominated data)
   could not have memorized.
2. Survivorship stress: basket of historically weak/troubled large caps
   (GE, F, T, C, BAC, INTC, VZ, XRX) — no hindsight winners — plus crypto.
3. Costs: hourly and daily backtests with realistic slippage per side.

Run:  python3 validate.py
"""

import pandas as pd
import yfinance as yf

from backtest import run_backtest, stats
from indicator import Params

DEV = ["SPY", "QQQ", "DIA", "IWM", "AAPL", "MSFT", "GOOGL", "JNJ", "XLP", "GLD"]
OOS = ["XLK", "XLV", "XLE", "KO", "PG", "V", "WMT", "EEM", "EFA", "HD"]
WEAK = ["GE", "F", "T", "C", "BAC", "INTC", "VZ", "XRX"]


def fetch(syms, **kw):
    out = {}
    for sym in syms:
        df = yf.download(sym, auto_adjust=True, progress=False, **kw)
        if df is None or df.empty:
            continue
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        out[sym] = df
    return out


def agg(data, p=Params(), cost_bps=0.0, lo=None, hi=None):
    trades = []
    for df in data.values():
        d = df.loc[lo:hi] if (lo or hi) else df
        if len(d) > 250:
            trades.extend(run_backtest(d, p, cost_bps=cost_bps))
    return stats(trades)


def line(name, s):
    if s["trades"] == 0:
        print(f"{name:<44}  no trades")
        return
    print(f"{name:<44}{s['trades']:>7}{s['winrate']:>8.1f}{s['avg_ret']:>8.2f}"
          f"{s['profit_factor']:>7.2f}{s['avg_bars']:>8.1f}{s['worst']:>9.2f}")


print("fetching data...")
dev_d = fetch(DEV, interval="1d", start="2005-01-01")
oos_d = fetch(OOS, interval="1d", start="2005-01-01")
weak_d = fetch(WEAK, interval="1d", start="2005-01-01")
dev_h = fetch(DEV, interval="1h", period="730d")
crypto = fetch(["BTC-USD", "ETH-USD"], interval="1d", start="2015-01-01")

hdr = f"{'test':<44}{'trades':>7}{'win%':>8}{'avg%':>8}{'PF':>7}{'bars':>8}{'worst%':>9}"

print("\n=== 1. WALK-FORWARD (2016-2026, unseen by tuning) ===")
print(hdr)
line("  dev basket 2016-2026", agg(dev_d, lo="2016-01-01"))
line("  OOS basket 2016-2026", agg(oos_d, lo="2016-01-01"))

print("\n=== 2. SURVIVORSHIP STRESS ===")
print(hdr)
line("  weak large caps, daily 2005-2026", agg(weak_d))
line("  crypto BTC/ETH, daily 2015-2026", agg(crypto))

print("\n=== 3. COSTS ===")
print(hdr)
line("  hourly dev, 0 bps", agg(dev_h))
line("  hourly dev, 5 bps/side", agg(dev_h, cost_bps=5))
line("  hourly dev, 10 bps/side", agg(dev_h, cost_bps=10))
line("  daily dev, 5 bps/side", agg(dev_d, cost_bps=5))
