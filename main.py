import requests
import xml.etree.ElementTree as ET
import os

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# 監視キーワード
KEYWORDS = ["甲種輸送", "特殊貨物", "EF210", "EF64", "EF65", "EF66", "DD200", "DE10"]

# RSS一覧（増やせる）
RSS_URLS = [
    "https://news.google.com/rss/search?q=甲種輸送",
    "https://news.google.com/rss/search?q=特殊貨物",
    "https://news.google.com/rss/search?q=EF210",
    "https://news.google.com/rss/search?q=EF64",
    "https://news.google.com/rss/search?q=EF65",
    "https://news.google.com/rss/search?q=EF66",  
]

def fetch_rss():
    results = []

    for url in RSS_URLS:
        try:
            res = requests.get(url, timeout=10)
            root = ET.fromstring(res.content)

            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text

                # キーワード判定
                if any(k in title for k in KEYWORDS):
                    results.append({
                        "title": title,
                        "link": link
                    })

        except Exception as e:
            print("RSS取得エラー:", e)

    return results


def send_discord(msg):
    if not DISCORD_WEBHOOK:
        return
    requests.post(DISCORD_WEBHOOK, json={"content": msg})


def main():
    results = fetch_rss()
    count = len(results)

    print("件数:", count)

    if count > 0:
        msg = f"🚆 甲種輸送・貨物検知\n件数: {count}\n\n"

        for r in results[:5]:
            msg += f"・{r['title']}\n{r['link']}\n\n"

        send_discord(msg)


if __name__ == "__main__":
    main()
