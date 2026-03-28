import os
import requests

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
LINE_TOKEN = os.getenv("LINE_TOKEN")

def send_line(msg):
    res = requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": "Bearer " + LINE_TOKEN},
        data={"message": msg}
    )
    print("LINE STATUS:", res.status_code)
    print("LINE BODY:", res.text)

def get_koshu_tweets():
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {"query": "甲種輸送 -is:retweet", "max_results": 10}
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    res = requests.get(url, headers=headers, params=params)
    print("X STATUS:", res.status_code)
    print("X BODY:", res.text)
    data = res.json()
    return data.get("data", [])

def main():
    send_line("テスト通知")
    tweets = get_koshu_tweets()
    if not tweets:
        print("ツイート取得なし")
        return
    for t in tweets:
        msg = "🚃甲種輸送検知\n\n" + t["text"]
        send_line(msg)

if __name__ == "__main__":
    main()
