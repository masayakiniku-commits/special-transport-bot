import os
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# 貨物系キーワード
KEYWORDS = ["甲種輸送", "特殊貨物"]

# 対象エリア（県 + 既存の市も含める）
AREAS = [
    "愛知", "岐阜", "滋賀", "静岡", "長野",
    "一宮", "名古屋", "刈谷", "安城", "岡崎", "豊川", "豊橋", "浜松"
]

# 鉄道関連（路線・会社）
RAIL_WORDS = [
    "東海道本線", "中央線", "JR貨物", "JR東海"
]

# 機関車・車両
LOCO_WORDS = [
    "DE10", "EF210", "EF64", "DD200", "EF65"
]

THRESHOLD = 10


def fetch_results():
    query = "+".join(KEYWORDS + AREAS)
    url = f"https://search.yahoo.co.jp/search?p={query}"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except:
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for a in soup.select("a"):
        title = a.get_text(strip=True)
        link = a.get("href")

        if not title or not link:
            continue

        # ノイズ除去
        if len(title) < 15:
            continue
        if "yahoo.co.jp" in link:
            continue

        text = title

        hit = 0

        # 貨物系
        if any(k in text for k in KEYWORDS):
            hit += 1

        # エリア
        if any(a in text for a in AREAS):
            hit += 1

        # 路線・会社
        if any(r in text for r in RAIL_WORDS):
            hit += 1

        # 車両
        if any(l in text for l in LOCO_WORDS):
            hit += 1

        # 2条件以上一致で採用
        if hit >= 2:
            results.append({
                "title": title,
                "url": link
            })

    return results


def send_discord(msg):
    if not DISCORD_WEBHOOK:
        return
    requests.post(DISCORD_WEBHOOK, json={"content": msg})


def main():
    results = fetch_results()
    count = len(results)

    print("件数:", count)

    if count >= THRESHOLD:

        top = results[:3]

        links = ""
        for r in top:
            links += f"\n・{r['title']}\n{r['url']}\n"

        msg = (
            f"⚠️ 貨物投稿数増加（広域）\n"
            f"対象: 愛知・岐阜・滋賀・静岡・長野\n"
            f"件数: {count}\n"
            f"{links}"
        )

        send_discord(msg)


if __name__ == "__main__":
    main()
