print("🔥 実行されてる")

import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")

requests.post(
    "https://notify-api.line.me/api/notify",
    headers={"Authorization": f"Bearer {LINE_TOKEN}"},
    data={"message": "🔥 強制通知"}
)
