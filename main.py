import os
import requests
from bs4 import BeautifulSoup

LINE_TOKEN = os.getenv("LINE_TOKEN")

# ======================
# LINE送信
# ======================
def send_line(msg):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": "U895287281171ab97865fafce69b8af76",
        "messages": [{"type": "text", "text": msg}]
    }

    requests.post(url, headers=headers, json=data)


# ======================
# Yahoo占い取得
# ======================
def yahoo():
    url = "https://uranai.yahoo.co.jp/ranking"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 適当にテキスト抽出（まずは動作優先）
    text = soup.get_text()

    # 上位だけ抜粋（長すぎ防止）
    return text[:300]


# ======================
# 実行
# ======================
def run():
    msg = "🔮今日の占いランキング\n\n"
    msg += yahoo()

    send_line(msg)


# ======================
# スタート
# ======================
if __name__ == "__main__":
    print("TOKEN:", LINE_TOKEN)  # デバッグ
    run()
