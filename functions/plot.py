import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from aiogram.types import BufferedInputFile
from API.moex import get_moex_stock_history, get_moex_stock_history_today

import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from aiogram.types import BufferedInputFile

def plot_moex_history(ticker, days=7):
    df = get_moex_stock_history(ticker, days)
    
    if df is not None and not df.empty:
        df["begin"] = pd.to_datetime(df["begin"])
        df.set_index("begin", inplace=True)

        bg_color="#242424"

        plt.figure(figsize=(12, 6), facecolor=bg_color)
        ax = plt.gca()
        ax.set_facecolor(bg_color)

        plt.plot(df.index, df["close"], linestyle="-", color="#00c8ff", label="Цена закрытия")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
        plt.xticks(rotation=45, fontsize=10, color="white")
        plt.yticks(color="white")

        plt.xlabel("Дата", fontsize=12, fontweight="bold", color="white")
        plt.ylabel("Цена (₽)", fontsize=12, fontweight="bold", color="white")
        plt.title(f"История цен акции {ticker} за {days} дней", fontsize=14, fontweight="bold", color="white")

        plt.grid(True, linestyle="--", alpha=0.5, color="gray")
        plt.gca().yaxis.grid(True, linestyle="--", alpha=0.5, color="gray")

        last_date = df.index[-1]
        last_price = df["close"].iloc[-1]
        plt.annotate(f"{last_price:.2f} ₽", 
                     xy=(last_date, last_price), 
                     xytext=(last_date, last_price + (df["close"].max() - df["close"].min()) * 0.05),
                     fontsize=12, color="yellow",
                     arrowprops=dict(facecolor="yellow", arrowstyle="->"))

        plt.legend(fontsize=10, facecolor="#222222", edgecolor="white", labelcolor="white")
        
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=200, facecolor=bg_color, pad_inches=0.5)
        img_bytes.seek(0)
        plt.close()

        photo = BufferedInputFile(img_bytes.getvalue(), filename=f"{ticker}_history.png")
        return photo
    else:
        return None

def plot_moex_history_today(ticker):
    df = get_moex_stock_history_today(ticker)

    if df is not None and not df.empty:
        df["begin"] = pd.to_datetime(df["begin"])
        df.set_index("begin", inplace=True)

        bg_color="#242424"

        plt.figure(figsize=(12, 6), facecolor=bg_color)
        ax = plt.gca()
        ax.set_facecolor(bg_color)

        plt.plot(df.index, df["close"], linestyle="-", color="#00c8ff")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        plt.xticks(rotation=45, fontsize=10, color="white")
        plt.yticks(color="white")

        plt.xlabel("Время (часы)", fontsize=12, fontweight="bold", color="white")
        plt.ylabel("Цена (₽)", fontsize=12, fontweight="bold", color="white")
        plt.title(f"Динамика цены акции {ticker} за сегодня", fontsize=14, fontweight="bold", color="white")

        plt.grid(True, linestyle="--", alpha=0.5, color="gray")
        plt.gca().yaxis.grid(True, linestyle="--", alpha=0.5, color="gray")

        last_time = df.index[-1]
        last_price = df["close"].iloc[-1]
        plt.annotate(f"{last_price:.2f} ₽",
                     xy=(last_time, last_price),
                     xytext=(last_time, last_price + (df["close"].max() - df["close"].min()) * 0.05),
                     fontsize=12, color="yellow",
                     arrowprops=dict(facecolor="yellow", arrowstyle="->"))

        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=200, facecolor=bg_color, pad_inches=0.5)
        img_bytes.seek(0)
        plt.close()

        photo = BufferedInputFile(img_bytes.getvalue(), filename=f"{ticker}_1d_history.png")
        return photo
    else:
        return None
