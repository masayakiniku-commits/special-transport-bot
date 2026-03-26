def get_best(results, targets, title):
    """
    条件に合うものの中で一番順位が良いものを返す
    """
    best = None

    for rank, text in results:
        if any(t in text for t in targets):
            if best is None or rank < best[1]:
                best = (title, rank, text)

    return best


def run():
    print("処理開始")

    candidates = []

    # 星座
    z = zodiac()
    print("星座:", z)
    best = get_best(z, MY_SIGNS, "星座")
    if best:
        candidates.append(best)

    # 血液型
    b = blood()
    print("血液型:", b)
    best = get_best(b, MY_BLOOD, "血液型")
    if best:
        candidates.append(best)

    # 干支
    e = eto()
    print("干支:", e)
    best = get_best(e, MY_ETO, "干支")
    if best:
        candidates.append(best)

    # ----------------------
    # 最強だけ選ぶ
    # ----------------------
    if not candidates:
        print("該当なし（通知なし）")
        return

    best_all = min(candidates, key=lambda x: x[1])
    # x = (title, rank, text)

    title, rank, text = best_all

    msg = f"🔮今日の最強運勢\n\n{title} {rank}位\n{text}"

    print("送信内容:\n", msg)
    send_line(msg)


run()
