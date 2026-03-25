import requests
from bs4 import BeautifulSoup
import os

# ======================
# 設定
# ======================
TOP_N = 5
TARGET = ["てんびん座", "天秤座"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LINE_TOKEN = os.getenv("LINE_TOKEN")

# ======================
# LINE送信
# ======================
def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )

# ======================
# LINE占い
# ======================
def line_fortune():
    try:
        url = "https://fortune.line.me/horoscope"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select("li")

        rank = 0
        for item in items:
            text = item.get_text()

            if "座" in text:
                rank += 1
                if rank <= TOP_N:
                    results.append((rank, text))

        return results

    except:
        return []

# ======================
# Goo占い
# ======================
def goo_fortune():
    try:
        url = "https://fortune.goo.ne.jp/ranking/"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select(".ranking_list li")[:TOP_N]

        for i, item in enumerate(items, start=1):
            text = item.get_text(strip=True)
            results.append((i, text))

        return results

    except:
        return []

# ======================
# 楽天占い
# ======================
def rakuten_fortune():
    try:
        url = "https://fortune.rakuten.co.jp/"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select("li")

        rank = 0
        for item in items:
            text = item.get_text()

            if "座" in text and "位" in text:
                rank += 1
                if rank <= TOP_N:
                    results.append((rank, text))

        return results

    except:
        return []

# ======================
# 判定ロジック
# ======================
def check_target(results, site_name):
    if not results:
        return ""

    msg = f"\n🔮{site_name}\n"
    hit = False

    for rank, text in results:
        msg += f"{rank}位：{text}\n"
        if any(t in text for t in TARGET):
            hit = True

    return msg if hit else ""

# ======================
# 実行
# ======================
def run():
    msg = f"🔮今日の占い（TOP{TOP_N}）\n"

    msg += check_target(line_fortune(), "LINE占い")
    msg += check_target(goo_fortune(), "Goo占い")
    msg += check_target(rakuten_fortune(), "楽天占い")

    if msg.strip() == f"🔮今日の占い（TOP{TOP_N}）":
        msg = f"てんびん座TOP{TOP_N}入りなし"

    send_line(msg)

# ======================
# 実行
# ======================
run()
