import os
import requests

# ----------------------------
# 設定
# ----------------------------
LINE_TOKEN = os.environ.get("LINE_TOKEN", "YOUR_LINE_TOKEN")  # GitHub Secrets推奨
SIGN = "libra"  # てんびん座
LINE_HEADERS = {"Authorization": f"Bearer {LINE_TOKEN}"}

# ----------------------------
# Vedika占い取得
# ----------------------------
def get_vedika(sign=SIGN):
    url = f"https://api.vedika.io/horoscope/today/{sign}"
    try:
        res = requests.get(url, timeout=10).json()
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
        return res.get("today", {}).get("summary", "AstroJson占い情報なし")
    except Exception as e:
        return f"AstroJson取得失敗: {e}"

# ----------------------------
# LINE通知
# ----------------------------
def send_line(message):
    try:
        res = requests.post(
            "https://notify-api.line.me/api/notify",
            headers=LINE_HEADERS,
            data={"message": message},
            timeout=10
        )
        if res.status_code != 200:
            print(f"LINE通知エラー: {res.status_code} {res.text}")
    except Exception as e:
        print(f"LINE通知失敗: {e}")

# ----------------------------
# メイン処理
# ----------------------------
if __name__ == "__main__":
    vedika_msg = get_vedika()
    astro_msg = get_astrojson()
    
    combined_message = (
        f"🔮今日の占い ({SIGN})\n\n"
        f"【Vedika】\n{vedika_msg}\n\n"
        f"【AstroJson】\n{astro_msg}"
    )
    
    print(combined_message)  # ログ用
    send_line(combined_message)
