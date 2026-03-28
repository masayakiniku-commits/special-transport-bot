import os
import requests
from time import sleep

# 環境変数からトークン取得
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

# X取得関数
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

# メインループ（1時間ごとに通知）
def main():
    while True:
        tweets = get_koshu_tweets()
        if not tweets:
            print("ツイート取得なし")
        for t in tweets:
            msg = "🚃甲種輸送検知\n\n" + t["text"]
            send_line(msg)
        sleep(3600)  # 1時間待機

if __name__ == "__main__":
    main()
