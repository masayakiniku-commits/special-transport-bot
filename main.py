# main.py

# -------------------------------
# テスト用：外部アクセス不要版
# -------------------------------

def get_yahoo():
    # 本来はスクレイピングするところですが、
    # Actions で DNS エラーになるので仮の順位を返す
    return 3  # 仮の順位（例）

def get_nifty():
    return 5  # 仮の順位（例）

def get_au():
    return 2  # 仮の順位（例）

if __name__ == "__main__":
    print("★実行スタート")
    
    rank_yahoo = get_yahoo()
    rank_nifty = get_nifty()
    rank_au = get_au()
    
    print(f"Yahoo占い順位: {rank_yahoo}")
    print(f"Nifty占い順位: {rank_nifty}")
    print(f"AU占い順位: {rank_au}")
    
    print("★処理完了（テスト用）")
