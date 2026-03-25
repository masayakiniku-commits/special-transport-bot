import os
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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
# Yahoo占い取得（Playwright版）
# ======================
def yahoo():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("https://fortune.yahoo.co.jp/", timeout=60000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    return text[:300]


# ======================
# 実行
# ======================
def run():
    msg = "🔮今日の占い\n\n"
    msg += yahoo()

    send_line(msg)


if __name__ == "__main__":
    print("TOKEN:", LINE_TOKEN)
    run()
