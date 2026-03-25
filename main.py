import requests
from bs4 import BeautifulSoup
import os
import time

# ======================
# 自分の条件（ここ固定）
# ======================
MY_SIGNS = ["てんびん座", "天秤座"]
MY_BLOOD = ["A型"]
MY_ETO = ["巳"]   # 巳年

TOP_N = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

LINE_TOKEN = os.getenv("LINE_TOKEN")

# ======================
# LINE送信
# ======================
def send_line(msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": msg}

    for _ in range(3):
        try:
            res = requests.post(url, headers=headers, data=data, timeout=10)
            print("送信:", res.status_code)
            return
        except:
            time.sleep(2)

# ======================
# Gooランキング共通取得
# ======================
def get_ranking(url, selector):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select(selector)[:TOP_N]

        for i, item in enumerate(items, start=1):
            text = item.get_text(strip=True)
            results.append((i, text))

        return results
    except Exception as e:
        print("取得エラー:", e)
        return []

# ======================
# 各占い
# ======================
def zodiac():
    return get_ranking(
        "https://fortune.goo.ne.jp/ranking/",
        ".ranking_list li"
    )

def blood():
    return get_ranking(
        "https://fortune.goo.ne.jp/blood/",
        "li"
    )

def eto():
    return get_ranking(
        "https://fortune.goo.ne.jp/",
        "li"
    )

# ======================
# 判定
# ======================
def check(results, targets, title):
    msg = ""
    hit = False

    for rank, text in results:
        if any(t in text for t in targets):
            msg += f"{title} {rank}位：{text}\n"
            hit = True

    return msg, hit

# ======================
# 実行
# ======================
def run():
    print("処理開始")

    msg = "🔮今日のラッキー通知\n"
    hit_total = False

    # 星座
    z = zodiac()
    print("星座:", z)
    m, h = check(z, MY_SIGNS, "星座")
    msg += m
    hit_total |= h

    # 血液型
    b = blood()
    print("血液型:", b)
    m, h = check(b, MY_BLOOD, "血液型")
    msg += m
    hit_total |= h

    # 干支
    e = eto()
    print("干支:", e)
    m, h = check(e, MY_ETO, "干支")
    msg += m
    hit_total |= h

    # 通知判定
    if hit_total:
        print("送信内容:\n", msg)
        send_line(msg)
    else:
        print("該当なし（通知なし）")

run()
