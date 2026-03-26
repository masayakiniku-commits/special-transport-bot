import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")

def send_line(msg):
    res = requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )
    print("STATUS:", res.status_code)
    print("BODY:", res.text)

# ★絶対に通る確認用
print("ここまで来てる")

send_line("🔥 強制通知テスト")
