import os
print("TOKEN:", os.getenv("LINE_TOKEN"))
import requests
from bs4 import BeautifulSoup
import os
from playwright.sync_api import sync_playwright

LINE_TOKEN = os.getenv("LINE_TOKEN")
SIGN = "てんびん座"

def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )

# ----------------------
# Yahoo占い
# ----------------------
def yahoo():
    url = "https://fortune.yahoo.co.jp/12astro/ranking.html"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    rows = soup.select(".rankingTable tr")

    for r in rows[1:4]:
        if SIGN in r.text:
            return f"【Yahoo】\n{r.text.strip()}\n{url}"
    return None

# ----------------------
# goo占い
# ----------------------
def goo():
    url = "https://fortune.goo.ne.jp/ranking/"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    items = soup.select(".ranking_list li")

    for i in range(3):
        if SIGN in items[i].text:
            return f"【goo】\n{items[i].text.strip()}\n{url}"
    return None

# ----------------------
# LINE占い（Playwright）
# ----------------------
def line_fortune():
    url = "https://fortune.line.me/horoscope"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)

            page.wait_for_timeout(5000)  # 描画待ち

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        items = soup.select("li")  # 汎用（構造変化に強くするため）

        for i in range(3):
            text = items[i].text
            if SIGN in text:
                return f"【LINE占い】\n{text.strip()}\n{url}"

    except Exception as e:
        return None

    return None

# ----------------------
# 実行
# ----------------------
def run():
    msgs = []

    for f in [yahoo, goo, line_fortune]:
        res = f()
        if res:
            msgs.append(res)

    if msgs:
        send_line("\n\n".join(msgs))

if __name__ == "__main__":
    run()
