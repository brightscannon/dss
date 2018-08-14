from flask import *
import pickle
import numpy as np

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True, # 이것은 템플릿이 수정되면 자동으로 리로드함..
)

models = {}

def init():
    with open("./models/classification.pkl", "rb") as f:
        models["classification"] = pickle.load(f)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predic")
def predic():
    result = {}
    result["category"] = ["정치","경제","사회","생활/문화","세계","IT/과학"]

    model = models["classification"]

    sentence = request.values.get("sentence") #쿼리형태로 가져오는게 가능함
    result["sentence"] = sentence
    result["result"] = list(np.round_(model.predict_proba([sentence])[0]*100,2))

    return jsonify(result)


init()
app.run()
