import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from aiogram.types import BufferedInputFile
from API.moex import get_moex_stock_history, get_moex_stock_history_1d

def plot_moex_history(ticker, days=7):
    df = get_moex_stock_history(ticker, days)
    
    if df is not None and not df.empty:
        df["begin"] = pd.to_datetime(df["begin"])
        df.set_index("begin", inplace=True)

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df["close"], marker="o", linestyle="-", color="dodgerblue", label="Цена закрытия")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
        plt.xticks(rotation=45, fontsize=10)

        plt.xlabel("Дата", fontsize=12, fontweight="bold")
        plt.ylabel("Цена (₽)", fontsize=12, fontweight="bold")
        plt.title(f"История цен акции {ticker} за последние {days} дней", fontsize=14, fontweight="bold")

        plt.grid(True, linestyle="--", alpha=0.6)
        plt.gca().yaxis.grid(True, linestyle="--", alpha=0.6)

        last_date = df.index[-1]
        last_price = df["close"].iloc[-1]
        plt.annotate(f"{last_price:.2f} ₽", 
                     xy=(last_date, last_price), 
                     xytext=(last_date, last_price + (df["close"].max() - df["close"].min()) * 0.05),
                     fontsize=12, color="red",
                     arrowprops=dict(facecolor="red", arrowstyle="->"))

        plt.legend(fontsize=10)
        
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=200)
        img_bytes.seek(0)
        plt.close()

        photo = BufferedInputFile(img_bytes.getvalue(), filename=f"{ticker}_history.png")
        return photo
    else:
        return None

def plot_moex_history_1d(ticker):
    df = get_moex_stock_history_1d(ticker)

    if df is not None and not df.empty:
        df["begin"] = pd.to_datetime(df["begin"])
        df.set_index("begin", inplace=True)

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df["close"], marker="o", linestyle="-", color="dodgerblue")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        plt.xticks(rotation=45, fontsize=10)

        plt.xlabel("Время (часы)", fontsize=12, fontweight="bold")
        plt.ylabel("Цена (₽)", fontsize=12, fontweight="bold")
        plt.title(f"Динамика цены акции {ticker} за последние 24 часа", fontsize=14, fontweight="bold")

        plt.grid(True, linestyle="--", alpha=0.6)
        plt.gca().yaxis.grid(True, linestyle="--", alpha=0.6)

        last_time = df.index[-1]
        last_price = df["close"].iloc[-1]
        plt.annotate(f"{last_price:.2f} ₽",
                     xy=(last_time, last_price),
                     xytext=(last_time, last_price + (df["close"].max() - df["close"].min()) * 0.05),
                     fontsize=12, color="red",
                     arrowprops=dict(facecolor="red", arrowstyle="->"))

        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=200)
        img_bytes.seek(0)
        plt.close()

        photo = BufferedInputFile(img_bytes.getvalue(), filename=f"{ticker}_1d_history.png")
        return photo
    else:
        return None
