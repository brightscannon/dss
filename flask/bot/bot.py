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
    if "성령" in text:
        msg = "응~ 성령이?"
        send_slack(msg)
    if "이뻐?" in text:
        msg = "이쁘지~"
        send_slack(msg)
    if ("뭐야"or"모야") in text:
        msg = "뭐긴뭐야~"
        send_slack(msg)
    if "누구" in text:
        msg = "난 SR봇이라고해. 민우킴이 만들었지~"
        send_slack(msg)
    if "야" in text:
        msg = "근데 반말 하지는 마. 내가 누군지 알오??"
        send_slack(msg)
    if ("여친"or"여자친구") in text:
        msg = "민우님 짝이 이쁜사람이라는건 알지~"
        send_slack(msg)
    if "비밀" in text:
        msg = "쉿.... 너무 많을걸 알려고 하진 마"
        send_slack(msg)
    if "줘" in text:
        msg = "뭘... 난 정해진말밖에 못하는거 알잖아 ㅜ"
        send_slack(msg)
    if "너" in text:
        msg = "내이름은 너가 아니여~"
        send_slack(msg)
    if "민우" in text:
        msg = "민우는 항상 열심히 하려고 노력하고있지"
        send_slack(msg)
    if "사랑" in text:
        msg = "저두요~ 민우두 성령이 사랑해요~"
        send_slack(msg)
    if "해" in text:
        msg = "해해헤헤헤"
        send_slack(msg)
    if ("점심"or"식사"or"밥") in text:
        msg = "꼬르륵~....... 밥사준다고?? 나이수~"
        send_slack(msg)
    if ("아니"or"무슨") in text:
        msg = "?? 이게 무슨소리여 ㅜ"
        send_slack(msg)        
    return Response(), 200

app.run()
