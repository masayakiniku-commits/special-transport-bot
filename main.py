import requests
from bs4 import BeautifulSoup
import json
import os

# ===== プログラムタイトル =====
PROGRAM_TITLE = "甲種輸送・特殊貨物アラート"

# ===== 設定 =====
KEYWORDS = ["甲種輸送", "特殊貨物"]
AREAS = ["岐阜","一宮","名古屋","刈谷","安城","岡崎","豊川","豊橋","浜松"]

LINE_TOKEN = os.getenv("LINE_TOKEN")
DATA_FILE = "data.json"
THRESHOLD = 10  # 通知閾値

# ===== Yahoo検索から投稿URLを取得 =====
def fetch_posts(query):
    url = f"https://search.yahoo.co.jp/search?p={query}+site:twitter.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    posts = []
    for item in soup.select("li"):
        text = item.get_text()
        if "twitter.com" in text or "X" in text:
            # URLを抽出する簡易版
            links = item.select("a[href]")
            for link in links:
                href = link.get("href")
                if "twitter.com" in href:
                    posts.append(href)
    return list(set(posts))  # 重複排除

# ===== データ読み込み/保存 =====
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ===== LINE通知 =====
def send_line(msg):
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": msg}
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

# ===== メイン =====
def main():
    old_data = load_data()
    new_data = {}
    alerts = []

    for kw in KEYWORDS:
        for area in AREAS:
            query = f"{kw} {area}"
            posts = fetch_posts(query)
            new_data[query] = posts

            old_posts = old_data.get(query, [])
            if len(posts) >= THRESHOLD and len(posts) > len(old_posts):
                # 件数順に整列
                alerts.append(f"{query} 投稿数: {len(posts)}件 (前回 {len(old_posts)}件)")
                # URLリンクの上位10件を通知
                top_links = "\n".join(posts[:10])
                alerts.append(top_links)

    save_data(new_data)

    if alerts:
        msg = f"【{PROGRAM_TITLE}】\n" + "\n".join(alerts)
        send_line(msg)

if __name__ == "__main__":
    main()
