import os
import requests
from datetime import datetime, timedelta
import tweepy

LINE_TOKEN = os.getenv("LINE_TOKEN")
BEARER_TOKEN = os.getenv("TWITTER_BEARER")

KEYWORDS = ['甲種輸送', 'シキ1000', 'シキ800', '特殊貨物']
TARGET = ["愛知", "名古屋", "岡崎", "豊橋", "岐阜", "一宮", "浜松"]

def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )

def is_target(text):
    return any(k in text for k in TARGET)

def run():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    start = (datetime.utcnow() - timedelta(minutes=30)).isoformat("T")+"Z"

    tweets = []
    for kw in KEYWORDS:
        res = client.search_recent_tweets(
            query=f'"{kw}" -is:retweet',
            start_time=start,
            max_results=50
        )
        if res.data:
            for t in res.data:
                if is_target(t.text):
                    tweets.append(t.text)

    if len(tweets) >= 2:
        msg = f"⚠️ 特殊輸送検知 {len(tweets)}件\n\n"
        msg += "\n\n".join(tweets[:3])
        send_line(msg)

if __name__ == "__main__":
    run()
