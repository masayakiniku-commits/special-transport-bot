import os
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://fortune.line.me/horoscope", timeout=60000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # ★ランキングっぽい部分を取得
    items = soup.select("li")  # とりあえずli全部

    result = "🔮今日の星座ランキング TOP3\n\n"

    count = 0
    for item in items:
        text = item.get_text(strip=True)

        # 星座っぽいキーワードでフィルタ
        if "座" in text and len(text) < 20:
            result += f"{count+1}位：{text}\n"
            count += 1

        if count == 3:
            break

    if count == 0:
        return "占い取得失敗（サイト構造変化）"

    return result


def run():
    msg = get_fortune()
    send_line(msg)


if __name__ == "__main__":
    print("TOKEN:", LINE_TOKEN)
    run()
