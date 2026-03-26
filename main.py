import os
import requests

LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_API = "https://notify-api.line.me/api/notify"

def send_line(message):
    if not LINE_TOKEN:
        print("⚠️ LINE_TOKEN 未設定")
        return
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": message}
    try:
        res = requests.post(LINE_API, headers=headers, data=payload)
        print(f"LINE通知ステータス: {res.status_code}")
    except Exception as e:
        print(f"LINE通知失敗: {e}")

# テスト用順位
rank_yahoo = 3
rank_nifty = 5
rank_au = 2

message = (
    f"★テスト占い順位★\n"
    f"Yahoo占い: {rank_yahoo}\n"
    f"Nifty占い: {rank_nifty}\n"
    f"AU占い: {rank_au}"
)

print(message)
send_line(message)
