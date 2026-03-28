import os
import requests

# 環境変数から取得
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
LINE_TOKEN = os.getenv("LINE_TOKEN")

# LINE通知関数
def send_line(msg):
    try:
        res = requests.post(
            "https://notify-api.line.me/api/notify",
            headers={"Authorization": "Bearer " + LINE_TOKEN},
            data={"message": msg}
        )
        print("LINE STATUS:", res.status_code)
        print("LINE BODY:", res.text)
    except Exception as e:
        print("LINE送信失敗:", e)

# 甲種輸送ツイート取得関数
def get_koshu_tweets():
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {"query": "甲種輸送 -is:retweet", "max_results": 10}
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    try:
        res = requests.get(url, headers=headers, params=params)
        print("X STATUS:", res.status_code)
        data = res.json()
        return data.get("data", [])
    except Exception as e:
        print("X取得失敗:", e)
        return []

# メイン処理
def main():
    tweets = get_koshu_tweets()
    if not tweets:
        send_line("ℹ️ 有効な甲種輸送投稿はありません")
        print("ツイート取得なし")
        return
    for t in tweets:
        msg = "🚃甲種輸送検知\n\n" + t["text"]
        send_line(msg)

if __name__ == "__main__":
    main()
