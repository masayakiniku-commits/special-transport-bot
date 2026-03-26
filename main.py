import requests
from bs4 import BeautifulSoup

print("★実行スタート")

# ===== ニフティ =====
def get_nifty():
    url = "https://fortune.nifty.com/12star/libra/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    rank = soup.select_one(".rank")
    if rank:
        return int(rank.text.replace("位", "").strip())
    return 99


# ===== Yahoo =====
def get_yahoo():
    url = "https://fortune.yahoo.co.jp/12astro/libra"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    rank = soup.select_one(".rank")
    if rank:
        return int(rank.text.replace("位", "").strip())
    return 99


print("★スクレイピング開始")

results = {
    "nifty占い": (get_nifty(), "https://fortune.nifty.com/12star/libra/"),
    "Yahoo占い": (get_yahoo(), "https://fortune.yahoo.co.jp/12astro/libra"),
}

print("★取得結果:", results)

# ===== 一番良い順位を選ぶ =====
best = min(results.items(), key=lambda x: x[1][0])

name = best[0]
rank = best[1][0]
url = best[1][1]

if rank <= 3:
    message = f"今日のてんびん座は{rank}位！\n{name}\n{url}"
else:
    message = f"今日は見送り（最高{rank}位）"

print(message)
