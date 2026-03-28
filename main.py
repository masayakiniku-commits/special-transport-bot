import requests
import xml.etree.ElementTree as ET
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")

def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": "Bearer " + LINE_TOKEN},
        data={"message": msg}
    )

def check_rss():
    url = "https://news.yahoo.co.jp/rss/topics/domestic.xml"
    res = requests.get(url)
    root = ET.fromstring(res.content)

    items = root.findall(".//item")

    found = False

    for item in items:
        title = item.find("title").text

        if "甲種輸送" in title:
            send_line("🚃甲種輸送検知\n" + title)
            found = True

    if not found:
        send_line("ℹ️ 有効な投稿はありません")

if __name__ == "__main__":
    check_rss()
