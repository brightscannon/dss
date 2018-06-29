import requests, json
WEBHOOK_URL = "https://hooks.slack.com/services/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"
def send_slack(msg):
    data = {
        "channel": "#webhook",
        "emoji": ":thumbsup_all:",
        "msg": msg,
        "username": "날씨봇",
    }
    payload = {
        "channel": data["channel"],
        "username": data["username"],
        "icon_emoji": data["emoji"],
        "text": data["msg"],
    }
    response = requests.post( WEBHOOK_URL, data = json.dumps(payload), )
send_slack("hello_world")
send_slack("오늘의 커밋왕 : 김민우_B")
