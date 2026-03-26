import requests
from bs4 import BeautifulSoup

def get_nifty():
    url = "https://uranai.nifty.com/12seiza/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for li in soup.select("li"):
        text = li.get_text()
        if "てんびん座" in text:
            return int(text.split("位")[0])
    return 99


def get_dmenu():
    url = "https://fortune.dmkt-sp.jp/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for li in soup.select("li"):
        text = li.get_text()
        if "てんびん座" in text:
            return int(text.split("位")[0])
    return 99


def get_yahoo():
    url = "https://fortune.yahoo.co.jp/12astro/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for li in soup.select("li"):
        text = li.get_text()
        if "てんびん座" in text:
            return int(text.split("位")[0])
    return 99


if __name__ == "__main__":
    print("★実行スタート")

    results = {
        "占いnifty": (get_nifty(), "https://uranai.nifty.com/"),
        "dmenu占い": (get_dmenu(), "https://fortune.dmkt-sp.jp/"),
        "Yahoo占い": (get_yahoo(), "https://fortune.yahoo.co.jp/12astro/")
    }

    best_site = ""
    best_rank = 99
    best_link = ""

    for site, (rank, link) in results.items():
        print(site, rank)

        if rank < best_rank:
            best_rank = rank
            best_site = site
            best_link = link

    if best_site:
        print("\n🔮てんびん座 今日の最強占い")
        print(f"{best_site}：{best_rank}位")
        print(best_link)
    else:
        print("⚠️取得失敗")
