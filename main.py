import os
import requests

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
LINE_TOKEN = os.getenv("LINE_TOKEN")

# =========================

# ■ LINE送信（デバッグ付き）

# =========================

def send_line(msg):
res = requests.post(
"https://notify-api.line.me/api/notify",
headers={"Authorization": "Bearer " + str(LINE_TOKEN)},
data={"message": msg}
)

```
print("===== LINE DEBUG =====")
print("STATUS:", res.status_code)
print("BODY:", res.text)
print("======================")
```

# =========================

# ■ X取得

# =========================

def get_koshu_tweets():
url = "https://api.twitter.com/2/tweets/search/recent"

```
params = {
    "query": "甲種輸送 -is:retweet",
    "max_results": 10
}

headers = {
    "Authorization": "Bearer " + str(BEARER_TOKEN)
}

res = requests.get(url, headers=headers, params=params)

print("===== X DEBUG =====")
print("STATUS:", res.status_code)
print("BODY:", res.text)
print("===================")

data = res.json()
return data.get("data", [])
```

# =========================

# ■ 実行

# =========================

def main():
# ① LINE単体テスト
send_line("テスト通知")

```
# ② X取得テスト
tweets = get_koshu_tweets()

if not tweets:
    print("ツイート取得なし")
    return

for t in tweets:
    text = t["text"]
    msg = "🚃甲種輸送検知\n\n" + text
    send_line(msg)
```

if **name** == "**main**":
main()
