import os
import requests

LINE_TOKEN = os.getenv("LINE_TOKEN")

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


def get_fortune():
    # 仮：固定メッセージ（まずは成功させる）
    return "🔮今日の運勢\n\n今日は良い流れ。チャンスを逃すな。"


def run():
    msg = get_fortune()
    send_line(msg)


if __name__ == "__main__":
    print("TOKEN:", LINE_TOKEN)
    run()
