import requests

TOKEN = "8775385140:AAG6Mt-_4r7Mq7s1RYjWRkMqYpn_EUiB7E4"
CHAT_ID = "8775385140"

def kirim_telegram(pesan):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    params = {
        "chat_id": CHAT_ID,
        "text": pesan
    }

    r = requests.get(url, params=params)

    print(r.text)

kirim_telegram("AI Trading GitHub Berhasil Jalan")
