import os
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# 検索キーワード
keywords = ["甲種輸送", "特殊貨物"]
locations = ["岐阜", "一宮", "名古屋", "刈谷", "安城", "岡崎", "豊川", "豊橋", "浜松"]

def get_yahoo_posts():
    # Yahoo検索URL作成（例）
    query = "+".join(keywords + locations)
    url = f"https://search.yahoo.co.jp/search?p={query}"
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 投稿件数をざっくりカウント
    posts = soup.find_all("li")  # 適宜調整
    count = len(posts)
    return count

def send_discord(msg):
    if not DISCORD_WEBHOOK:
        print("Webhook URL not set")
        return
    data = {"content": msg}
    try:
        requests.post(DISCORD_WEBHOOK, json=data)
    except Exception as e:
        print("Discord通知失敗:", e)

def main():
    count = get_yahoo_posts()
    if count >= 10:
        send_discord(f"⚠️ 投稿数増加: {count}件")

if __name__ == "__main__":
    main()
