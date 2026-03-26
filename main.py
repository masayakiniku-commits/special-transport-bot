import requests
from bs4 import BeautifulSoup

def get_best_libra():
    print("★スクレイピング開始")

    url = "https://today.namedic.jp/horoscope/detail/libra"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    text = soup.get_text()

    best_rank = 99
    best_site = ""
    best_link = ""

    sites = {
        "占いnifty": "https://uranai.nifty.com/",
        "dmenu占い": "https://fortune.dmkt-sp.jp/",
        "Yahoo占い": "https://fortune.yahoo.co.jp/12astro/"
    }

    for site in sites:
        if site in text:
            # 「○位」を探す
            import re
            match = re.search(r"(\d+)位.*" + site, text)

            if match:
                rank = int(match.group(1))

                if rank < best_rank:
                    best_rank = rank
                    best_site = site
                    best_link = sites[site]

    print("★取得結果:", best_rank, best_site)

    return best_rank, best_site, best_link


if __name__ == "__main__":
    print("★実行スタート")

    rank, site, link = get_best_libra()

    if site:
        print("🔮てんびん座 今日の最強占い")
        print(f"{site}：{rank}位")
        print(link)
    else:
        print("⚠️該当なし")
