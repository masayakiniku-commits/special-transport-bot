import requests
from bs4 import BeautifulSoup

def get_yahoo():
    url = "https://fortune.yahoo.co.jp/12stars/libra/"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    rank_tag = soup.select_one("span.rank")  # 実際のHTML構造に合わせて修正
    if rank_tag:
        return int(rank_tag.text.strip())
    return 99

rank = get_yahoo()
print(f"★実行スタート")
print(f"今日のてんびん座は Yahoo占い！")
print(f"順位: {rank}位")
print(f"リンク: https://fortune.yahoo.co.jp/12stars/libra/")
