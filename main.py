import requests
from bs4 import BeautifulSoup

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
            try:
                rank = int(text.split("位")[0])
                site = text.split("位")[1].strip()

                link_map = {
                    "占いnifty": "https://uranai.nifty.com/",
                    "dmenu占い": "https://fortune.dmkt-sp.jp/",
                    "Yahoo占い": "https://fortune.yahoo.co.jp/12astro/"
                }

                if site in link_map and rank < best_rank:
                    best_rank = rank
                    best_site = site
                    best_link = link_map[site]

            except:
                continue

    return best_rank, best_site, best_link


if __name__ == "__main__":
    rank, site, link = get_best_libra()

    if site:
        print("🔮てんびん座 今日の最強占い\n")
        print(f"{site}：{rank}位")
        print(link)
    else:
        print("⚠️該当占いなし")
