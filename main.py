import requests
from bs4 import BeautifulSoup
import os
import time

# ======================
# 設定
# ======================
TOP_N = 3
TARGET = ["てんびん座", "天秤座"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LINE_TOKEN = os.getenv("LINE_TOKEN")

# ======================
# LINE送信（安定版）
# ======================
def send_line(msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    data = {"message": msg}

    for i in range(3):
        try:
            res = requests.post(url, headers=headers, data=data, timeout=10)
            print(f"送信ステータス: {res.status_code}")
            if res.status_code == 200:
                return
        except Exception as e:
            print(f"送信エラー: {e}")
            time.sleep(2)

# ======================
# LINE占い
# ======================
def line_fortune():
    try:
        url = "https://fortune.line.me/horoscope"
        r = requests.get(url, headers=HEADERS, timeout=10)
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

    except Exception as e:
        print(f"LINE占いエラー: {e}")
        return []

# ======================
# Goo占い
# ======================
def goo_fortune():
    try:
        url = "https://fortune.goo.ne.jp/ranking/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select(".ranking_list li")[:TOP_N]

        for i, item in enumerate(items, start=1):
            text = item.get_text(strip=True)
            results.append((i, text))

        return results

    except Exception as e:
        print(f"Goo占いエラー: {e}")
        return []

# ======================
# 楽天占い
# ======================
def rakuten_fortune():
    try:
        url = "https://fortune.rakuten.co.jp/"
        r = requests.get(url, headers=HEADERS, timeout=10)
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

    except Exception as e:
        print(f"楽天占いエラー: {e}")
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
    print("処理開始")

    msg = f"🔮今日の占い（TOP{TOP_N}）\n"

    line = line_fortune()
    goo = goo_fortune()
    rakuten = rakuten_fortune()

    print("LINE取得:", line)
    print("Goo取得:", goo)
    print("楽天取得:", rakuten)

    msg += check_target(line, "LINE占い")
    msg += check_target(goo, "Goo占い")
    msg += check_target(rakuten, "楽天占い")

    if msg.strip() == f"🔮今日の占い（TOP{TOP_N}）":
        msg = f"てんびん座TOP{TOP_N}入りなし"

    print("送信内容:\n", msg)

    send_line(msg)

# ======================
# 実行
# ======================
run()
