import os
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# 検索キーワードと場所
keywords = ["甲種輸送", "特殊貨物"]
locations = ["岐阜", "一宮", "名古屋", "刈谷", "安城", "岡崎", "豊川", "豊橋", "浜松"]

# 投稿数の閾値
THRESHOLD = 10

def get_yahoo_posts_count():
    # Yahoo検索クエリを作成
    query = "+".join(keywords + locations)
    url = f"https://search.yahoo.co.jp/search?p={query}"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        print("Yahoo取得失敗:", e)
        return 0

    soup = BeautifulSoup(res.text, "html.parser")

    # 検索結果の数をざっくりカウント
    # Yahoo検索結果では <li> タグに個別結果があるのでカウント
    results = soup.select("li")  # 必要に応じてCSSセレクタを調整
    count = len(results)
    return count

def send_discord(msg):
    if not DISCORD_WEBHOOK:
        print("Webhook URLが設定されていません")
        return

    data = {"content": msg}
    try:
        r = requests.post(DISCORD_WEBHOOK, json=data, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print("Discord通知失敗:", e)

def main():
    count = get_yahoo_posts_count()
    print(f"投稿件数: {count}")
    if count >= THRESHOLD:
        send_discord(f"⚠️ 投稿数増加: {count}件")

if __name__ == "__main__":
    main()
