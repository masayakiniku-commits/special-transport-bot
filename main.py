import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")

def get_best_libra():
    url = "https://today.namedic.jp/horoscope/detail/libra"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    best_rank = 99
    best_site = ""
    best_link = ""

    sections = soup.select("h3")

    for s in sections:
        text = s.get_text()

        if "位" in text:
            rank = int(text.split("位")[0])
            site = text.split("位")[1].strip()

            # 各サイトリンク作成（固定）
            link_map = {
                "占いnifty": "https://uranai.nifty.com/",
                "dmenu占い": "https://fortune.dmkt-sp.jp/",
                "Yahoo占い": "https://fortune.yahoo.co.jp/12astro/"
            }

            if site in link_map and rank < best_rank:
                best_rank = rank
                best_site = site
                best_link = link_map[site]

    return best_rank, best_site, best_link


def send_line(msg):
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": msg}
    )


if __name__ == "__main__":
    rank, site, link = get_best_libra()

    if site:
        msg = f"🔮てんびん座 今日の最強占い\n\n{site}：{rank}位\n{link}"
    else:
        msg = "⚠️該当占いなし"

    send_line(msg)
