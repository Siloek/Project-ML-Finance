import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def backtest_mm(price, short, long):
    """
    Does the backtest of a moving average crossover strategy.
    ...
    """
    yields = price.pct_change().dropna()

    mm_short = price.rolling(short).mean()
    mm_long = price.rolling(long).mean()

    signal = (mm_short > mm_long).astype(int)

    yields_strategy = signal.mul(yields, axis=0).dropna()

    cumul_market = (1 + yields).cumprod()
    cumuls_strategy = (1 + signal.mul(yields, axis=0)).dropna().cumprod()

    name_strat = f"Strategy {short}/{long}"

    result = pd.DataFrame({
        'Yields_Market': yields,
        'Yields_Strategy': yields_strategy,
        'Cumul_Market': cumul_market,
        name_strat: cumuls_strategy
    })
    return result

data = yf.download('SPY', start="2014-01-01", auto_adjust=True)
price = data["Close"].squeeze()

fig, ax = plt.subplots(figsize=(12, 6))

yields = price.pct_change().dropna()
(yields + 1).cumprod().plot(ax=ax, label="Buy & Hold (S&P 500)", color="black", alpha=0.6)

combinations = [(5, 20), (10, 100), (10, 5), (5, 200), (10,200), (1, 1)]

for short, long in combinations:
    result = backtest_mm(price, short, long)
    result[f"Strategy {short}/{long}"].plot(ax=ax, alpha = 0.8)

plt.title("Comparaison Strategy vs Buy & Hold")
plt.xlabel("Date")
plt.ylabel("$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()