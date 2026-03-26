import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")

def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )

# ★テスト用
send_line("✅ 通知テスト成功")
