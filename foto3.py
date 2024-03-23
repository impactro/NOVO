from flask import Flask, render_template
from card1 import card1Upload
from commom import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("aplicaFundo.html")


@app.route("/card1", methods=["POST"])
def upload():
    return card1Upload()


if __name__ == "__main__":
    app.run(debug=True)
