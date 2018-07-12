from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world! This is Bright's page."


@app.route("/flask")
def hello():
    return "hello flask"

@app.route("/user/<username>")
def user(username):
    return render_template("profile.html", name=username)

# json format api 만들기
@app.route("/people/<name>/<age>")
def people(name,age):
    users = {
        "name" : name,
        "age" : age,
        "kim":[
            {"age":31},
            {"email":"kim@gmail.com"},
        ]
    }
    return jsonify(users)

app.run()
