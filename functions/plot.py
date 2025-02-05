def plot_moex_history(ticker, days=7):
    from API.moex import get_moex_stock_history
    import pandas as pd
    import matplotlib.pyplot as plt

    df = get_moex_stock_history(ticker, days)
    if df is not None:
        df["begin"] = pd.to_datetime(df["begin"])
        df.set_index("begin", inplace=True)
        df["close"].plot()
        plt.title(f"История цен акции {ticker}")
        plt.show()
    else:
        False