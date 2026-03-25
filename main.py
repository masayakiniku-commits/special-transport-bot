import requests
from bs4 import BeautifulSoup

TARGET = ["てんびん座", "天秤座"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ----------------------
# LINE占い（耐性強化）
# ----------------------
def line_fortune():
    try:
        url = "https://fortune.line.me/horoscope"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select("li")  # 広く取る

        rank = 0
        for item in items:
            text = item.get_text()

            if "座" in text:
                rank += 1
                if rank <= 3:
                    results.append((rank, text))

        return results

    except:
        return []

# ----------------------
# Goo占い（安定）
# ----------------------
def goo_fortune():
    try:
        url = "https://fortune.goo.ne.jp/ranking/"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        items = soup.select(".ranking_list li")[:3]

        for i, item in enumerate(items, start=1):
            text = item.get_text(strip=True)
            results.append((i, text))

        return results

    except:
        return []

# ----------------------
# 楽天占い（精度改善）
# ----------------------
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

            # 星座っぽいものだけ抽出
            if "座" in text and "位" in text:
                rank += 1
                if rank <= 3:
                    results.append((rank, text))

        return results

    except:
        return []

# ----------------------
# 判定
# ----------------------
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

# ----------------------
# 実行
# ----------------------
def run():
    msg = "🔮今日の占い（TOP3）\n"

    msg += check_target(line_fortune(), "LINE占い")
    msg += check_target(goo_fortune(), "Goo占い")
    msg += check_target(rakuten_fortune(), "楽天占い")

    if msg.strip() == "🔮今日の占い（TOP3）":
        msg = "てんびん座TOP3入りなし"

    print(msg)

run()
