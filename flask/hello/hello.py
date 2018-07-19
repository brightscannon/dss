from flask import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)


Bootstrap(app) #요렇게 해줘야 적용된다.
# @app.route('/bootstrap') #접속할 URL
# def bootstrap():
# 	return render_template('bootstrap.html') #예제 템플릿

@app.route("/")
def index():
    # return "hello world! This is Bright's page."
    return render_template("index.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


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
