import requests
from bs4 import BeautifulSoup
import os

MY_SIGNS = ["てんびん座", "天秤座"]
MY_BLOOD = ["A型"]
MY_ETO = ["巳"]

HEADERS = {"User-Agent": "Mozilla/5.0"}
LINE_TOKEN = os.getenv("LINE_TOKEN")


def send_line(msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": msg}
    requests.post(url, headers=headers, data=data)


def get_ranking(url, selector):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    items = soup.select(selector)

    for i, item in enumerate(items, start=1):
        text = item.get_text(strip=True)
        results.append((i, text))

    return results


def zodiac():
    return get_ranking("https://fortune.goo.ne.jp/ranking/", ".ranking_list li")


def blood():
    return get_ranking("https://fortune.goo.ne.jp/blood/", "li")


def eto():
    return get_ranking("https://fortune.goo.ne.jp/", "li")


def get_best(results, targets, title):
    best = None
    for rank, text in results:
        if any(t in text for t in targets):
            if best is None or rank < best[1]:
                best = (title, rank, text)
    return best


def run():
    candidates = []

    for func, targets, name in [
        (zodiac, MY_SIGNS, "星座"),
        (blood, MY_BLOOD, "血液型"),
        (eto, MY_ETO, "干支"),
    ]:
        data = func()
        best = get_best(data, targets, name)
        if best:
            candidates.append(best)

    if not candidates:
        print("該当なし")
        return

    best_all = min(candidates, key=lambda x: x[1])

    title, rank, text = best_all
    msg = f"🔮今日の最強運勢\n\n{title} {rank}位\n{text}"

    print(msg)
    send_line(msg)


run()
