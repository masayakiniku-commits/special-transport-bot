import os
import requests

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
LINE_TOKEN = os.getenv("LINE_TOKEN")

def send_line(msg):
requests.post(
"https://notify-api.line.me/api/notify",
headers={"Authorization": "Bearer " + LINE_TOKEN},
data={"message": msg}
)

def get_koshu_tweets():
url = "https://api.twitter.com/2/tweets/search/recent"

```
params = {
    "query": "(甲種輸送 OR 配給輸送) (EF210 OR EF65 OR DE10 OR DD200) -is:retweet",
    "max_results": 10
}

headers = {
    "Authorization": "Bearer " + BEARER_TOKEN
}

res = requests.get(url, headers=headers, params=params)
data = res.json()

return data.get("data", [])
```

def main():
tweets = get_koshu_tweets()

```
if not tweets:
    print("取得なし")
    return

for t in tweets:
    text = t["text"]

    if "甲種輸送" in text:
        msg = "🚃甲種輸送検知\n\n" + text
        send_line(msg)
        print("送信:", text)
```

if **name** == "**main**":
main()
