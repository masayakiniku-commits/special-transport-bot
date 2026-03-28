import requests
from bs4 import BeautifulSoup
import json
import os

# -----------------------------
# 設定
# -----------------------------
LINE_TOKEN = "pT3tMy7Wkdtxrzt/0Ok0tACP+qA8kiRjD5+bgWyekS5tAVdwqY0gHnWR49EETDVHLF5rKdfijeaxxfVbkInVdW6b8O+HAziOd/j6P/YCKj/IRqbCWMfxDJrE2Ja8BRk9FmgJcU55jHD2BEx1uVA3XwdB04t89/1O/w1cDnyilFU="

KEYWORDS = ["甲種輸送", "特殊貨物"]
LOCATIONS = ["岐阜","一宮","名古屋","刈谷","安城","岡崎","豊川","豊橋","浜松"]
THRESHOLD = 10

DATA_FILE = "data.json"

# -----------------------------
# LINE送信関数
# -----------------------------
def send_line(msg):
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": msg}
    try:
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("LINE通知失敗:", e)

# -----------------------------
# Yahoo検索から投稿数取得
# -----------------------------
def get_post_count():
    total = 0
    for kw in KEYWORDS:
        for loc in LOCATIONS:
            query = f"{kw} {loc}"
            url = f"https://search.yahoo.co.jp/search?p={query}"
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                # Yahoo検索の件数部分を取得（簡易版）
                cnt_tag = soup.select_one(".compPagination .numbers")
                if cnt_tag:
                    cnt = int(cnt_tag.text.replace(",", ""))
                    total += cnt
            except Exception as e:
                print(f"{query} 取得失敗:", e)
    return total

# -----------------------------
# 前回データの読み込み・保存
# -----------------------------
def load_prev():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"count":0}

def save_curr(count):
    with open(DATA_FILE, "w") as f:
        json.dump({"count": count}, f)

# -----------------------------
# メイン処理
# -----------------------------
def main():
    prev = load_prev()
    count = get_post_count()
    print("投稿数:", count, "(前回:", prev['count'], ")")

    if count - prev['count'] >= THRESHOLD:
        msg = f"甲種輸送・特殊貨物の投稿数増加！\n現在: {count}件 (前回比 +{count - prev['count']})"
        send_line(msg)

    save_curr(count)

if __name__ == "__main__":
    main()
