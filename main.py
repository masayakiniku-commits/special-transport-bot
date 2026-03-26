import requests

# ----------------------------
# 設定
# ----------------------------
LINE_TOKEN = "YOUR_LINE_TOKEN"  # GitHub Secrets に入れると安全
SIGN = "libra"  # てんびん座の場合
LINE_HEADERS = {"Authorization": f"Bearer {LINE_TOKEN}"}

# ----------------------------
# Vedika占い取得
# ----------------------------
def get_vedika(sign=SIGN):
    url = f"https://api.vedika.io/horoscope/today/{sign}"
    try:
        res = requests.get(url, timeout=10).json()
        # サンプル: res['description'] に今日の運勢が入っている想定
        return res.get("description", "Vedika占い情報なし")
    except Exception as e:
        return f"Vedika取得失敗: {e}"

# ----------------------------
# AstroJson占い取得
# ----------------------------
def get_astrojson(sign=SIGN):
    url = f"https://api.astrojson.io/horoscope/daily/{sign}"
    try:
        res = requests.get(url, timeout=10).json()
        # サンプル: res['today']['summary'] に今日の運勢が入っている想定
        return res.get("today", {}).get("summary", "AstroJson占い情報なし")
    except Exception as e:
        return f"AstroJson取得失敗: {e}"

# ----------------------------
# LINE通知
# ----------------------------
def send_line(message):
    try:
        requests.post("https://notify-api.line.me/api/notify", headers=LINE_HEADERS, data={"message": message})
    except Exception as e:
        print(f"LINE通知失敗: {e}")

# ----------------------------
# メイン処理
# ----------------------------
if __name__ == "__main__":
    messages = [
        f"🔮今日のVedika占い ({SIGN})\n{get_vedika()}",
        f"🔮今日のAstroJson占い ({SIGN})\n{get_astrojson()}"
    ]
    
    for msg in messages:
        print(msg)  # ログ用
        send_line(msg)
