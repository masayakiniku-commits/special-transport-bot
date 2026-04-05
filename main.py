import os
import requests
import datetime

BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

QUERY = "甲種輸送 OR 特殊貨物 (EF210 OR EF64 OR EF65 OR EF66 OR DD200 OR DE10)"

def fetch_tweets():
    url = "https://api.twitter.com/2/tweets/search/recent"

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = {
        "query": QUERY,
        "max_results": 20,
        "tweet.fields": "created_at,text"
    }

    res = requests.get(url, headers=headers, params=params)

    if res.status_code != 200:
        print("APIエラー:", res.text)
        return []

    data = res.json()

    tweets = []

    for t in data.get("data", []):
        text = t["text"]

        # ノイズ除去
        if "プレゼント" in text:
            continue
        if len(text) < 20:
            continue

        tweets.append(text)

    return tweets


def send_discord(msg):
    if not DISCORD_WEBHOOK:
        return

    requests.post(DISCORD_WEBHOOK, json={"content": msg})


def main():
    tweets = fetch_tweets()
    count = len(tweets)

    print("件数:", count)

    if count >= 3:
        msg = "⚠️ 甲種輸送・特殊貨物の投稿増加\n\n"

        for t in tweets[:5]:
            msg += f"・{t[:80]}\n\n"

        send_discord(msg)


if __name__ == "__main__":
    main()
