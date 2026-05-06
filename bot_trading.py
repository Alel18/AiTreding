import yfinance as yf
import pandas as pd
import requests
from ta.trend import SMAIndicator
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
rsi = RSIIndicator(close).rsi().iloc[-1]

if rsi < 70:
    score += 1

TOKEN = "8775385140:AAG6Mt-_4r7Mq7s1RYjWRkMqYpn_EUiB7E4"
CHAT_ID = "6809245174"

tickers = [
    "BBCA.JK",
    "BBRI.JK",
    "TLKM.JK",
    "ASII.JK",
    "ADRO.JK"
]
tickers = [
    "BBRI.JK","BBCA.JK","BMRI.JK","BBNI.JK",
    "TLKM.JK","ASII.JK","ICBP.JK","INDF.JK",
    "ANTM.JK","ADRO.JK","PTBA.JK","MDKA.JK",
    "CPIN.JK","UNTR.JK","BRIS.JK","GOTO.JK",
    "EXCL.JK","SMGR.JK","KLBF.JK","AKRA.JK"
]

hasil = []

for ticker in tickers:

    data = yf.download(ticker, period="3mo")

    if len(data) < 25:
        continue

    close = data["Close"].squeeze()

    ma5 = SMAIndicator(close, window=5).sma_indicator()
    ma20 = SMAIndicator(close, window=20).sma_indicator()
    rsi = RSIIndicator(close).rsi()
    macd = MACD(close)
    macd_line = macd.macd()
    macd_signal = macd.macd_signal()
    sma20 = SMAIndicator(close, window=20).sma_indicator().iloc[-1]
    sma50 = SMAIndicator(close, window=50).sma_indicator().iloc[-1]

if sma20 > sma50:
    score += 1

    harga = float(close.iloc[-1])

    score = 0

    if ma5.iloc[-1] > ma20.iloc[-1]:
        score += 1

    return_1m = (
        close.iloc[-1] / close.iloc[-20] - 1
    )

    if return_1m > 0:
        score += 1
prob = round(score / 4 * 100, 1)

hasil.append({
    "ticker": ticker,
    "price": harga,
    "score": score,
    "prob": prob
})
score = 0

if ma5.iloc[-1] > ma20.iloc[-1]:
    score += 1

if rsi.iloc[-1] < 30:
    score += 1

if macd_line.iloc[-1] > macd_signal.iloc[-1]:
    score += 1

return_1m = (
    close.iloc[-1] / close.iloc[-20] - 1
)

if return_1m > 0:
    score += 1
df = pd.DataFrame(hasil)

df = df.sort_values(
    by="score",
    ascending=False
)
if return_1m > 0:
    score += 1

prob = round(score / 4 * 100, 1)

hasil.append({
    "ticker": ticker,
    "price": harga,
    "score": score,
    "prob": prob
})
score = 0

# SMA Trend
if sma5 > sma20:
    score += 1

# Volume
if volume_today > volume_avg:
    score += 1

# RSI
if rsi < 70:
    score += 1

# Momentum
if return_1m > 0:
    score += 1

# Probabilitas
prob = round(score / 4 * 100, 1)
hasil.append({
    "ticker": ticker,
    "price": harga,
    "score": score,
    "prob": prob
})

pesan = "TOP SAHAM HARI INI\n\n"

for i, row in df.iterrows():

    pesan += (
        f"{row['ticker']}\n"
        f"Harga: {row['price']:.0f}\n"
        f"Score: {row['score']}\n\n"
    )
    f"Score: {row['score']}\n"
    f"Probabilitas: {row['prob']}%\n\n"

url = (
    f"https://api.telegram.org/bot{TOKEN}/sendMessage"
)

params = {
    "chat_id": CHAT_ID,
    "text": pesan
}

r = requests.get(url, params=params)

print(r.text)
