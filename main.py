def send_line(msg):
    res = requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": "Bearer " + LINE_TOKEN},
        data={"message": msg}
    )
    
    print("STATUS:", res.status_code)
    print("BODY:", res.text)
