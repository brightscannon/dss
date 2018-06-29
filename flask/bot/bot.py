from flask import *
from lib.slack import send_slack
from lib.forecast import forecast

# forecast를 받아서 슬랙으로 보내주는 봇

# cmd에서 ngrok.exe http 5000 켜고

# 나오는 주소로 slack에 있는 리퀘스트 설정을 바꿔줘야함

app = Flask(__name__)

@app.route("/slack",methods=["POST"])
def slack():
    username = request.form.get("user_name")
    token = request.form.get("token")
    text = request.form.get("text")

    if "날씨" in text:
        msg = forecast()
        send_slack(msg)

    return Response(), 200

app.run()
