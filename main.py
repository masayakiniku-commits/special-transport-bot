import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")

print("TOKEN確認:", LINE_TOKEN)  # ★追加

def send_line(msg):
    res = requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )
    print("STATUS:", res.status_code)  # ★追加
    print("BODY:", res.text)          # ★追加

send_line("テスト通知")
