import yfinance as yf
import pandas as pd
import requests

from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator

TOKEN = "TOKEN_BOT_KAMU"
CHAT_ID = "6809245174"

tickers = [
    "BBRI.JK","BBCA.JK","BMRI.JK","BBNI.JK",
    "TLKM.JK","ASII.JK","ICBP.JK","INDF.JK",
    "ANTM.JK","ADRO.JK","PTBA.JK","MDKA.JK",
    "CPIN.JK","UNTR.JK","BRIS.JK","GOTO.JK",
    "EXCL.JK","SMGR.JK","KLBF.JK","AKRA.JK"
]

hasil = []

for ticker in tickers:

    try:

        data = yf.download(
            ticker,
            period="3mo",
            progress=False
        )

        if len(data) < 50:
            continue

        close = data["Close"].squeeze()
        volume = data["Volume"].squeeze()

        harga = float(close.iloc[-1])

        score = 0

        # SMA
        sma5 = SMAIndicator(
            close,
            window=5
        ).sma_indicator().iloc[-1]

        sma20 = SMAIndicator(
            close,
            window=20
        ).sma_indicator().iloc[-1]

        if sma5 > sma20:
            score += 1

        # RSI
        rsi = RSIIndicator(close).rsi().iloc[-1]

        if rsi < 70:
            score += 1

        # MACD
        macd = MACD(close)

        macd_line = macd.macd().iloc[-1]
        macd_signal = macd.macd_signal().iloc[-1]

        if macd_line > macd_signal:
            score += 1

        # Momentum
        return_1m = (
            close.iloc[-1] / close.iloc[-20] - 1
        )

        if return_1m > 0:
            score += 1

        # Volume
        volume_today = volume.iloc[-1]
        volume_avg = volume.rolling(20).mean().iloc[-1]

        if volume_today > volume_avg:
            score += 1

        # Probabilitas
        prob = round(score / 5 * 100, 1)

        hasil.append({
            "ticker": ticker,
            "price": harga,
            "score": score,
            "prob": prob
        })

    except:
        continue

df = pd.DataFrame(hasil)

df = df.sort_values(
    by="score",
    ascending=False
)

pesan = "TOP SAHAM HARI INI\n\n"

for i, row in df.head(5).iterrows():

    pesan += (
        f"{row['ticker']}\n"
        f"Harga: {row['price']:.0f}\n"
        f"Score: {row['score']}\n"
        f"Probabilitas: {row['prob']}%\n\n"
    )

url = (
    f"https://api.telegram.org/bot{TOKEN}/sendMessage"
)

params = {
    "chat_id": CHAT_ID,
    "text": pesan
}

r = requests.get(url, params=params)

print(r.text)
TOKEN = "8775385140:AAG6Mt-_4r7Mq7s1RYjWRkMqYpn_EUiB7E4"
r = requests.get(url, params=params)

print(pesan)
print(r.status_code)
print(r.text)
